from app.modules.crm.infra.db.apps.models import Install as InstallModel
from app.modules.crm.infra.db.attribution.models import Click as ClickModel
from app.modules.crm.infra.db.attribution.models import CurrentParam as CurrentParamModel
from app.modules.crm.infra.db.attribution.models import Event as EventModel

__all__ = ["ClickModel", "CurrentParamModel", "EventModel", "InstallModel"]
