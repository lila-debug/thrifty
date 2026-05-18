"""Add session revocation timestamp."""

from __future__ import annotations

import sqlalchemy as sa

from alembic import op

revision = "0002_session_revocation"
down_revision = "0001_initial"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("session_revoked_after", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("users", "session_revoked_after")
