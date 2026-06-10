from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="MedRoute AI",
    description="Emergency Medical Logistics System",
    version="1.0"
)

class BloodRequest(BaseModel):
    hospital_name: str
    blood_type: str
    units_required: int
    urgency: str

@app.get("/")
def home():
    return {
        "project": "MedRoute AI",
        "status": "Backend Running Successfully"
    }

@app.post("/request-blood")
def request_blood(request: BloodRequest):
    return {
        "message": "Request Received",
        "hospital": request.hospital_name,
        "blood_type": request.blood_type,
        "units": request.units_required,
        "urgency": request.urgency
    }