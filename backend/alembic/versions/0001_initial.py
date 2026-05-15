"""Initial Thrifty schema."""

from __future__ import annotations

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS citext")

    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column("email", postgresql.CITEXT(), nullable=False, unique=True),
        sa.Column("timezone", sa.Text(), nullable=False, server_default="Europe/London"),
        sa.Column("locale", sa.Text(), nullable=False, server_default="en-GB"),
        sa.Column("default_currency", sa.CHAR(3), nullable=False, server_default="GBP"),
        sa.Column("tier", sa.Text(), nullable=False, server_default="free"),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()
        ),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint("tier IN ('free','plus')", name="ck_users_tier"),
    )

    op.create_table(
        "auth_tokens",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column(
            "user_id",
            postgresql.UUID(as_uuid=False),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("token_hash", sa.Text(), nullable=False, unique=True),
        sa.Column("purpose", sa.Text(), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("consumed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()
        ),
        sa.CheckConstraint("purpose IN ('magic_link','session')", name="ck_auth_tokens_purpose"),
    )
    op.create_index("idx_auth_tokens_user", "auth_tokens", ["user_id"])
    op.create_index("idx_auth_tokens_expires", "auth_tokens", ["expires_at"])

    op.create_table(
        "subscriptions",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column(
            "user_id",
            postgresql.UUID(as_uuid=False),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("source", sa.Text(), nullable=False),
        sa.Column("source_product_id", sa.Text(), nullable=True),
        sa.Column("service_name", sa.Text(), nullable=False),
        sa.Column("amount", sa.Numeric(12, 2), nullable=True),
        sa.Column("currency", sa.CHAR(3), nullable=True),
        sa.Column("cadence", sa.Text(), nullable=True),
        sa.Column("custom_period_days", sa.Integer(), nullable=True),
        sa.Column("status", sa.Text(), nullable=False),
        sa.Column("trial_ends_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("next_event_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("next_event_kind", sa.Text(), nullable=True),
        sa.Column("precision", sa.Text(), nullable=False, server_default="unknown"),
        sa.Column("cancel_by_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("cancel_url", sa.Text(), nullable=True),
        sa.Column("terms_raw", sa.Text(), nullable=True),
        sa.Column("terms_plain", sa.Text(), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()
        ),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint(
            "source IN ('storekit','play_billing','plaid','manual')", name="ck_subscriptions_source"
        ),
        sa.CheckConstraint(
            "cadence IN ('weekly','monthly','quarterly','semi_annual','annual','custom')",
            name="ck_subscriptions_cadence",
        ),
        sa.CheckConstraint(
            "status IN ('trial','active','cancelled','expired','unknown')",
            name="ck_subscriptions_status",
        ),
        sa.CheckConstraint(
            "next_event_kind IN ('renewal','trial_conversion','unknown')",
            name="ck_subscriptions_event_kind",
        ),
        sa.CheckConstraint(
            "precision IN ('exact','estimated','unknown')", name="ck_subscriptions_precision"
        ),
        sa.UniqueConstraint(
            "user_id", "source", "source_product_id", name="uq_subscriptions_source_product"
        ),
    )
    op.create_index(
        "idx_subs_user",
        "subscriptions",
        ["user_id"],
        postgresql_where=sa.text("deleted_at IS NULL"),
    )
    op.create_index(
        "idx_subs_next_event",
        "subscriptions",
        ["next_event_at"],
        postgresql_where=sa.text("next_event_at IS NOT NULL"),
    )

    op.create_table(
        "alerts",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column(
            "subscription_id",
            postgresql.UUID(as_uuid=False),
            sa.ForeignKey("subscriptions.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "user_id",
            postgresql.UUID(as_uuid=False),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("alert_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("lead_label", sa.Text(), nullable=False),
        sa.Column("status", sa.Text(), nullable=False, server_default="scheduled"),
        sa.Column("attempts", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("last_error", sa.Text(), nullable=True),
        sa.Column("sent_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()
        ),
        sa.CheckConstraint(
            "status IN ('scheduled','sent','failed','cancelled')", name="ck_alerts_status"
        ),
    )
    op.create_index(
        "idx_alerts_due", "alerts", ["alert_at"], postgresql_where=sa.text("status = 'scheduled'")
    )
    op.create_index("idx_alerts_user", "alerts", ["user_id"])

    op.create_table(
        "notification_tokens",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column(
            "user_id",
            postgresql.UUID(as_uuid=False),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("platform", sa.Text(), nullable=False),
        sa.Column("token", sa.Text(), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()
        ),
        sa.CheckConstraint("platform IN ('ios','android')", name="ck_notification_tokens_platform"),
        sa.UniqueConstraint("user_id", "token", name="uq_notification_tokens_user_token"),
    )

    op.create_table(
        "alert_delivery_log",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column(
            "alert_id",
            postgresql.UUID(as_uuid=False),
            sa.ForeignKey("alerts.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "attempted_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()
        ),
        sa.Column("outcome", sa.Text(), nullable=False),
        sa.Column("reason", sa.Text(), nullable=True),
        sa.CheckConstraint(
            "outcome IN ("
            "'delivered','failed_token_invalid','failed_provider',"
            "'failed_network','skipped_no_token'"
            ")",
            name="ck_alert_delivery_log_outcome",
        ),
    )


def downgrade() -> None:
    op.drop_table("alert_delivery_log")
    op.drop_table("notification_tokens")
    op.drop_index("idx_alerts_user", table_name="alerts")
    op.drop_index("idx_alerts_due", table_name="alerts")
    op.drop_table("alerts")
    op.drop_index("idx_subs_next_event", table_name="subscriptions")
    op.drop_index("idx_subs_user", table_name="subscriptions")
    op.drop_table("subscriptions")
    op.drop_index("idx_auth_tokens_expires", table_name="auth_tokens")
    op.drop_index("idx_auth_tokens_user", table_name="auth_tokens")
    op.drop_table("auth_tokens")
    op.drop_table("users")
