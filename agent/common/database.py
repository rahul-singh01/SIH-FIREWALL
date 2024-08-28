from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from .config import Config
from .logger import get_logger

logger = get_logger(__name__)

class Database:
    def __init__(self):
        # Get the database URL from the config
        db_url = Config.DB_URL
        if not db_url:
            raise ValueError("Database URL is not configured.")
        
        # Create an SQLAlchemy engine
        self.engine = create_engine(db_url, pool_size=10, max_overflow=20, echo=True)
        
        # Create a scoped session to manage sessions across threads
        self.Session = scoped_session(sessionmaker(bind=self.engine))
    
    def get_session(self):
        try:
            # Return a session from the scoped session
            return self.Session()
        except Exception as e:
            logger.error(f"Error creating session: {str(e)}")
            raise

    def close(self):
        # Close all sessions and dispose the engine
        self.Session.remove()
        self.engine.dispose()
        logger.info("Database connection closed.")

# Example usage:
# db = Database()
# session = db.get_session()
# session.query(MyModel).all()
# db.close()
