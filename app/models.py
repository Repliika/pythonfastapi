from database import Base 
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

#create model from Base class in sqlalchemy allowing us to inherit table making methods

class Music(Base):
    __tablename__ = 'Music_Posts'

    id = Column(Integer, primary_key=True, nullable=False)
    song = Column(String, nullable=False)
    artist = Column(String, nullable=False)
    genre = Column(String, nullable=False)
    opinion = Column(Text, nullable =True)
    spotify = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    #grab id from user table. cascade mode for on delete, and must be filled in
    user_id = Column(Integer, ForeignKey(
        "users.id" , ondelete="CASCADE"), nullable=False)
    
    #when we return a post it will create an owner property and fetch the user based on user_id
    owner = relationship("User")



class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    


class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("Music_Posts.id", ondelete="CASCADE"), primary_key=True)