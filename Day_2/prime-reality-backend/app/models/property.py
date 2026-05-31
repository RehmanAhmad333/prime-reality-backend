# This module defines the Property model for the Prime Reality backend application. The Property model is used to store information about properties listed on the platform, including details such as the seller ID, title, description, property type, price, number of bedrooms and bathrooms, area in square feet, location (using geographic coordinates), address, city, state, zip code, status of the listing (pending, approved, rejected), whether the property is featured, and the number of views. It also includes additional fields for tags, labels, categories, and timestamps for when the property was created and last updated. This model serves as the core representation of a property listing in the application and is essential for managing and displaying properties to users.

from sqlalchemy import Column, Integer, String, Numeric, Boolean, TIMESTAMP, ForeignKey, func, BigInteger
from geoalchemy2 import Geography
from app.core.database import Base

class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(String)
    property_type = Column(String(50))  # apartment/villa/land/commercial
    price = Column(Numeric(12,2), nullable=False)
    bedrooms = Column(Integer)
    bathrooms = Column(Integer)
    area_sqft = Column(Integer)
    location = Column(Geography(geometry_type='POINT', srid=4326))
    address = Column(String)
    city = Column(String(100))
    state = Column(String(100))
    zip_code = Column(String(20))
    status = Column(String(50), default="pending")  # pending, approved, rejected
    featured = Column(Boolean, default=False)
    views_count = Column(BigInteger, default=0)
    # Extra from design analysis
    tag = Column(String(100))          # "LIVE THE CITY LIFE"
    label = Column(String(255))        # "Build the Home of Your Dreams"
    category = Column(String(50))      # residential / commercial / industrial
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())