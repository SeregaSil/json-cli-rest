import enum
from sqlalchemy import Column, String, UUID, Enum, JSON
from rest.database import Base
from uuid import uuid4

class Status(enum.Enum):
    NEW = "NEW"
    INSTALLING = "INSTALLING"
    RUNNING = "RUNNING"


class Apps(Base):
    __tablename__ = "apps"

    UUID = Column(UUID, primary_key=True, unique=True, nullable=False, default=uuid4())
    kind = Column(String(32), nullable=False)
    name = Column(String(128), nullable=False)
    version = Column(String, nullable=False)
    description = Column(String(4096), nullable=False)
    state = Column(Enum(Status), default=Status.NEW)
    json = Column(JSON)