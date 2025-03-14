from contextlib import contextmanager
from sqlalchemy import text
from app.models import db
from typing import Optional

@contextmanager
def user_context(user_id: Optional[int] = None):
    """Context manager to set user_id for row-level security.
    
    Args:
        user_id: The ID of the user to set in the context. If None, operates in system context
                with full access to all rows.
    
    Usage:
        # For user operations:
        with user_context(user_id=123):
            # Operations here will only see user 123's data
            
        # For system operations:
        with user_context():  # or with user_context(None)
            # Operations here will see all data
    """
    previous_user_id = None
    try:
        # Store previous user_id if any
        with db.session.connection() as conn:
            result = conn.execute(text("SELECT current_setting('app.current_user_id', TRUE)"))
            previous_user_id = result.scalar()
        
        # Set new user_id (None is valid for system operations)
        with db.session.connection() as conn:
            conn.execute(text("SELECT set_user_id(:user_id)"), {"user_id": user_id})
            yield
    finally:
        # Restore previous user_id if any, otherwise clear it
        with db.session.connection() as conn:
            conn.execute(text("SELECT set_user_id(:user_id)"), 
                       {"user_id": previous_user_id if previous_user_id != '' else None}) 