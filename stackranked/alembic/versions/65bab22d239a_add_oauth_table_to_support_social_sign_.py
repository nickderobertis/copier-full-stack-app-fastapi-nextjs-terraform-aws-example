"""Add Oauth table to support social sign in

Revision ID: 65bab22d239a
Revises: 2ab89177fcba
Create Date: 2022-09-16 07:44:54.929466

"""
import sqlalchemy as sa
from alembic import op
from fastapi_users_db_sqlalchemy import GUID

# revision identifiers, used by Alembic.
revision = "65bab22d239a"
down_revision = "2ab89177fcba"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "oauth_account",
        sa.Column("oauth_name", sa.String(length=100), nullable=False),
        sa.Column("access_token", sa.String(length=1024), nullable=False),
        sa.Column("expires_at", sa.Integer(), nullable=True),
        sa.Column("refresh_token", sa.String(length=1024), nullable=True),
        sa.Column("account_id", sa.String(length=320), nullable=False),
        sa.Column("account_email", sa.String(length=320), nullable=False),
        sa.Column("id", GUID(), nullable=False),
        sa.Column("user_id", GUID(), nullable=False),
        sa.ForeignKeyConstraint(("user_id",), ["user.id"], ondelete="cascade"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_oauth_account_account_id"),
        "oauth_account",
        ["account_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_oauth_account_oauth_name"),
        "oauth_account",
        ["oauth_name"],
        unique=False,
    )
    op.add_column(
        "user",
        sa.Column(
            "has_real_password", sa.Boolean(), server_default="t", nullable=False
        ),
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_oauth_account_oauth_name"), table_name="oauth_account")
    op.drop_index(op.f("ix_oauth_account_account_id"), table_name="oauth_account")
    op.drop_table("oauth_account")
    op.drop_column("user", "has_real_password")
