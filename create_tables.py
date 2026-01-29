from db import engine 
from db import Base 
import models

Base.metadata.create_all(bind=engine)

print("Tables created")
