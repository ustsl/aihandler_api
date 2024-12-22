from sqlalchemy import Boolean, Column, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

##############################
# BLOCK WITH DATABASE MODELS #
##############################


class MaintenanceModel(Base):

    __abstract__ = True

    is_active = Column(Boolean(), default=True, nullable=False)
    is_deleted = Column(Boolean(), default=False, nullable=False)


class TimeModel(Base):

    __abstract__ = True

    time_create = Column(DateTime(timezone=True), default=func.now())
    time_update = Column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )
