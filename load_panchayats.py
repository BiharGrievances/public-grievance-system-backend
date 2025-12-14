import json
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.panchayat import Panchayat

def load_panchayats():
    db: Session = SessionLocal()

    # Load JSON file
    with open("app/data/panchayats.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    count = 0

    # Insert each panchayat
    for item in data:
        p = Panchayat(
            id=item["id"],
            district_id=item["district_id"],
            block=item["block"],
            name=item["name"]
        )
        db.merge(p)  # safe insert/update
        count += 1

    db.commit()
    db.close()

    print(f"Loaded {count} panchayats successfully!")

if __name__ == "__main__":
    load_panchayats()
