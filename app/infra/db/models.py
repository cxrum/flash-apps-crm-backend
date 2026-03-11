"""Import model modules so SQLAlchemy metadata is populated."""

from app.infra.db.access import models as access_models  # noqa: F401
from app.infra.db.apps import models as apps_models  # noqa: F401
from app.infra.db.attribution import models as attribution_models  # noqa: F401
from app.infra.db.audit import models as audit_models  # noqa: F401
from app.infra.db.config import models as config_models  # noqa: F401
from app.infra.db.crm import models as crm_models  # noqa: F401
from app.infra.db.push import models as push_models  # noqa: F401
