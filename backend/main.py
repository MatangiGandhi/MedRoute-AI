from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import HTTPException

from db import engine
from models import Base

Base.metadata.create_all(bind=engine)

from db import SessionLocal
from models import HospitalRequest, BloodBank
Base.metadata.create_all(bind=engine)
db = SessionLocal()

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
class BloodBankRequest(BaseModel):
    bank_name: str
    blood_type: str
    available_units: int
    location: str

@app.get("/")
def home():
    return {
        "project": "MedRoute AI",
        "status": "Backend Running Successfully"
    }

@app.post("/request-blood")
def request_blood(request: BloodRequest):

    new_request = HospitalRequest(
        hospital_name=request.hospital_name,
        blood_type=request.blood_type,
        units_required=request.units_required,
        urgency=request.urgency
    )

    db.add(new_request)
    db.commit()
    db.refresh(new_request)

    return {
        "message": "Request Saved Successfully",
        "request_id": new_request.id
    }

@app.get("/requests")
def get_requests():

    requests = db.query(HospitalRequest).all()

    return requests

@app.post("/add-bloodbank")
def add_bloodbank(request: BloodBankRequest):

    bank = BloodBank(
        bank_name=request.bank_name,
        blood_type=request.blood_type,
        available_units=request.available_units,
        location=request.location
    )

    db.add(bank)
    db.commit()
    db.refresh(bank)

    return {
        "message": "Blood Bank Added",
        "id": bank.id
    }

@app.get("/bloodbanks")
def get_bloodbanks():

    banks = db.query(BloodBank).all()

    return [
        {
            "id": b.id,
            "bank_name": b.bank_name,
            "blood_type": b.blood_type,
            "available_units": b.available_units,
            "location": b.location
        }
        for b in banks
    ]

@app.get("/match-blood/{request_id}")
def match_blood(request_id: int):

    request = db.query(HospitalRequest).filter(
        HospitalRequest.id == request_id
    ).first()

    if not request:
        raise HTTPException(
            status_code=404,
            detail="Request not found"
        )

    bank = db.query(BloodBank).filter(
        BloodBank.blood_type == request.blood_type,
        BloodBank.available_units >= request.units_required
    ).first()

    if not bank:
        return {
            "message": "No matching blood bank found"
        }

    bank.available_units -= request.units_required
    db.commit()
    db.refresh(bank)

    return {
        "hospital": request.hospital_name,
        "blood_type": request.blood_type,
        "units_required": request.units_required,
        "matched_bank": bank.bank_name,
        "available_units": bank.available_units,
        "location": bank.location
    }