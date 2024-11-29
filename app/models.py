from .database import Base
from sqlalchemy import Column,Integer,String,Boolean,ForeignKey
from sqlalchemy.sql.sqltypes import TIME_TIMEZONE
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import Relationship
class Post(Base):
    __tablename__="posts1"
    id=Column(Integer,primary_key=True,nullable=False)
    title=Column(String,nullable=False)
    content=Column(String,nullable=False)
    published=Column(Boolean,server_default='True')
    created_at=Column(TIME_TIMEZONE,nullable=False,server_default=text('now()'))
    owner_id=Column(Integer,ForeignKey("user.id",ondelete="CASCADE"),nullable=False)
    owner=Relationship("User")

class User(Base):
    __tablename__="user"
    id=Column(Integer,primary_key=True,nullable=False)
    email=Column(String,unique=True,nullable=False)
    password=Column(String,nullable=False)
    created_at=Column(TIME_TIMEZONE,nullable=False,server_default=text('now()'))

    
    
