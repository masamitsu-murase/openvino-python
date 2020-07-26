import argparse
import cv2
import numpy as np
import onnxruntime
import time


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
    output_name = "resnetv27_dense0_fwd"
    sess = onnxruntime.InferenceSession(args.model, None)

    input_image = load_image(args.image)
    input_image = input_image[np.newaxis, :]

    start = time.perf_counter()
    for _ in range(100):
        output = sess.run([output_name], {input_name: input_image})
        result = output[0]
    end = time.perf_counter()

    print(end - start)
    print(f"Index: {result[0, :].argmax()}, Value: {result[0, :].max()}")
