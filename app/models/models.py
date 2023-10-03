from sqlalchemy import Integer, String, TIMESTAMP, ForeignKey, Table, Column, Boolean, Text, Enum, CheckConstraint
from datetime import datetime
from sqlalchemy.orm import DeclarativeBase

user_statuses = ('active', 'inactive')

class Base(DeclarativeBase):
    pass

class UserModel(Base):
    __tablename__ = 'user'

    user_id = Column(Integer, primary_key=True)
    user_email = Column(String, nullable=False)
    user_firstname = Column(String, nullable=False)
    user_lastname = Column(String, nullable=True)
    user_status = Column(String, CheckConstraint(f"user_status IN {user_statuses}", name='user_status'),
            default='inactive')
    user_city = Column(String, nullable=True)
    user_phone = Column(String(15), nullable=True)
    user_links = Column(Text, nullable=True)
    user_avatar = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)


