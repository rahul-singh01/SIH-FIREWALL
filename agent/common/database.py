import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
from common.logger import logger
import datetime

class Config:
    DATABASE_NAME = 'firewall'
    DATABASE_USER = 'root'
    DATABASE_PASSWORD = 'root'
    DATABASE_HOST = 'localhost'
    DATABASE_PORT = '5432'

class Database:
    def __init__(self, config):
        logger.info("Initializing database connection with psycopg2.")
        self.config = config
        self.connection = None
        self.cursor = None
        self.connect()
        self.create_tables()

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                dbname=self.config.DATABASE_NAME,
                user=self.config.DATABASE_USER,
                password=self.config.DATABASE_PASSWORD,
                host=self.config.DATABASE_HOST,
                port=self.config.DATABASE_PORT
            )
            self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)
            logger.info("Successfully connected to the database.")
        except psycopg2.Error as e:
            logger.error(f"Error connecting to the database: {e}")
            raise

    def create_tables(self):
        try:
            # Create logs table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS api_log (
                    id SERIAL PRIMARY KEY,
                    level VARCHAR(50) NOT NULL,
                    message TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Create alerts table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS api_alert (
                    id SERIAL PRIMARY KEY,
                    level VARCHAR(50) NOT NULL,
                    message TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Create policies table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS api_policy (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    description TEXT,
                    action VARCHAR(50) NOT NULL,
                    source_ip VARCHAR(50) NOT NULL,
                    destination_ip VARCHAR(50) NOT NULL,
                    port INTEGER NOT NULL,
                    is_active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Create applications table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS api_application (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    description TEXT,
                    allowed_ports INTEGER[],
                    is_active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            self.connection.commit()
            logger.info("Database tables created successfully.")
        except psycopg2.Error as e:
            logger.error(f"Error creating tables: {e}")
            self.connection.rollback()
            raise

    # import datetime

    def add_log(self, level, message):
        try:
            # Get the current timestamp in Python
            created_at = datetime.datetime.now()
            self.cursor.execute(
                "INSERT INTO api_log (level, message, created_at) VALUES (%s, %s, %s)",
                (level, message, created_at)
            )
            self.connection.commit()
            logger.debug(f"Log added: {level} - {message}")
        except psycopg2.Error as e:
            logger.error(f"Error adding log: {e}")
            self.connection.rollback()



    def get_logs(self, limit=100):
        try:
            self.cursor.execute("SELECT * FROM api_log ORDER BY created_at DESC LIMIT %s", (limit,))
            return self.cursor.fetchall()
        except psycopg2.Error as e:
            logger.error(f"Error fetching logs: {e}")
            return []

    def add_alert(self, level, message):
        try:
            timestamp = datetime.datetime.now()
            self.cursor.execute(
                "INSERT INTO api_alert (level, message, timestamp , resolved) VALUES (%s, %s, %s, %s)",
                (level, message , timestamp , False)
            )
            self.connection.commit()
            logger.debug(f"Alert added: {level} - {message}")
        except psycopg2.Error as e:
            logger.error(f"Error adding alert: {e}")
            self.connection.rollback()

    def get_alerts(self, limit=100):
        try:
            self.cursor.execute("SELECT * FROM api_alert ORDER BY created_at DESC LIMIT %s", (limit,))
            return self.cursor.fetchall()
        except psycopg2.Error as e:
            logger.error(f"Error fetching alerts: {e}")
            return []

    def get_policies(self):
        try:
            self.cursor.execute("SELECT * FROM api_policy WHERE is_active = TRUE ORDER BY id")
            return self.cursor.fetchall()
        except psycopg2.Error as e:
            logger.error(f"Error fetching policies: {e}")
            return []

    def add_policy(self, name, description, action, source_ip, destination_ip, port):
        try:
            self.cursor.execute(
                """
                INSERT INTO api_policy (name, description, action, source_ip, destination_ip, port)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (name, description, action, source_ip, destination_ip, port)
            )
            self.connection.commit()
            logger.info(f"Policy added: {name}")
        except psycopg2.Error as e:
            logger.error(f"Error adding policy: {e}")
            self.connection.rollback()

    def update_policy(self, policy_id, **kwargs):
        try:
            update_fields = ', '.join([f"{k} = %s" for k in kwargs.keys()])
            query = f"UPDATE api_policy SET {update_fields}, updated_at = CURRENT_TIMESTAMP WHERE id = %s"
            self.cursor.execute(query, list(kwargs.values()) + [policy_id])
            self.connection.commit()
            logger.info(f"Policy updated: ID {policy_id}")
        except psycopg2.Error as e:
            logger.error(f"Error updating policy: {e}")
            self.connection.rollback()

    def delete_policy(self, policy_id):
        try:
            self.cursor.execute("DELETE FROM api_policy WHERE id = %s", (policy_id,))
            self.connection.commit()
            logger.info(f"Policy deleted: ID {policy_id}")
        except psycopg2.Error as e:
            logger.error(f"Error deleting policy: {e}")
            self.connection.rollback()

    def get_applications(self):
        try:
            self.cursor.execute("SELECT * FROM api_application WHERE is_active = TRUE ORDER BY id")
            return self.cursor.fetchall()
        except psycopg2.Error as e:
            logger.error(f"Error fetching applications: {e}")
            return []

    def add_application(self, name, description, allowed_ports):
        try:
            self.cursor.execute(
                """
                INSERT INTO api_application (name, description, allowed_ports)
                VALUES (%s, %s, %s)
                """,
                (name, description, allowed_ports)
            )
            self.connection.commit()
            logger.info(f"Application added: {name}")
        except psycopg2.Error as e:
            logger.error(f"Error adding application: {e}")
            self.connection.rollback()

    def update_application(self, app_id, **kwargs):
        try:
            update_fields = ', '.join([f"{k} = %s" for k in kwargs.keys()])
            query = f"UPDATE api_application SET {update_fields}, updated_at = CURRENT_TIMESTAMP WHERE id = %s"
            self.cursor.execute(query, list(kwargs.values()) + [app_id])
            self.connection.commit()
            logger.info(f"Application updated: ID {app_id}")
        except psycopg2.Error as e:
            logger.error(f"Error updating application: {e}")
            self.connection.rollback()

    def delete_application(self, app_id):
        try:
            self.cursor.execute("DELETE FROM api_application WHERE id = %s", (app_id,))
            self.connection.commit()
            logger.info(f"Application deleted: ID {app_id}")
        except psycopg2.Error as e:
            logger.error(f"Error deleting application: {e}")
            self.connection.rollback()

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            logger.info("Database connection closed.")