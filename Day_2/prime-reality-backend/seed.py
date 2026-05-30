import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base
from app.models.platform_stats import PlatformStat
from app.models.user import User
from app.models.property import Property
from geoalchemy2 import WKTElement
from passlib.context import CryptContext

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/primerealty"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

# Insert platform stats
stats = [
    PlatformStat(stat_key="total_network_users", stat_value=12_000_000),
    PlatformStat(stat_key="visit_multiplier", stat_value=12),
    PlatformStat(stat_key="rural_listings", stat_value=1_000_000),
    PlatformStat(stat_key="total_properties", stat_value=0),
    PlatformStat(stat_key="total_users", stat_value=0),
]
for stat in stats:
    if not db.query(PlatformStat).filter(PlatformStat.stat_key == stat.stat_key).first():
        db.add(stat)
db.commit()

# Create a test admin user (password = "admin123")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
admin = User(
    email="admin@primerealty.com",
    password_hash=pwd_context.hash("admin123"),
    full_name="Admin User",
    role="admin",
    is_active=True
)
if not db.query(User).filter(User.email == admin.email).first():
    db.add(admin)
    db.commit()

# Create a sample property (featured)
sample_property = Property(
    seller_id=admin.id,
    title="Luxury Villa in Beverly Hills",
    description="Stunning modern villa with ocean views.",
    property_type="villa",
    price=2300.00,  # as shown in design: "$2,300.00"
    bedrooms=4,
    bathrooms=5,
    area_sqft=4500,
    location=WKTElement('POINT(-118.406 34.056)', srid=4326),  # Beverly Hills coordinates
    address="123 Rodeo Drive",
    city="Beverly Hills",
    state="CA",
    zip_code="90210",
    status="approved",
    featured=True,
    tag="LIVE THE CITY LIFE",
    label="Build the Home of Your Dreams",
    category="residential"
)
db.add(sample_property)
db.commit()

print("Seed data inserted successfully.")