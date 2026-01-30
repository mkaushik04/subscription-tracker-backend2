from fastapi import FastAPI 
from pydantic import BaseModel 
from sqlalchemy.orm import Session 
from fastapi import Depends 
from db import get_db 
from models import Subscription 
from datetime import date 
from typing import Optional 
import requests 

app = FastAPI()


#What should a new subscription have 
class SubscriptionCreate(BaseModel):
    name: str 
    amount: float
    billing_day: int
    currency: str = "AUD"
    
class SubscriptionUpdate(BaseModel):
    name: Optional[str] = None
    amount: Optional[float] = None 
    billing_day: Optional[int] = None 
    currency: Optional[str] = None
    
def get_usd_to_aud_rate():
    response = requests.get(
        "https://api.exchangerate.host/latest", 
        params = {"base": "USD", "symbols": "AUD"},
        timeout = 5
    )
    data = response.json()
    return data["rates"]["AUD"]

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
        billing_day = new_sub.billing_day,
        currency = new_sub.currency 
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

@app.put("/subscriptions/{subscriptions_id}")
def update_subscription(
    subscription_id: int, 
    updates: SubscriptionUpdate, 
    db: Session = Depends(get_db), 
):
    subscription = (
        db.query(Subscription)
        .filter(Subscription.id == subscription_id)
        .first()
    )
    
    if subscription is None:
        return {"error": "Subscription not found"}
    
    if updates.name is not None:
        subscription.name = updates.name
    if updates.amount is not None:
        subscription.amount = updates.amount
    if updates.billing_day is not None:
        subscription.billing_day = updates.billing_day
    if updates.currency is not None:
        subscription.currency = updates.currency 
        
    db.commit()
    db.refresh(subscription)
    return subscription