def coordinate_request(hospital, blood_bank):

    return {
        "hospital_agent": f"Request received from {hospital}",
        "bloodbank_agent": f"Blood available at {blood_bank}",
        "transport_agent": "Transport assigned",
        "status": "Coordination Successful"
    }