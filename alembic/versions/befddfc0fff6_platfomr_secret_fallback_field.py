"""platfomr secret fallback field

Revision ID: befddfc0fff6
Revises: 202606081130
Create Date: 2026-06-09 16:08:14.629150
"""

from __future__ import annotations

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "befddfc0fff6"
down_revision = "202606081130"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "crm_app_platforms",
        sa.Column("sdk_secret_fallback_encrypted", sa.String(length=255), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("crm_app_platforms", "sdk_secret_fallback_encrypted")
