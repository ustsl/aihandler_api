# AI HANDLER


# Path for start:
- alembic init migrations
- correct alembic.ini:
    - sqlalchemy.url = postgresql://login:pass@0.0.0.0:5432/db
- correct migrations.env:
    - from db.base import Base
    - target_metadata = Base.metadata
- alembic revision --autogenerate -m "comment"
- alembic upgrade heads
- uvicorn main:app --reload