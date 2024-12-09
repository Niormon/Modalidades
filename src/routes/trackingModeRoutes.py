from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.database import get_db
from src.schemas.trackingModeSchema import TrackingModeCreate, TrackingModeUpdate, TrackingModeResponse, TrackingModeResponseGet
from src.controllers.trackingModeController import (
    get_tracking_modes,
    get_tracking_mode,
    create_tracking_mode,
    update_tracking_mode,
    delete_tracking_mode,
)

TRACKING_MODE_ROUTES = APIRouter()

@TRACKING_MODE_ROUTES.get("/tracking_modes/", response_model=list[TrackingModeResponseGet])
async def list_tracking_modes(db: AsyncSession = Depends(get_db)):
    return await get_tracking_modes(db)

@TRACKING_MODE_ROUTES.get("/tracking_modes/{tracking_mode_id}", response_model=TrackingModeResponseGet)
async def get_tracking_mode_by_id(tracking_mode_id: int, db: AsyncSession = Depends(get_db)):
    return await get_tracking_mode(db, tracking_mode_id)

@TRACKING_MODE_ROUTES.post("/tracking_modes/", response_model=TrackingModeResponse)
async def create_tracking_mode_endpoint(tracking_mode: TrackingModeCreate, db: AsyncSession = Depends(get_db)):
    return await create_tracking_mode(db, tracking_mode)

@TRACKING_MODE_ROUTES.put("/tracking_modes/{tracking_mode_id}", response_model=TrackingModeResponse)
async def update_tracking_mode_endpoint(tracking_mode_id: int, tracking_mode: TrackingModeUpdate, db: AsyncSession = Depends(get_db)):
    return await update_tracking_mode(db, tracking_mode_id, tracking_mode)

@TRACKING_MODE_ROUTES.delete("/tracking_modes/{tracking_mode_id}")
async def delete_tracking_mode_endpoint(tracking_mode_id: int, db: AsyncSession = Depends(get_db)):
    return await delete_tracking_mode(db, tracking_mode_id)
