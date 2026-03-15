import uuid
from sqlalchemy import Column, String, Boolean, Text, TIMESTAMP, text
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True), 
        primary_key=True, 
        server_default=text("gen_random_uuid()"), 
        default=uuid.uuid4
    )
    fullname = Column(Text, nullable=False)
    email = Column(Text, nullable=False, unique=True)
    password = Column(Text, nullable=False)
    profile_image_url = Column(Text, nullable=True)
    is_verified = Column(Boolean, server_default=text("false"), nullable=False)
    phone_number = Column(Text, nullable=False)
    role = Column(Text, server_default=text("'USER'"), nullable=False)
    
    # Timestamp without time zone sesuai SQL kamu
    created_at = Column(TIMESTAMP, server_default=text("now()"))
    updated_at = Column(TIMESTAMP, onupdate=text("now()"))
    
    # Deleted at dengan time zone sesuai SQL kamu
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)

    def __repr__(self):
        return f"<User email={self.email} role={self.role}>"