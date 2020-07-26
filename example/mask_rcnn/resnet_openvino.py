import argparse
import cv2
import numpy as np
from openvino.inference_engine import IECore, Blob, TensorDesc
import os
import time


def print_model_info(network):
    print(network.input_info)
    for name in network.input_info:
        print(name, network.input_info[name].input_data.shape)
    print(network.outputs)
    for name in network.outputs:
        print(name, network.outputs[name].shape)


def load_exec_network(model, device="CPU"):
    ie = IECore()
    # ie.set_config({'CPU_THROUGHPUT_STREAMS': 'CPU_THROUGHPUT_AUTO'}, "CPU")
    # ie.set_config({'CPU_THREADS_NUM': '4', "CPU_BIND_THREAD": "NO"}, "CPU")
    ie.set_config({'CPU_THREADS_NUM': '4'}, "CPU")
    if model.endswith(".bin"):
        xml = os.path.splitext(model)[0] + ".xml"
        network = ie.read_network(model=xml, weights=model)
    else:
        network = ie.read_network(model)
    exec_net = ie.load_network(network=network,
                               device_name=device,
                               num_requests=1)

    print_model_info(network)

    return exec_net


def preprocess(img_data):
    # See https://github.com/onnx/models/tree/master/vision/classification/resnet
    mean_vec = np.array([0.485, 0.456, 0.406])
    stddev_vec = np.array([0.229, 0.224, 0.225])
    norm_img_data = np.zeros(img_data.shape).astype('float32')
    for i in range(img_data.shape[0]):
        norm_img_data[i, :, :] = (img_data[i, :, :] / 255 -
                                  mean_vec[i]) / stddev_vec[i]
    return norm_img_data


def load_image(filepath):
    bgr_image = cv2.imread(filepath)
    rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
    image = rgb_image.transpose(2, 0, 1)
    return preprocess(image)


if __name__ == "__main__":
    # https://github.com/onnx/models/tree/master/vision/classification/resnet
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
    parser.add_argument("image")
    args = parser.parse_args()

    input_name = "data"
    output_name = "resnetv24_dense0_fwd"
    exec_net = load_exec_network(args.model, "CPU")

    nreq = len(exec_net.requests)
    input_image = [load_image(args.image) for _ in range(nreq)]
    req = [exec_net.requests[i] for i in range(nreq)]

    start = time.perf_counter()
    for _ in range(100 // nreq):
        output = exec_net.infer({input_name: input_image[0]})
        result = output[output_name]
        # for i in range(nreq):
        #     req[i].async_infer({input_name: input_image[i]})
        # for i in range(nreq):
        #     req[i].wait()
        #     output = req[i].output_blobs
        #     result = output[output_name].buffer
    end = time.perf_counter()
    # result = result0

    print(end - start)
    print(f"Index: {result[0, :].argmax()}, Value: {result[0, :].max()}")
