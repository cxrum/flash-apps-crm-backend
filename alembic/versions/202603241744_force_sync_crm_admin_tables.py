"""force sync crm admin tables

Revision ID: 202603241744
Revises: 202603191320
Create Date: 2026-03-24 17:44:47
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "202603241744"
down_revision = "202603191320"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("crm_apps", sa.Column("category", sa.Text(), nullable=True))

    op.drop_table("crm_user_app_access")
    op.drop_table("crm_user_roles")
    op.drop_table("crm_role_permissions")

    op.create_table(
        "crm_user_permisions",
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("app_id", sa.BigInteger(), nullable=False),
        sa.Column("permission_id", sa.Integer(), nullable=False),
        sa.Column("assigned_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["permission_id"], ["crm_permissions.permission_id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["crm_users.user_id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["app_id"], ["crm_apps.app_id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("user_id", "permission_id", "app_id", name="pk_crm_user_permision"),
    )

    op.create_table(
        "crm_user_app_access",
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("app_id", sa.BigInteger(), nullable=False),
        sa.Column("role_id", sa.BigInteger(), nullable=False),
        sa.Column("assigned_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["app_id"], ["crm_apps.app_id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["role_id"], ["crm_roles.role_id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["crm_users.user_id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("user_id", "app_id", "role_id", name="pk_crm_user_app_access"),
    )


def downgrade() -> None:
    op.drop_table("crm_user_app_access")
    op.drop_table("crm_user_permisions")

    op.create_table(
        "crm_role_permissions",
        sa.Column("role_id", sa.Integer(), nullable=False),
        sa.Column("permission_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["permission_id"], ["crm_permissions.permission_id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["role_id"], ["crm_roles.role_id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("role_id", "permission_id", name="pk_crm_role_permissions"),
    )

    op.create_table(
        "crm_user_roles",
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("role_id", sa.Integer(), nullable=False),
        sa.Column("assigned_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["role_id"], ["crm_roles.role_id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["crm_users.user_id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("user_id", "role_id", name="pk_crm_user_roles"),
    )

    op.create_table(
        "crm_user_app_access",
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("app_id", sa.BigInteger(), nullable=False),
        sa.Column("access_level", sa.String(length=32), nullable=False),
        sa.Column("assigned_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint("access_level IN ('viewer', 'manager', 'owner')", name="ck_crm_user_app_access_level"),
        sa.ForeignKeyConstraint(["app_id"], ["crm_apps.app_id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["crm_users.user_id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("user_id", "app_id", name="pk_crm_user_app_access"),
    )

    op.drop_column("crm_apps", "category")
