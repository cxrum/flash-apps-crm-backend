"""platform version policy

Revision ID: 0d9359a914ee
Revises: befddfc0fff6
Create Date: 2026-06-12 15:45:34.774621
"""

from __future__ import annotations

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "0d9359a914ee"
down_revision = "befddfc0fff6"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "crm_app_platforms",
        sa.Column("version_policy", sa.JSON, nullable=True),
    )
    op.add_column(
        "crm_app_platforms",
        sa.Column("current_version", sa.String(255), nullable=False),
    )


def downgrade() -> None:
    op.drop_column("crm_app_platforms", "version_policy")
    op.drop_column("crm_app_platforms", "current_version")
