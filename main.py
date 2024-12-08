from fastapi import FastAPI
from src.routes.studentRoutes import STUDENT_ROUTES
from src.routes.institutionRoutes import INSTITUTION_ROUTES

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

# Incluir las rutas de estudiantes
app.include_router(STUDENT_ROUTES)

app.include_router(INSTITUTION_ROUTES)