"""drop mismatched column

Revision ID: 828215855bd1
Revises: f3ade97fa117
Create Date: 2026-03-05 04:46:54.755420

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "828215855bd1"
down_revision: Union[str, Sequence[str], None] = "f3ade97fa117"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_column("git_repositories", "created_at")
    op.drop_column("git_repositories", "updated_at")


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column(
        "git_repositories", sa.Column("created_at", sa.String(), nullable=True)
    )
    op.add_column(
        "git_repositories", sa.Column("updated_at", sa.String(), nullable=True)
    )
