from sqlalchemy import Column, Integer, String, Float 
from db import Base 

class Subscription(Base):
    __tablename__ = "subscriptions"
    id = Column(Integer, primary_key = True, index = True)
    name = Column(String, index = True)
    amount = Column(Float)
    cycle = Column(String)
    