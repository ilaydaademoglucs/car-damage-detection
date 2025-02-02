import requests
import numpy as np
import os


def download_model_to_memory(model_url):
    response = requests.get(model_url)
    # Check if the download is successful
    if response.status_code == 200:
        print("Weights downloaded successfully!")
        return np.frombuffer(
            response.content, np.uint8
        )  # Convert the downloaded bytes to a numpy array
    else:
        raise Exception(f"Failed to download model weights: {response.status_code}")


def download_model_to_tmp(model_url, tmp_file_path="/tmp/yolov3-tiny.weights"):
    # Download the YOLOv3-tiny weights
    tmp_dir = os.path.dirname(tmp_file_path)
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)
    response = requests.get(model_url)

    # Check if the download was successful
    if response.status_code == 200:
        # Save the weights to a temporary file in /tmp directory
        with open(tmp_file_path, "wb") as model_file:
            model_file.write(response.content)
        print(f"Weights downloaded and saved to {tmp_file_path} successfully.")
    else:
        raise Exception(f"Failed to download model weights: {response.status_code}")

    return tmp_file_path
