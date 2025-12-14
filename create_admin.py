from app.database import SessionLocal
from app.models.admin_user import AdminUser
from app.auth_middleware import hash_password

db = SessionLocal()

username = "Ashu"
password = "Ashu"

existing = db.query(AdminUser).filter(AdminUser.username == username).first()

if not existing:
    admin = AdminUser(
        username=username,
        password_hash=hash_password(password)
    )
    db.add(admin)
    db.commit()
    print("Admin created")
else:
    print("Admin already exists")

db.close()
