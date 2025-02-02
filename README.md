# Car Damage Detection via image comparison
Car Damage Detection via image comparison is a full-stack application designed to compare two images of cars, detect damage, and highlight the damaged areas. It uses advanced machine learning models from Roboflow to process the images and provide visual feedback on potential damage.

<img width="882" alt="Difference Image" src="https://github.com/user-attachments/assets/2b4dc013-2201-467d-8246-eefa7365c227" />

## Features

- Upload and compare two car images
- Detect and highlight damaged areas on the cars
- Provide damage confidence percentages for each image
- Combine processed images for side-by-side comparison
  
## Project Structure

The project is organized as a monorepo with separate frontend and backend directories:


    .
    car-image-diff-check/
    ├── ...
    ├── api/                   
    │   ├── main.py           
    │   ├── poetry.lock           
    │   ├── pyproject.toml        
    │   ├── requirements.txt           
    │   └── .env                
    └── client/
    │   │── public/             
    │   ├── src/         
    │   ├── README.md      
    ├── .gitignore         
    └── README.md           

## Technologies Used

### Backend
- FastAPI
- OpenCV (cv2)
- NumPy
- Roboflow
- Supervision

### Frontend
- Vue.js
- JavaScript (ES6+)
- HTML5
- CSS3

## Machine Learning Models

This project utilizes two machine learning models from Roboflow:
1. Car Parts Segmentation: [Car Parts Segmentation Model](https://universe.roboflow.com/segmentation-9q8ob/car-parts-llqro)
2. Car Damage Detection: [Car Damage Detection Model](https://universe.roboflow.com/roboflow-universe-projects/car-damage-detection-ha5mm)

The main.py file implements a multi-step process to analyze car images for damage. The algorithm accepts two images of a car for comparison.

Damage Detection:
Both images are processed through the Car Damage Detection model.
Areas of potential damage are identified and their coordinates extracted.

Car Parts Segmentation:
The images are then passed through the Car Parts Segmentation model.
This step identifies and segments individual car parts in both images.

Damage Localization:
The algorithm correlates the detected damage areas with the segmented car parts for identifying
which specific car parts are damaged.

Comparison and Analysis:
The results from both images are compared to identify any new or additional damage.
Damage confidence percentages are calculated for each affected part.

Results:
The algorithm produces a detailed report of the damage assessment, including:
Affected car parts
Damage confidence percentages
Visual representation of the damage

## Setup and Installation

### Backend

1. Navigate to the backend directory:
```cd api```

2. Install the required dependencies:
```poetry install```

3. Create a `.env` file in the backend directory and add your Roboflow API key:
```API_KEY=your_roboflow_api_key```

4. Run the FastAPI server:
```poetry run uvicorn main:app --reload```


### Frontend

1. Navigate to the frontend directory:
```cd client```

2. Install the required dependencies:
```npm install```

3. Start the development server:
```npm run serve```

## Usage

1. Start both the backend and frontend servers.
2. Open the frontend application in a web browser (at http://localhost:8080).
3. Upload two images of cars you want to compare using the file input fields.
4. Click the "Compare Images" button to process the images.
5. The application will display the processed images side by side with damaged areas highlighted.
6. Damage confidence percentages for each image will be shown below the processed images.

## API Endpoints

### POST /process-images/

Accepts two image files and returns a processed image with damaged areas highlighted.

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body:
- file1: (required) First image file (JPEG or PNG)
- file2: (required) Second image file (JPEG or PNG)

**Response:**
- Status Code: 200 OK
- Content-Type: image/png
- Body: Combined processed image
- Damaged-Parts: String containing damage confidence percentages for both images

**Notes**
Maximum file size: 10MB per image
Supported image formats: JPEG, PNG
Processing time may vary based on image size and complexity

## Acknowledgements

- [Roboflow](https://roboflow.com/) for providing the machine learning models
- [FastAPI](https://fastapi.tiangolo.com/) for the backend framework
- [Vue.js](https://vuejs.org/) for the frontend library
- [OpenCV](https://opencv.org/) for image processing capabilities
