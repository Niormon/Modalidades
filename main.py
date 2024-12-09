from fastapi import FastAPI
from src.routes.studentRoutes import STUDENT_ROUTES
from src.routes.institutionRoutes import INSTITUTION_ROUTES
from src.routes.modalityRoutes import MODALITY_ROUTES
from src.routes.teacherRoutes import TEACHER_ROUTES
from src.routes.trackingModeRoutes import TRACKING_MODE_ROUTES

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

# Incluir las rutas de estudiantes
app.include_router(STUDENT_ROUTES)

app.include_router(INSTITUTION_ROUTES)

app.include_router(MODALITY_ROUTES)

app.include_router(TEACHER_ROUTES)

app.include_router(TRACKING_MODE_ROUTES)