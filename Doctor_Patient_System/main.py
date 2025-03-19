import threading
from fastapi import FastAPI
import uvicorn

from scripts.init_db import initialize_db, initialize_db_1

from api.producer_api import router as producer_router
from api.consumer_api import router as consumer_router
from api.prescription_api import router as prescription_router
from api.test_api import router as test_router
from services.report_visualizer import run_gui
from api.gui_api import router as gui_router

initialize_db()
initialize_db_1()

app = FastAPI(
    title="Doctor-Patient Service", description="API for doctor & patient related functionality"
)

app.include_router(producer_router, tags=["Patient"])
app.include_router(consumer_router, tags=["Doctor"])
app.include_router(prescription_router, tags=["Prescription"])
app.include_router(test_router, tags=["Reports"])
app.include_router(gui_router, tags=["GUI"])

# if __name__ == "__main__":
#     run_gui()                                          #not working because we need to run both gui and the uvicorn
                                                         #concurrently
#     uvicorn.run(app, host="localhost", port=12354)

# netstat -ano | findstr :12354
# taskkill /PID  17384 /F

def start_fastapi():
    uvicorn.run(app, host="localhost", port=12354)


if __name__ == "__main__":
    fastapi_thread = threading.Thread(target=start_fastapi, daemon=True)
    fastapi_thread.start()

    run_gui()