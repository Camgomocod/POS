from models.base import get_db
from models.order import Order
from sqlalchemy import func
from datetime import datetime, timedelta

class ReportController:
    def __init__(self):
        self.db = get_db()
    
    def get_daily_sales(self, date=None):
        if not date:
            date = datetime.now().date()
        
        start_date = datetime.combine(date, datetime.min.time())
        end_date = datetime.combine(date, datetime.max.time())
        
        return self.db.query(func.sum(Order.total)).filter(
            Order.created_at.between(start_date, end_date)
        ).scalar() or 0
    
    def get_recent_orders(self, limit=10):
        return self.db.query(Order).order_by(Order.created_at.desc()).limit(limit).all()
