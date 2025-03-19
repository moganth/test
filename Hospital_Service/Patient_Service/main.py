import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from Hospital_Service.Patient_Service.api.patient_api import router as patient_router
from Hospital_Service.Patient_Service.database import initialize_db
from Hospital_Service.Patient_Service.handlers.mqtt_handler import start_mqtt_client
from Hospital_Service.Patient_Service.utils.logger import logger

app = FastAPI(title="Patient Service", description="API for patient-related functionality")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(patient_router, tags=["Patient"])

@app.on_event("startup")
async def startup_event():
    initialize_db()
    start_mqtt_client()
    logger.info("Patient Service has started")

@app.get("/Sick")
def health_check():
    return {"status": "Sick", "service": "Patient Service"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=12378, reload=True)