# MNIST Digit Prediction API using FastAPI

This project implements a FastAPI application that predicts handwritten digits from images using a pre-trained MNIST model. Users can upload an image containing a handwritten digit, and the API will return the predicted digit.

## Features

- FastAPI application with a `/predict` endpoint to handle image uploads and return predictions
- Model loading and prediction functions
- Image preprocessing for resizing and converting to grayscale
- Supports various image formats (e.g., PNG, JPEG)

## Getting Started

### Prerequisites

- Python 3.6 or higher
- Pickle
- TensorFlow
- FastAPI
- Pillow (PIL) library

### Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/mnist-fastapi.git
```
## Usage

1. First, run the model.ipynb file with the set of parameters you want. I have opted for a big neural network, however, you can also add regularization, stopping criteria, optimizer, etc.
2. Once the run finishes, the model will be saved in the .h5 format along with the model architecture and weights at the location where the model.ipynb file is saved however it is recommended to check the location.
3. The main.py has the code of the API. To run the FastAPI application:
```bash
uvicorn main:app --reload
```
4. In the command prompt, you get a link similar to "http://127.0.0.1:8000." copy and paste it into your web browser and navigate to "http://127.0.0.1:8000/docs" to access the Swagger UI.
5. Upload an image containing a handwritten digit using the /predict endpoint.
6. The API will return the predicted digit in the response.

## Testing

You can test the API by drawing handwritten digits using a simple image editor like MS Paint and uploading them through the Swagger UI.

## Model Training

The model.py file contains the code for training the MNIST model using TensorFlow and Keras. You can modify the model architecture and hyperparameters and save the trained model for use in the FastAPI application.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request if you have any improvements or bug fixes.



