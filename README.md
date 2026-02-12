# AI HANDLER

## Local PostgreSQL (manual control)

- Start DB: `sudo pg_ctlcluster 16 main start`
- Stop DB: `sudo pg_ctlcluster 16 main stop`
- Check DB status: `pg_isready -h 0.0.0.0 -p 5432`
- Apply migrations (create/update tables): `.venv/bin/alembic upgrade heads`

`postgresql` autostart is not required. Do not run `systemctl enable postgresql`.

# Path for start:
- alembic init migrations
- correct alembic.ini:
    - sqlalchemy.url = postgresql://login:pass@0.0.0.0:5432/db
- correct migrations.env:
    - from db.base import Base
    - target_metadata = Base.metadata
- alembic revision --autogenerate -m "comment"
- alembic upgrade heads
- uvicorn src.main:app --reload
