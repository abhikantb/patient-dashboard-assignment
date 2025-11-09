from pymongo import MongoClient
from fastapi import FastAPI, HTTPException
from datetime import datetime
from models import Patient


### connection to the database
client = MongoClient("mongodb://localhost:27017/")
conn = client["patients_database"]
collection = conn["records"]
app = FastAPI()


@app.get("/api/patients/")
def get_patients():
    patients = list(collection.find({}))
    for patient in patients:
        # Convert the ObjectId object to a simple string
        patient["_id"] = str(patient["_id"])
    return {"patients": patients}

@app.get("/")
def home():
    # This is what the server returns when you go to the root path (/)
    return {"message": "Welcome to the Patient API!"}

@app.post("/api/patients/")
def create_patient(patient: Patient):
    try:
        if not patient.name or not patient.phone:
            raise HTTPException(status_code=400, detail="Name and phone cannot be empty")
        if patient.age <= 0:
            raise HTTPException(status_code=400, detail="Age must be greater than 0")
        if patient.billed_amount < 0 or patient.outstanding_amount < 0:
            raise HTTPException(status_code=400, detail="Amounts cannot be negative")

        existing = collection.find_one({"phone": patient.phone})
        if existing:
            raise HTTPException(status_code=400, detail="Patient with this phone number already exists")    
        
        patient_data = patient.model_dump()  #converts that object into a normal Python dictionary.
        result = collection.insert_one(patient_data)
        return {"message": "Patient created successfully", "patient_id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating patient: {str(e)}")
        