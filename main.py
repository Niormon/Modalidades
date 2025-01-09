from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes.studentRoutes import STUDENT_ROUTES
from src.routes.institutionRoutes import INSTITUTION_ROUTES
from src.routes.modalityRoutes import MODALITY_ROUTES
from src.routes.teacherRoutes import TEACHER_ROUTES
from src.routes.trackingModeRoutes import TRACKING_MODE_ROUTES
from src.routes.rolRoutes import ROL_ROUTER
from src.routes.usuarioRoutes import USUARIO_ROUTER
from src.routes.authRoutes import AUTH_ROUTER
from src.routes.permisoRoutes import PERMISO_ROUTER
from src.routes.rolPermisoRoutes import ROL_PERMISO_ROUTER

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

# Incluir las rutas
app.include_router(STUDENT_ROUTES)

app.include_router(INSTITUTION_ROUTES)

app.include_router(MODALITY_ROUTES)

app.include_router(TEACHER_ROUTES)

app.include_router(TRACKING_MODE_ROUTES)

app.include_router(ROL_ROUTER)

app.include_router(USUARIO_ROUTER)

app.include_router(AUTH_ROUTER)

app.include_router(PERMISO_ROUTER)

app.include_router(ROL_PERMISO_ROUTER)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)