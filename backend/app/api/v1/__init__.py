from fastapi import APIRouter
from app.api.v1 import auth, alerts, cases, assets, sensors, collect


router = APIRouter(prefix="/v1")

router.include_router(auth.router)
router.include_router(alerts.router)
router.include_router(cases.router)
router.include_router(assets.router)
router.include_router(sensors.router)
router.include_router(collect.router)
