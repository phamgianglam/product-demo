from uuid import UUID, uuid4
from datetime import datetime

from sqlalchemy import Column, Index, func
from sqlalchemy.sql.sqltypes import DateTime, Integer, String
from sqlalchemy.dialects.postgresql import UUID as sqlUUID
from sqlalchemy.orm import declarative_base

BaseModel = declarative_base()


class Product(BaseModel):
    __tablename__ = "product"
    id_: UUID = Column(
        "id", sqlUUID(as_uuid=True), default=uuid4, primary_key=True
    )
    name: str = Column(String, nullable=False, unique=True)
    description: str = Column(String, nullable=False, unique=False)
    price: int = Column(Integer, nullable=False)
    date: datetime = Column(
        DateTime(timezone=True), nullable=False,
    )

    __table_args__ = (Index("index_name", func.lower(name)),)
