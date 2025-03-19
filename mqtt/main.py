from fastapi import FastAPI
import uvicorn

from Doctor_Patient_System.scripts.init_db import initialize_db, initialize_db_1
from api.consumer_api import router as consumer_router
from api.publisher_api import router as publisher_router

app = FastAPI()

initialize_db()
initialize_db_1()

app.include_router(consumer_router, prefix="/consumer", tags=["Consumer"])
app.include_router(publisher_router, prefix="/publisher", tags=["Publisher"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=12378, reload=True)
