from fastapi import FastAPI
import uvicorn
from api.teacher_api import router as teacher_router
from api.student_api import router as student_router
from core.database import init_db

app = FastAPI()

init_db()

app.include_router(teacher_router, prefix="/teacher", tags=["Teacher"])
app.include_router(student_router, prefix="/student", tags=["Student"])
if __name__ == "__main__":
    uvicorn.run(app, host = "localhost", port = 12356)