# 🎓 AWS MLOps Student Marks Predictor

An end-to-end Machine Learning deployment project that predicts a student's **Physics marks** using their **Maths and English marks**.

The project demonstrates a complete cloud-based ML inference workflow using **Amazon SageMaker, AWS Lambda, Amazon API Gateway, Amazon S3, FastAPI, and a web frontend**.

---

## 📌 Project Overview

The **AWS MLOps Student Marks Predictor** is an end-to-end machine learning application built to demonstrate how a trained ML model can be deployed and consumed through a cloud-based architecture.

The machine learning model takes two input features:

- Maths Marks
- English Marks

and predicts:

- Physics Marks

The model is trained using student marks data, packaged as a SageMaker-compatible model artifact, uploaded to Amazon S3, deployed to a real-time Amazon SageMaker endpoint, exposed through AWS Lambda and Amazon API Gateway, and finally consumed through a FastAPI backend and HTML frontend.

---

## 🏗️ System Architecture

```text
┌───────────────────────┐
│     HTML Frontend     │
│ Maths + English Input │
└───────────┬───────────┘
            │
            │ HTTP POST
            ▼
┌───────────────────────┐
│    FastAPI Backend    │
│   POST /predict       │
└───────────┬───────────┘
            │
            │ REST API Request
            ▼
┌───────────────────────┐
│   Amazon API Gateway  │
│   /predict Endpoint   │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│      AWS Lambda       │
│  Invokes SageMaker    │
└───────────┬───────────┘
            │
            │ invoke_endpoint()
            ▼
┌───────────────────────┐
│   Amazon SageMaker    │
│ Real-Time ML Endpoint │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│  Prediction Response  │
│ Estimated Physics Mark│
└───────────────────────┘
```

---

## 🚀 End-to-End Workflow

### 1. Dataset Preparation

The project uses student academic data containing fields such as:

- Student Name
- Gender
- Physics Marks
- Maths Marks
- English Marks

For the prediction model:

```text
Input Features:
Maths + English

Target:
Physics
```

The model learns the relationship between Maths and English performance to estimate Physics marks.

---

### 2. Model Training

The machine learning model is trained using Python and Scikit-learn.

The trained model is serialized using Joblib:

```text
model.joblib
```

The model is then packaged into a compressed SageMaker-compatible artifact:

```text
model.tar.gz
```

---

### 3. Amazon S3 Model Storage

The packaged model artifact is uploaded to an Amazon S3 bucket.

Example structure:

```text
S3 Bucket
└── model/
    └── model.tar.gz
```

Amazon SageMaker loads the model artifact directly from Amazon S3 during deployment.

---

### 4. Custom SageMaker Inference Script

The project uses a custom inference script:

```text
Inference.py
```

The inference script implements the SageMaker inference lifecycle:

```python
model_fn()
input_fn()
predict_fn()
output_fn()
```

### `model_fn()`

Loads the trained Joblib model from the SageMaker model directory.

### `input_fn()`

Receives JSON input containing:

```json
{
  "maths": 70,
  "english": 60
}
```

and converts it into the format expected by the machine learning model.

### `predict_fn()`

Runs the model prediction.

### `output_fn()`

Returns the prediction as a JSON response:

```json
{
  "prediction": [67.45]
}
```

---

### 5. Amazon SageMaker Deployment

The Scikit-learn model is deployed as a real-time Amazon SageMaker endpoint.

The endpoint provides scalable cloud-based model inference.

The deployed model receives:

```json
{
  "maths": 70,
  "english": 60
}
```

and returns a prediction similar to:

```json
{
  "prediction": [67.45]
}
```

---

### 6. AWS Lambda Integration

AWS Lambda acts as the serverless integration layer between Amazon API Gateway and the SageMaker endpoint.

The Lambda function:

1. Receives the HTTP request from API Gateway.
2. Extracts the JSON request body.
3. Uses the AWS SDK for Python (`boto3`).
4. Invokes the SageMaker real-time endpoint.
5. Reads the model prediction.
6. Returns the result to API Gateway.

Core SageMaker invocation:

```python
response = runtime.invoke_endpoint(
    EndpointName=ENDPOINT_NAME,
    ContentType="application/json",
    Body=json.dumps(body)
)
```

---

### 7. Amazon API Gateway

Amazon API Gateway exposes the Lambda function through an HTTP API.

The application sends a POST request to:

```text
/predict
```

Request body:

```json
{
  "maths": 70,
  "english": 60
}
```

API Gateway forwards the request to AWS Lambda, which invokes the SageMaker endpoint.

---

### 8. FastAPI Backend

The project includes a FastAPI application that acts as the application backend.

Available endpoints:

```text
GET  /
POST /predict
```

### Health Check

```http
GET /
```

Example response:

```json
{
  "status": "success",
  "message": "Student Marks Prediction API is running"
}
```

### Prediction Endpoint

```http
POST /predict
```

Request:

```json
{
  "maths": 70,
  "english": 60
}
```

Example response:

```json
{
  "status": "success",
  "prediction": 67.45
}
```

The FastAPI backend communicates with Amazon API Gateway and returns the final prediction to the frontend.

---

## 🖥️ Web Interface

The project includes a simple HTML-based frontend.

Users can enter:

- Maths marks
- English marks

and click:

```text
Predict Marks Evaluation
```

The frontend sends the input to the FastAPI backend and displays the estimated Physics marks returned by the AWS-hosted machine learning model.

---

## 🛠️ Technology Stack

### Machine Learning

- Python
- NumPy
- Pandas
- Scikit-learn
- Joblib
- Jupyter Notebook

### Backend

- FastAPI
- Uvicorn
- Pydantic
- Requests

### AWS Cloud

- Amazon SageMaker
- Amazon S3
- AWS Lambda
- Amazon API Gateway
- AWS IAM
- Boto3

### Frontend

- HTML5
- CSS3
- JavaScript
- Fetch API

### Version Control

- Git
- GitHub

---

## 📂 Project Structure

```text
AWS-MLOps-Student-Marks-Predictor-final/
│
├── screenshots/
│   ├── Lambda-Function-event-test-ss.png
│   ├── Lambda-Function.png
│   ├── Output1.png
│   ├── Output2.png
│   ├── S3-bucket-1.png
│   ├── S3-bucket-3.png
│   ├── Sagemaker-Ai-Lab ss.png
│   ├── api1.png
│   ├── api2.png
│   ├── api3.png
│   └── s3-bucket-2.png
│
├── Inference.py
├── Lambda-Function.py
├── Untitled1.ipynb
├── app.py
├── index (1).html
├── model.joblib
├── model.tar.gz
├── requirements.txt
├── student-data.json
├── .gitignore
└── README.md
```

---

## ⚙️ Installation and Local Setup

### 1. Clone the Repository

```bash
git clone https://github.com/009vinaysharma/AWS-MLOps-Student-Marks-Predictor-final.git
```

Move into the project directory:

```bash
cd AWS-MLOps-Student-Marks-Predictor-final
```

---

### 2. Create a Virtual Environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux / macOS

```bash
python -m venv venv
source venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

The project uses:

```text
FastAPI
Uvicorn
Pydantic
NumPy
Pandas
Scikit-learn
Joblib
Requests
```

---

### 4. Run the FastAPI Backend

```bash
python app.py
```

The backend will run at:

```text
http://127.0.0.1:5000
```

---

### 5. Open Swagger API Documentation

Open:

```text
http://127.0.0.1:5000/docs
```

You can test the `/predict` endpoint directly from the interactive Swagger UI.

Example request:

```json
{
  "maths": 70,
  "english": 60
}
```

---

### 6. Run the Frontend

Open:

```text
index (1).html
```

in a web browser.

Make sure the FastAPI backend is running before making a prediction.

---

## 📸 Project Screenshots

### Amazon SageMaker AI Lab

![Amazon SageMaker AI Lab](screenshots/Sagemaker-Ai-Lab%20ss.png)

### Amazon S3 Bucket

![Amazon S3 Bucket](screenshots/S3-bucket-1.png)

![Amazon S3 Model Storage](screenshots/s3-bucket-2.png)

![Amazon S3 Model Artifact](screenshots/S3-bucket-3.png)

### AWS Lambda Function

![AWS Lambda Function](screenshots/Lambda-Function.png)

### AWS Lambda Test Event

![AWS Lambda Test Event](screenshots/Lambda-Function-event-test-ss.png)

### Amazon API Gateway

![API Gateway](screenshots/api1.png)

![API Gateway Configuration](screenshots/api2.png)

![API Gateway Testing](screenshots/api3.png)

### Application Output

![Application Output 1](screenshots/Output1.png)

![Application Output 2](screenshots/Output2.png)

---

## 🔄 Request Flow

A prediction request travels through the following services:

```text
1. User enters Maths and English marks
                ↓
2. HTML frontend sends POST request
                ↓
3. FastAPI receives the request
                ↓
4. FastAPI calls Amazon API Gateway
                ↓
5. API Gateway triggers AWS Lambda
                ↓
6. Lambda invokes Amazon SageMaker Endpoint
                ↓
7. SageMaker model generates Physics prediction
                ↓
8. Lambda returns the prediction
                ↓
9. API Gateway returns the response
                ↓
10. FastAPI processes the response
                ↓
11. Frontend displays the predicted Physics marks
```

---

## 🧪 Example Prediction

### Input

```json
{
  "maths": 70,
  "english": 60
}
```

### Output

```json
{
  "status": "success",
  "prediction": 67.45
}
```

> The exact prediction depends on the trained model.

---

## ✨ Key Features

- End-to-end machine learning workflow
- Student Physics marks prediction
- Scikit-learn model training
- Model serialization using Joblib
- Model packaging for Amazon SageMaker
- Amazon S3 model artifact storage
- Custom SageMaker inference script
- Real-time SageMaker endpoint deployment
- Serverless inference using AWS Lambda
- REST API using Amazon API Gateway
- FastAPI backend integration
- Interactive Swagger API documentation
- HTML, CSS, and JavaScript frontend
- Complete cloud-based prediction workflow

---

## 🔐 AWS Security

This project uses AWS IAM roles and permissions to allow AWS services to communicate securely.

Typical permissions required include:

- SageMaker access to the S3 model artifact
- Lambda permission to invoke the SageMaker endpoint
- IAM execution roles for AWS services

AWS credentials should never be hardcoded or committed to the repository.

---

## 💡 What I Learned

Through this project, I gained hands-on experience with:

- Building and training a machine learning model
- Serializing ML models using Joblib
- Packaging ML models for cloud deployment
- Uploading model artifacts to Amazon S3
- Creating custom inference logic for SageMaker
- Deploying a Scikit-learn model to a real-time SageMaker endpoint
- Invoking SageMaker endpoints using Boto3
- Building serverless integrations with AWS Lambda
- Exposing cloud services through Amazon API Gateway
- Developing REST APIs using FastAPI
- Connecting frontend, backend, and cloud ML services
- Debugging end-to-end cloud inference pipelines
- Managing project source code using Git and GitHub

---

## 🔮 Future Improvements

Possible improvements include:

- Add API authentication and authorization
- Store the API Gateway URL in environment variables
- Store the SageMaker endpoint name in environment variables
- Add automated model retraining
- Add model versioning
- Add CI/CD using GitHub Actions
- Add Amazon CloudWatch monitoring
- Add SageMaker Model Monitor
- Containerize the FastAPI application using Docker
- Deploy the FastAPI backend to a cloud hosting service
- Improve the frontend UI
- Add automated tests
- Use a larger real-world dataset

---

## 👨‍💻 Author

**Vinay Sharma**

B.Tech — Computer Science & Engineering (Artificial Intelligence)

Interested in:

- Machine Learning
- Data Science
- AWS Cloud
- MLOps
- AI Engineering

GitHub: `009vinaysharma`

---

## ⭐ Support

If you find this project useful, consider giving the repository a ⭐.

---

## 📄 Disclaimer

This project is created for educational and learning purposes. The dataset is small, so the predictions should be treated as a demonstration of an end-to-end machine learning deployment architecture rather than a production-grade academic prediction system.
