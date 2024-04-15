from sqlalchemy import Column, Boolean, DateTime
from sqlalchemy.sql import func
from db.base import Base


##############################
# BLOCK WITH DATABASE MODELS #
##############################


class MaintenanceModel(Base):

    __abstract__ = True

    is_active = Column(Boolean(), default=True)
    is_deleted = Column(Boolean(), default=False)
    time_create = Column(DateTime(timezone=True), default=func.now())
    time_update = Column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )
