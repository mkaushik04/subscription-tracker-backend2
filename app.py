from fastapi import FastAPI 
from pydantic import BaseModel 
from sqlalchemy.orm import Session 
from fastapi import Depends 
from db import get_db 
from models import Subscription 
from datetime import date 

app = FastAPI()


#What should a new subscription have 
class SubscriptionCreate(BaseModel):
    name: str
    amount: float
    billing_day: int 

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
        billing_day = new_sub.billing_day
    )
    
    db.add(subscription)
    db.commit()
    db.refresh(subscription)
    
    return subscription


#Filter endpoint 

@app.get("/subscriptions/due")
def subscriptions_due(db: Session = Depends(get_db)):
    today_day = date.today().day
    
    return(
        db.query(Subscription)
        .filter(Subscription.billing_day > today_day)
        .all()
    )
@app.delete("/subscriptions/{subscription_id}")
def delete_subscription(subscription_id: int, db: Session = Depends(get_db)):
    subscription = db.query(Subscription).filter(
        Subscription.id == subscription_id
    ).first()
    
    if subscription is None:
        return {"error": "Subscription not found"}
    
    db.delete(subscription)
    db.commit()
    
    return {"message": f"Subscription {subscription_id} deleted successfully"}