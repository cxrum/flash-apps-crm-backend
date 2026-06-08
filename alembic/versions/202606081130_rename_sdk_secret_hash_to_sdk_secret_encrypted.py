"""rename sdk secret hash to sdk secret encrypted

Revision ID: 202606081130
Revises: 202603101800
Create Date: 2026-06-08 11:30:00
"""

from __future__ import annotations

from alembic import op


# revision identifiers, used by Alembic.
revision = "202606081130"
down_revision = "202603101800"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column(
        "crm_app_platforms",
        "sdk_secret_hash",
        new_column_name="sdk_secret_encrypted",
    )


def downgrade() -> None:
    op.alter_column(
        "crm_app_platforms",
        "sdk_secret_encrypted",
        new_column_name="sdk_secret_hash",
    )
