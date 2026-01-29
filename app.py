from fastapi import FastAPI 
from pydantic import BaseModel 
from sqlalchemy.orm import Session 
from fastapi import Depends 
from db import get_db 
from models import Subscription 

app = FastAPI()

#Temp 
# subscriptions = [
#     {"id": 1, "name": "YouTube", "amount": 22.99, "cycle": "monthly"},
#     {"id": 2, "name": "Google AI", "amount": 32.99, "cycle": "monthly"},
# ]

#What should a new subscription have 
class SubscriptionCreate(BaseModel):
    name: str
    amount: float
    cycle: str 

@app.get("/")
def home():
    return {"message": "My Subscription tracker is running"}

@app.get("/subscriptions")
def get_subscriptions(db: Session = Depends(get_db)):
    return db.query(Subscription).all()

@app.post("/subscriptions")
def create_subscription(new_sub: SubscriptionCreate, db: Session = Depends(get_db)):
    
    subscription = Subscription(
        name = new_sub.name,
        amount = new_sub.amount,
        cycle = new_sub.cycle
    )
    
    db.add(subscription)
    db.commit()
    db.refresh(subscription)
    
    return subscription
    # new_id = subscriptions[-1]["id"] + 1 if subscriptions else 1
    
    # sub_dict = {
    #     "id": new_id, 
    #     "name": new_sub.name,
    #     "amount": new_sub.amount,
    #     "cycle": new_sub.cycle,
    # }
    
    # subscriptions.append(sub_dict)
    # return sub_dict

#Filter endpoint 
@app.get("/subscriptions/filter")
def filter_subscriptions(cycle: str, db:Session = Depends(get_db)):
    return db.query(Subscription).filter(Subscription.cycle == cycle).all()
    # results = []
    
    # for sub in subscriptions:
    #     if sub["cycle"] == cycle:
    #         results.append(sub)
            
    # return results