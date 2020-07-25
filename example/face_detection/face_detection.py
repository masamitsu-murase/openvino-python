import argparse
import cv2
from openvino.inference_engine import IECore


def print_model_info(network):
    print(network.input_info)
    for name in network.input_info:
        print(name, network.input_info[name].input_data.shape)
    print(network.outputs)
    for name in network.outputs:
        print(name, network.outputs[name].shape)


def load_exec_network(model_xml, model_bin, device="CPU"):
    ie = IECore()
    network = ie.read_network(model=model_xml, weights=model_bin)
    exec_net = ie.load_network(network=network, device_name=device)

    print_model_info(network)

    return exec_net


if __name__ == "__main__":
    # https://download.01.org/opencv/2020/openvinotoolkit/2020.4/open_model_zoo/models_bin/3/face-detection-retail-0005/FP32/
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-xml", required=True)
    parser.add_argument("--model-bin", required=True)
    parser.add_argument("image")
    args = parser.parse_args()

    input_name = "input.1"
    output_name = "527"
    exec_net = load_exec_network(args.model_xml, args.model_bin, "CPU")
    image = cv2.imread(args.image)
    rgb_image = image.transpose(2, 0, 1)
    input_image = rgb_image.reshape((1, ) + rgb_image.shape)
    output = exec_net.infer({input_name: input_image})
    result = output[output_name]

    size = 300
    for i in range(result.shape[2]):
        _, label, conf, x_min, y_min, x_max, y_max = result[0, 0, i, :]
        if label == 0 or conf < 0.8:
            continue

        cv2.rectangle(image, (int(x_min * size), int(y_min * size)),
                      (int(x_max * size), int(y_max * size)), (255, 0, 0), 3)

    cv2.imshow("result", image)
    cv2.waitKey(0)
