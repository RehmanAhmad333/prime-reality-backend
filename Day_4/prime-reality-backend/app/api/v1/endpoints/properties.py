# This module defines the API endpoints for managing properties in the real estate platform. It includes routes for listing properties with filtering and pagination, searching properties by location, fetching featured properties, getting property categories, retrieving a single property by ID, creating new properties with image uploads, updating existing properties, and deleting properties. The endpoints include validation for input data and handle permissions based on user roles (sellers and admins). The module also interacts with the database using SQLAlchemy and handles potential errors gracefully, providing clear error messages in the API responses.

from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form, Query, Path
from sqlalchemy.orm import Session
from geoalchemy2 import WKTElement
from typing import List, Optional
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.property import Property
from app.models.property_image import PropertyImage
from app.schemas.property_schema import PropertyCreate, PropertyResponse, PropertyUpdate
from app.services.s3_service import upload_image_to_s3


router = APIRouter(prefix="/properties", tags=["Properties"])


def validate_images(images: List[UploadFile]):
    """
    Validate uploaded image files. This function checks if the list of images is not empty and if each image has an allowed content type (JPEG, PNG, JPG, WEBP). If any validation fails, it raises an HTTPException with a 422 status code and a detailed error message indicating the issue with the images.
    """
    if not images or len(images) == 0:
        raise HTTPException(
            status_code=422,
            detail={
                "field": "images",
                "error": "At least one image is required."
            }
        )

    allowed_types = ["image/jpeg", "image/png", "image/jpg", "image/webp"]

    for img in images:
        if img.content_type not in allowed_types:
            raise HTTPException(
                status_code=422,
                detail={
                    "field": "images",
                    "filename": img.filename,
                    "error": "Only JPG, JPEG, PNG, and WEBP images are allowed."
                }
            )


@router.get("/", response_model=dict)
def list_properties(
    property_type: Optional[str] = Query(None, description="Filter by property type"),
    city: Optional[str] = Query(None, description="Filter by city"),
    bedrooms: Optional[int] = Query(None, ge=0, description="Bedrooms must be 0 or greater"),
    price_min: Optional[float] = Query(None, ge=0, description="Minimum price must be 0 or greater"),
    price_max: Optional[float] = Query(None, ge=0, description="Maximum price must be 0 or greater"),
    skip: int = Query(0, ge=0, description="Skip must be 0 or greater"),
    limit: int = Query(12, ge=1, le=100, description="Limit must be between 1 and 100"),
    db: Session = Depends(get_db)
):
    try:
        if price_min is not None and price_max is not None and price_min > price_max:
            raise HTTPException(
                status_code=422,
                detail={
                    "field": "price_min / price_max",
                    "error": "price_min cannot be greater than price_max."
                }
            )

        query = db.query(Property).filter(Property.status == "approved")

        if property_type:
            query = query.filter(Property.property_type == property_type)

        if city:
            query = query.filter(Property.city.ilike(f"%{city}%"))

        if bedrooms is not None:
            query = query.filter(Property.bedrooms == bedrooms)

        if price_min is not None:
            query = query.filter(Property.price >= price_min)

        if price_max is not None:
            query = query.filter(Property.price <= price_max)

        total = query.count()
        properties = query.offset(skip).limit(limit).all()

        return {
            "total": total,
            "page": skip // limit + 1,
            "pages": (total + limit - 1) // limit,
            "properties": properties
        }

    except HTTPException:
        raise

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Database error while listing properties.",
                "details": str(e)
            }
        )


 
@router.get("/search/location")
def search_by_location(
    lat: float = Query(..., ge=-90, le=90, description="Latitude must be between -90 and 90"),
    lng: float = Query(..., ge=-180, le=180, description="Longitude must be between -180 and 180"),
    radius_m: float = Query(5000, gt=0, description="Radius must be greater than 0"),
    skip: int = Query(0, ge=0, description="Skip must be 0 or greater"),
    limit: int = Query(20, ge=1, le=100, description="Limit must be between 1 and 100"),
    db: Session = Depends(get_db)
):
    try:
        point = func.ST_SetSRID(func.ST_MakePoint(lng, lat), 4326)

        query = db.query(Property).filter(
            func.ST_DWithin(Property.location, point, radius_m),
            Property.status == "approved"
        )

        total = query.count()
        properties = query.offset(skip).limit(limit).all()

        return {
            "total": total,
            "properties": properties
        }

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Database error while searching by location.",
                "details": str(e)
            }
        )


@router.get("/featured")
def get_featured(db: Session = Depends(get_db)):
    try:
        featured = db.query(Property).filter(
            Property.featured == True,
            Property.status == "approved"
        ).first()

        if not featured:
            featured = db.query(Property).filter(
                Property.status == "approved"
            ).order_by(Property.views_count.desc()).first()

        if not featured:
            raise HTTPException(
                status_code=404,
                detail="No featured or approved property found."
            )

        return featured

    except HTTPException:
        raise

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Database error while fetching featured property.",
                "details": str(e)
            }
        )


@router.get("/categories")
def get_categories(db: Session = Depends(get_db)):
    try:
        categories = ["residential", "commercial", "industrial"]
        result = []

        for cat in categories:
            count = db.query(Property).filter(
                Property.category == cat,
                Property.status == "approved"
            ).count()

            first_prop = db.query(Property).filter(
                Property.category == cat
            ).first()

            image_url = None

            if first_prop:
                first_img = db.query(PropertyImage).filter(
                    PropertyImage.property_id == first_prop.id
                ).first()

                if first_img:
                    image_url = first_img.image_url

            result.append({
                "name": cat,
                "label": {
                    "residential": "Build the Home of Your Dreams",
                    "commercial": "Shape Your Business Future",
                    "industrial": "Foundation for Industry"
                }.get(cat),
                "count": count,
                "image_url": image_url
            })

        return result

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Database error while fetching categories.",
                "details": str(e)
            }
        )


@router.get("/{property_id}", response_model=PropertyResponse)
def get_property(
    property_id: int = Path(..., gt=0, description="Property ID must be greater than 0"),
    db: Session = Depends(get_db)
):
    try:
        prop = db.query(Property).filter(Property.id == property_id).first()

        if not prop:
            raise HTTPException(
                status_code=404,
                detail={
                    "field": "property_id",
                    "error": "Property not found."
                }
            )

        prop.views_count += 1
        db.commit()
        db.refresh(prop)

        return prop

    except HTTPException:
        raise

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Database error while fetching property.",
                "details": str(e)
            }
        )


@router.post("/", response_model=PropertyResponse, status_code=201)
def create_property(
    title: str = Form(..., min_length=1, description="Title is required"),
    description: Optional[str] = Form(None),
    property_type: str = Form(..., min_length=1, description="Property type is required"),
    price: float = Form(..., gt=0, description="Price must be greater than 0"),
    bedrooms: Optional[int] = Form(None, ge=0, description="Bedrooms must be 0 or greater"),
    bathrooms: Optional[int] = Form(None, ge=0, description="Bathrooms must be 0 or greater"),
    area_sqft: Optional[int] = Form(None, gt=0, description="Area must be greater than 0"),
    location_lat: float = Form(..., ge=-90, le=90, description="Latitude must be between -90 and 90"),
    location_lng: float = Form(..., ge=-180, le=180, description="Longitude must be between -180 and 180"),
    address: str = Form(..., min_length=1, description="Address is required"),
    city: str = Form(..., min_length=1, description="City is required"),
    state: str = Form(..., min_length=1, description="State is required"),
    zip_code: str = Form(..., min_length=1, description="Zip code is required"),
    tag: Optional[str] = Form(None),
    label: Optional[str] = Form(None),
    category: Optional[str] = Form(None),
    images: List[UploadFile] = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        if current_user.role not in ["seller", "admin"]:
            raise HTTPException(
                status_code=403,
                detail={
                    "error": "Permission denied.",
                    "message": "Only sellers or admins can list properties."
                }
            )

        validate_images(images)

        point_wkt = f"POINT({location_lng} {location_lat})"

        new_property = Property(
            seller_id=current_user.id,
            title=title,
            description=description,
            property_type=property_type,
            price=price,
            bedrooms=bedrooms,
            bathrooms=bathrooms,
            area_sqft=area_sqft,
            location=WKTElement(point_wkt, srid=4326),
            address=address,
            city=city,
            state=state,
            zip_code=zip_code,
            status="pending",
            tag=tag,
            label=label,
            category=category
        )

        db.add(new_property)
        db.commit()
        db.refresh(new_property)

        for idx, img in enumerate(images):
            try:
                image_url = upload_image_to_s3(
                    img,
                    folder=f"properties/{new_property.id}"
                )

                property_image = PropertyImage(
                    property_id=new_property.id,
                    image_url=image_url,
                    is_primary=(idx == 0),
                    display_order=idx
                )

                db.add(property_image)

            except Exception as e:
                db.rollback()
                raise HTTPException(
                    status_code=500,
                    detail={
                        "field": "images",
                        "filename": img.filename,
                        "error": "Image upload failed.",
                        "details": str(e)
                    }
                )

        db.commit()
        db.refresh(new_property)

        return new_property

    except HTTPException:
        raise

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Database error while creating property.",
                "details": str(e)
            }
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Unexpected error while creating property.",
                "details": str(e)
            }
        )


@router.put("/{property_id}", response_model=PropertyResponse)
def update_property(
    property_id: int = Path(..., gt=0, description="Property ID must be greater than 0"),
    property_data: PropertyUpdate = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        if property_data is None:
            raise HTTPException(
                status_code=422,
                detail={
                    "field": "body",
                    "error": "Request body is required."
                }
            )

        prop = db.query(Property).filter(Property.id == property_id).first()

        if not prop:
            raise HTTPException(
                status_code=404,
                detail={
                    "field": "property_id",
                    "error": "Property not found."
                }
            )

        if prop.seller_id != current_user.id and current_user.role != "admin":
            raise HTTPException(
                status_code=403,
                detail={
                    "error": "Permission denied.",
                    "message": "Not authorized to update this property."
                }
            )

        for key, value in property_data.dict(exclude_unset=True).items():
            setattr(prop, key, value)

        db.commit()
        db.refresh(prop)

        return prop

    except HTTPException:
        raise

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Database error while updating property.",
                "details": str(e)
            }
        )


@router.delete("/{property_id}")
def delete_property(
    property_id: int = Path(..., gt=0, description="Property ID must be greater than 0"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        prop = db.query(Property).filter(Property.id == property_id).first()

        if not prop:
            raise HTTPException(
                status_code=404,
                detail={
                    "field": "property_id",
                    "error": "Property not found."
                }
            )

        if prop.seller_id != current_user.id and current_user.role != "admin":
            raise HTTPException(
                status_code=403,
                detail={
                    "error": "Permission denied.",
                    "message": "Not authorized to delete this property."
                }
            )

        db.delete(prop)
        db.commit()

        return {
            "message": "Property deleted successfully."
        }

    except HTTPException:
        raise

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Database error while deleting property.",
                "details": str(e)
            }
        )