from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"

engine = create_engine(DATABASE_URL)

def get_application_status(application_id):
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT status FROM applications WHERE application_id = :id"),
            {"id": application_id}
        ).fetchone()

        if result:
            return result[0]
        return None
