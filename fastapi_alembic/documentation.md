# Alembic Learning Documentation

This document serves as a guide and reference for using Alembic for database migrations in a FastAPI project, based on the hands-on exercises conducted in this repository.

---

## 1. Getting Started

### Installation
Ensure `alembic` and `python-decouple` (for environment variables) are installed:
```bash
uv add alembic python-decouple
```

### Initialization
Initialize the Alembic environment in your project:
```bash
# This creates an 'alembic' directory and an 'alembic.ini' file
alembic init alembic
```

---

## 2. Configuration (The "Dynamic" Approach)

To keep credentials secure, we load the database URL from a `.env` file instead of hardcoding it.

### `alembic.ini`
Set the `sqlalchemy.url` to a placeholder to use interpolation or just leave it as a reference point.
```ini
sqlalchemy.url = %(SQLALCHEMY_DATABASE_URL)s
```

### `env.py`
This is the heart of Alembic's runtime. We modify it to load the `.env` variable using `decouple`.

```python
from decouple import config
from alembic import context

# Load the database URL from .env
SQLALCHEMY_DATABASE_URL = config("SQLALCHEMY_DATABASE_URL")

# Get the alembic config object
config_obj = context.config

# Dynamically set the sqlalchemy.url
config_obj.set_main_option("sqlalchemy.url", SQLALCHEMY_DATABASE_URL)
```

---

## 3. Managing Migrations

### Creating a Revision
A "revision" is a script representing a change to the database.
```bash
alembic revision -m "description of changes"
```

### Writing the Migration (By Hand)
Inside the generated file in `alembic/versions/`, you define two functions:
- `upgrade()`: Logic to apply the changes.
- `downgrade()`: Logic to undo the changes.

Example:
```python
def upgrade():
    op.create_table(
        'employee',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
    )

def downgrade():
    op.drop_table('employee')
```

---

## 4. Key Commands

| Command | Description |
| :--- | :--- |
| `alembic upgrade head` | Apply all pending migrations to the latest version. |
| `alembic downgrade -1` | Rollback the last migration. |
| `alembic current` | Show the current revision level of the database. |
| `alembic history` | Show the list of all migrations in chronological order. |
| `alembic show <revision>` | Show details about a specific revision. |

---

## 5. Lessons Learned & Tips

1. **Transactional DDL**: Alembic wraps migrations in transactions (on supported DBs like Postgres), meaning if an upgrade fails halfway, it rolls back automatically.
2. **Deterministic Versions**: Every migration has a unique hash (e.g., `2860183cdf8c`). Use these to target specific versions.
3. **Always Write Downgrades**: A migration is only complete if it can be safely undone.
4. **Order Matters**: Alembic uses a linked list (Parent -> Child). Ensure the `down_revision` in your files correctly points to the previous state.

---
*Created as part of the FastAPI + Alembic Hands-on Tutorial.*
