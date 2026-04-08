from fastapi import Session, Depends
from app.models.sharelog import Sharelog
from app.core.database import get_db
from datetime import datetime


class ShareLogService:

    def __init__(self, db: Session):
        self.db = db

    
    def log_share_action(self, user_id, meroshare_id, share_name, share_code, message, status, response_data):
        sharelog = Sharelog(
            user_id= user_id,
            meroshare_id= meroshare_id,
            share_name= share_name,
            share_code= share_code,
            application_date= datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            message= message,
            status= status,
            applied_by= user_id,
            response_data= response_data
        )
        try:
            self.db.add(sharelog)
            self.db.commit()
            self.db.refresh(sharelog)
        except Exception as e:
            self.db.rollback()
            print(f"Error logging share action: {e}")

        return sharelog
    
    def get_sharelogs_by_user(self, user_id):
        return self.db.query(Sharelog).filter(Sharelog.user_id == user_id).all()
    
    def get_sharelogs_by_meroshare(self, meroshare_id):
        return self.db.query(Sharelog).filter(Sharelog.meroshare_id == meroshare_id).all()