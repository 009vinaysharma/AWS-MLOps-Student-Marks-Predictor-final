import json
import requests

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


# ==========================================
# FASTAPI APP
# ==========================================

app = FastAPI(title="Student Marks Prediction API")


# ==========================================
# CORS
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# API GATEWAY URL
# ==========================================

API_GATEWAY_URL = (
    "https://86w0p4fw37.execute-api.eu-north-1.amazonaws.com/predict"
)


# ==========================================
# REQUEST MODEL
# ==========================================

class Student(BaseModel):
    maths: float
    english: float


# ==========================================
# HOME ROUTE
# ==========================================

@app.get("/")
def home():
    return {
        "status": "success",
        "message": "Student Marks Prediction API is running"
    }


# ==========================================
# PREDICTION ROUTE
# ==========================================

@app.post("/predict")
def predict(student: Student):

    payload = {
        "maths": student.maths,
        "english": student.english
    }

    try:
        print("Sending payload to API Gateway:")
        print(payload)

        response = requests.post(
            API_GATEWAY_URL,
            json=payload,
            headers={
                "Content-Type": "application/json"
            },
            timeout=30
        )

        print("API Gateway Status Code:")
        print(response.status_code)

        print("API Gateway Raw Response:")
        print(response.text)

        # API Gateway error
        if not response.ok:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.text
            )

        # Convert response to JSON
        result = response.json()

        print("Parsed API Response:")
        print(result)

        # ----------------------------------
        # CASE 1:
        # {"prediction": [43.45]}
        # ----------------------------------

        if "prediction" in result:

            prediction = result["prediction"]

        # ----------------------------------
        # CASE 2:
        # {
        #   "statusCode": 200,
        #   "body": "{\"prediction\": [43.45]}"
        # }
        # ----------------------------------

        elif "body" in result:

            body = result["body"]

            # Lambda body may be JSON string
            if isinstance(body, str):
                body = json.loads(body)

            if "prediction" not in body:
                raise HTTPException(
                    status_code=500,
                    detail=f"Prediction missing in Lambda response: {body}"
                )

            prediction = body["prediction"]

        else:

            raise HTTPException(
                status_code=500,
                detail=f"Unexpected API response: {result}"
            )

        # SageMaker returns prediction as list
        # Example: [43.454169268701456]

        if isinstance(prediction, list):

            if len(prediction) == 0:
                raise HTTPException(
                    status_code=500,
                    detail="Empty prediction received"
                )

            prediction = prediction[0]

        # Convert to float and round
        prediction = round(float(prediction), 2)

        # Final response to frontend
        return {
            "status": "success",
            "prediction": prediction
        }


    except HTTPException:
        raise


    except requests.exceptions.Timeout:

        raise HTTPException(
            status_code=504,
            detail="API Gateway request timed out"
        )


    except requests.exceptions.RequestException as e:

        raise HTTPException(
            status_code=500,
            detail=f"Error connecting to API Gateway: {str(e)}"
        )


    except Exception as e:

        print("Unexpected Error:")
        print(str(e))

        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}"
        )


# ==========================================
# RUN SERVER
# ==========================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=5000,
        reload=True
    )