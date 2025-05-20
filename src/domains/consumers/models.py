import uuid
from datetime import datetime
from sqlalchemy import Column, String, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.infrastructure.database import Base


class Consumer(Base):
    __tablename__ = "Consumers"

    id = Column(
        UUID(),
        primary_key=True,
        index=True,
        default=uuid.uuid4
    )
    name = Column(
        String,
        name="name",
        index=True
    )
    email = Column(
        String,
        unique=True,
        index=True
    )
    favorites = relationship(
        "Favorite",
        back_populates="consumer",
        cascade="all, delete-orphan",
        lazy="selectin"
    )


class Favorite(Base):
    __tablename__ = "Favorites"

    id = Column(
        UUID(),
        primary_key=True,
        default=uuid.uuid4
    )
    consumer_id = Column(
        UUID(),
        ForeignKey('Consumers.id', ondelete='CASCADE'),
        nullable=False
    )
    product_id = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    consumer = relationship("Consumer", back_populates="favorites")

    __table_args__ = (
        UniqueConstraint('consumer_id', 'product_id', name='_consumer_product_uc'),
    )
