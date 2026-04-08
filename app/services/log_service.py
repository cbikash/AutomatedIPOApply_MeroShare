from fastapi import Session
from app.models.log import Log as LogModel
from datetime import datetime


class Log:
    def __init__(self, db: Session):
        self.db = db
    
    def log_action(self, user_id, message, status, response_data):
        log_entry = LogModel(
            message= message,
            level= status,
            timestamp= datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            user_id= user_id
        )

        try:
            self.db.add(log_entry)
            self.db.commit()
            self.db.refresh(log_entry)
        except Exception as e:
            self.db.rollback()
            print(f"Error logging action: {e}")

        return log_entry
