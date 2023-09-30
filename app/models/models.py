from sqlalchemy import MetaData, Integer, String, TIMESTAMP, ForeignKey, Table, Column, Boolean, Text, Enum, CheckConstraint
from datetime import datetime


metadata = MetaData()

user_statuses = ('active', 'inactive')

user = Table(
    'user',
    metadata,
    Column('user_id', Integer, primary_key=True),
    Column('user_email', String, nullable=False),
    Column('user_firstname', String, nullable=False),
    Column('user_lastname', String, nullable=True),
    Column('user_status', String, CheckConstraint(f"user_status IN {user_statuses}", name='user_status'),
            default='inactive'),
    Column('user_city', String, nullable=True),
    Column('user_phone', String(15), nullable=True),
    Column('user_links', Text, nullable=True),
    Column('user_avatar', String, nullable=True),
    Column('hashed_password',  String, nullable=False),
    Column('is_superuser', Boolean, default=False),
    Column('created_at', TIMESTAMP, default=datetime.utcnow),
    Column('updated_at', TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow),


)

