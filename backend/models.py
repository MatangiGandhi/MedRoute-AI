from sqlalchemy import Column, Integer, String
from db import Base


class BloodInventory(Base):
    __tablename__ = "blood_inventory"
    id = Column(Integer, primary_key=True, index=True)
    blood_bank_name = Column(String)
    blood_type = Column(String)
    units_available = Column(Integer)
    location = Column(String)

class HospitalRequest(Base):
    __tablename__ = "hospital_requests"
    id = Column(Integer, primary_key=True, index=True)
    hospital_name = Column(String)
    blood_type = Column(String)
    units_required = Column(Integer)
    urgency = Column(String)

class BloodBank(Base):
    __tablename__ = "blood_banks"

    id = Column(Integer, primary_key=True, index=True)
    bank_name = Column(String)
    blood_type = Column(String)
    available_units = Column(Integer)
    location = Column(String)