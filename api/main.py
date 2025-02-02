import io
import os
import cv2
import numpy as np
from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from roboflow import Roboflow
import supervision as sv
import tempfile

app = FastAPI()
load_dotenv()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["POST"],  
    allow_headers=["*"],
)

api_key = os.environ.get('API_KEY')
if api_key is None:
    raise ValueError("API_KEY environment variable is not set")

api_key = str(api_key).strip()

if not api_key:
    raise ValueError("API_KEY environment variable is empty")
rf = Roboflow(api_key=api_key)

project_parts = rf.workspace().project("car-parts-segmentation")
model_parts = project_parts.version(2).model

project_damage = rf.workspace().project("car-damage-detection-ha5mm")
model_damage = project_damage.version(1).model

@app.post("/process-images/")
async def process_images_endpoint(file1: UploadFile = File(...), file2: UploadFile = File(...)):
    image1_bytes = await file1.read()
    image2_bytes = await file2.read()

    image1_array = np.frombuffer(image1_bytes, np.uint8)
    image2_array = np.frombuffer(image2_bytes, np.uint8)

    image1 = cv2.imdecode(image1_array, cv2.IMREAD_COLOR)
    image2 = cv2.imdecode(image2_array, cv2.IMREAD_COLOR)

    if image1 is None or image2 is None:
        return {"error": "One or both images could not be processed."}

    def process_image(image, image_number):
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp_file:
            img_path = temp_file.name
            cv2.imwrite(img_path, image)

        result_damage = model_damage.predict(img_path, confidence=17).json()

        detections_damage = sv.Detections.from_inference(result_damage)
        mask_annotator = sv.MaskAnnotator()

        annotated_image_damage = mask_annotator.annotate(scene=image, detections=detections_damage)

        coordinates = []
        damage_percentages = []  
        for prediction in result_damage['predictions']:
            coords = prediction['x'], prediction['y'], prediction['width'], prediction['height']
            confidence = prediction['confidence'] * 100  
            coordinates.append(coords)
            damage_percentages.append(confidence)

        if len(coordinates) == 0:
            add_text_with_background(annotated_image_damage, f"Image {image_number}: No damage detected", (50, 50))
            return annotated_image_damage, [], "No damage detected.", 0.0

        avg_damage_percentage = np.mean(damage_percentages) if damage_percentages else 0.0
        label_text = f"Image {image_number}: Damage Confidence: {avg_damage_percentage:.2f}%"
        add_text_with_background(annotated_image_damage, label_text, (50, 50))

        return annotated_image_damage, [], None, avg_damage_percentage

    def add_text_with_background(image, text, position):
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1.2  
        font_thickness = 2

        (text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, font_thickness)

        background_color = (255, 255, 113)  
        text_color = (0, 0, 0)  

        top_left_corner = (position[0], position[1] - text_height - 10)
        bottom_right_corner = (position[0] + text_width, position[1])
        cv2.rectangle(image, top_left_corner, bottom_right_corner, background_color, cv2.FILLED)

        cv2.putText(image, text, (position[0], position[1] - 5), font, font_scale, text_color, font_thickness, cv2.LINE_AA)

    annotated_image1, parts1, error1, avg_damage1 = process_image(image1, 1)
    annotated_image2, parts2, error2, avg_damage2 = process_image(image2, 2)

    # If both images have no damage
    if error1 == "No damage detected." and error2 == "No damage detected.":
        # Concatenate the images and write "No damage detected" on them
        combined_image = np.hstack((annotated_image1, annotated_image2))
        add_text_with_background(combined_image, "No damage detected", (50, 50))

        _, img_encoded = cv2.imencode(".png", combined_image)
        img_byte_arr = io.BytesIO(img_encoded)
        return StreamingResponse(img_byte_arr, media_type="image/png")

    # Resize images to have the same height for concatenation
    def resize_to_same_height(img1, img2):
        height1, width1, _ = img1.shape
        height2, width2, _ = img2.shape

        new_height = min(height1, height2)

        # Calculate width preserving the aspect ratio
        new_width1 = int(width1 * (new_height / height1))
        new_width2 = int(width2 * (new_height / height2))

        # Resize both images
        img1_resized = cv2.resize(img1, (new_width1, new_height))
        img2_resized = cv2.resize(img2, (new_width2, new_height))

        return img1_resized, img2_resized

    # Resize images to match heights
    annotated_image1_resized, annotated_image2_resized = resize_to_same_height(annotated_image1, annotated_image2)

    combined_image = np.hstack((annotated_image1_resized, annotated_image2_resized))

    _, img_encoded = cv2.imencode(".png", combined_image)
    img_byte_arr = io.BytesIO(img_encoded)

    damaged_parts = (f"Image 1 Damage Confidence: {avg_damage1:.2f}%; "
                     f"Image 2 Damage Confidence: {avg_damage2:.2f}%")

    # Return the combined image with the damaged parts and damage percentage in the response headers
    return StreamingResponse(img_byte_arr, media_type="image/png", headers={"Damaged-Parts": damaged_parts})
