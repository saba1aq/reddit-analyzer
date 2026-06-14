"""seed subreddits

Revision ID: 03fe78568fdb
Revises: 246d6a30a544
Create Date: 2026-06-14 19:39:04.648485

"""

from typing import Sequence, Union

from alembic import op

revision: str = "03fe78568fdb"
down_revision: Union[str, Sequence[str], None] = "246d6a30a544"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

SUBREDDITS = [
    "Accounting",
    "aisolobusinesses",
    "AppIdeas",
    "appledevelopers",
    "buildinpublic",
    "devops",
    "digital_marketing",
    "digitalnomad",
    "ecommerce",
    "excel",
    "freelance",
    "indiehackers",
    "Landlord",
    "Lawyertalk",
    "marketing",
    "microsaas",
    "nocode",
    "ProductHunters",
    "productivity",
    "RealEstate",
    "SaaS",
    "saasbuild",
    "sales",
    "selfhosted",
    "shopify",
    "SideProject",
    "smallbusiness",
    "Startup_Ideas",
    "sysadmin",
    "Teachers",
    "webdev",
]


def upgrade() -> None:
    values = ", ".join(
        f"(gen_random_uuid(), '{name}', true, now(), now())" for name in SUBREDDITS
    )
    op.execute(
        "INSERT INTO subreddits (id, name, enabled, created_at, updated_at) "
        f"VALUES {values} "
        "ON CONFLICT (name) DO NOTHING"
    )


def downgrade() -> None:
    names = ", ".join(f"'{name}'" for name in SUBREDDITS)
    op.execute(f"DELETE FROM subreddits WHERE name IN ({names})")
