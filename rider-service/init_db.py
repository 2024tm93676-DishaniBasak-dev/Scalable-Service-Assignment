# init_db.py
# Gunicorn bypasses __main__, so DB creation and seeding must run before gunicorn starts. 
# This script is idempotent: it checks email to avoid duplicate rows.

import time, os, csv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from app import app, db, Rider  # imports models and db from app

DB_USER = os.getenv('DB_USER','root')
DB_PASS = os.getenv('DB_PASS','Dishani99')
DB_HOST = os.getenv('DB_HOST','rider-db')
DB_NAME = os.getenv('DB_NAME','riders_db')
DB_PORT = int(os.getenv('DB_PORT', 3306))

DATABASE_URI = f'mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
engine = create_engine(DATABASE_URI)

def wait_for_db(retries=20, delay=3):
    for i in range(retries):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("DB available")
            return
        except OperationalError:
            print(f"DB not ready, retry {i+1}/{retries}")
            time.sleep(delay)
    raise Exception("DB not available")

def create_tables():
    print("Creating tables...")
    with app.app_context():
        db.create_all()
    print("Tables created")

def seed_from_csv():
    csv_path = '/app/rhfd_riders.csv'  # mounted by docker-compose
    if not os.path.exists(csv_path):
        print("CSV not found:", csv_path)
        return
    print("Seeding from CSV:", csv_path)
    with app.app_context():
        with open(csv_path, newline='') as f:
            reader = csv.DictReader(f)
            added = 0
            for row in reader:
                email = (row.get('email') or row.get('Email') or '').strip()
                name = (row.get('name') or row.get('Name') or '').strip()
                phone = (row.get('phone') or row.get('Phone') or '').strip()
                if not email or not name:
                    continue
                if Rider.query.filter_by(email=email).first():
                    continue
                r = Rider(name=name, email=email, phone=phone or None)
                db.session.add(r)
                added += 1
            db.session.commit()
            print(f"Inserted {added} riders")

def run_sql_if_exists():
    sql_path = '/app/init_db.sql'
    if os.path.exists(sql_path):
        print("Running init_db.sql")
        with engine.connect() as conn:
            with open(sql_path) as f:
                sql_script = f.read()
                commands = [cmd.strip() for cmd in sql_script.split(';') if cmd.strip() and not cmd.strip().startswith('--')]
                for cmd in commands:
                    try:
                        conn.execute(text(cmd))
                    except Exception as e:
                        print(f"Skipping command due to error: {e}")
        print("init_db.sql executed successfully")
    else:
        print("init_db.sql not found, skipping.")
        
          
if __name__ == "__main__":
    wait_for_db()
    create_tables()
    run_sql_if_exists()
    seed_from_csv()
    print("DB init complete")
