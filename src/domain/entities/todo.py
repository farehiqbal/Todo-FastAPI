from datetime import datetime
from typing import Optional

class Todo:
    def __init__(self, id: str, user_id: str, title: str, description: str = "", completed: bool = False, created_at: Optional[datetime] = None, completed_at: Optional[datetime] = None):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.description = description
        self.completed = completed
        self.created_at = created_at or datetime.utcnow()
        self.completed_at = completed_at

    def mark_complete(self):
        if self.completed:
            raise ValueError("Todo is already completed.")

        self.completed = True
        self.completed_at = datetime.utcnow()

    def update_title(self, new_title: str):
        if self.completed:
            raise ValueError("Cannot update title of a completed todo.")
        
        if not new_title.strip():
            raise ValueError("Title cannot be empty.")

        self.title = new_title