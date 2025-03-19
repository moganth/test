import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from Hospital_Service.Doctor_Service.api.doctor_api import router as doctor_router
from Hospital_Service.Doctor_Service.api.test_api import router as test_router
from Hospital_Service.Doctor_Service.database import initialize_db
from Hospital_Service.Doctor_Service.handlers.mqtt_handler import start_mqtt_client
from Hospital_Service.Doctor_Service.utils.logger import logger

app = FastAPI(title="Doctor Service", description="API for doctor-related functionality")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(doctor_router, tags=["Doctor"])
app.include_router(test_router, tags=["Tests"])

@app.on_event("startup")
async def startup_event():
    initialize_db()
    start_mqtt_client()
    logger.info("Doctor Service has started")

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "Doctor Service"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=12398, reload=True)