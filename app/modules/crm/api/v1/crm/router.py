from __future__ import annotations

from fastapi import APIRouter

from app.modules.crm.api.v1.crm.routes.app import router as app_router
from app.modules.crm.api.v1.crm.routes.audit import router as audit_router
from app.modules.crm.api.v1.crm.routes.conversions import router as conversion_router
from app.modules.crm.api.v1.crm.routes.metrics import router as metrics_router
from app.modules.crm.api.v1.crm.routes.params import router as params_router
from app.modules.crm.api.v1.crm.routes.postback import router as postback_router
from app.modules.crm.api.v1.crm.routes.push import router as push_router
from app.modules.crm.api.v1.crm.routes.roles import router as roles_router
from app.modules.crm.api.v1.crm.routes.secrets import router as secrets_router

router = APIRouter()

router.include_router(app_router, prefix="/app")
router.include_router(audit_router, prefix="/audit")
router.include_router(conversion_router, prefix="/conversion")
router.include_router(metrics_router, prefix="/metric")
router.include_router(params_router, prefix="/param")
router.include_router(postback_router, prefix="/postback")
router.include_router(push_router, prefix="/push")
router.include_router(roles_router, prefix="/role")
router.include_router(secrets_router, prefix="/secret")
