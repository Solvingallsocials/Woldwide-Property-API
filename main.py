from fastapi import FastAPI, Query, HTTPException
from typing import List, Optional
from pydantic import BaseModel

app = FastAPI()

class Property(BaseModel):
    id: int
    country: str
    city: str
    type: str
    price: float
    size: float
    bedrooms: int
    bathrooms: int
    address: str
    description: str
    photos: List[str]

# Sample in-memory "database"
properties_db = [
    Property(
        id=1,
        country="USA",
        city="New York",
        type="apartment",
        price=950000,
        size=850,
        bedrooms=2,
        bathrooms=1,
        address="123 5th Ave, New York, NY",
        description="Cozy apartment in downtown New York.",
        photos=["https://example.com/photo1.jpg"]
    ),
    Property(
        id=2,
        country="Australia",
        city="Sydney",
        type="house",
        price=1250000,
        size=1500,
        bedrooms=4,
        bathrooms=3,
        address="456 Sydney Rd, Sydney NSW",
        description="Spacious family home with garden.",
        photos=["https://example.com/photo2.jpg"]
    )
]

@app.get("/properties/search", response_model=List[Property])
def search_properties(
    country: Optional[str] = Query(None),
    city: Optional[str] = Query(None),
    type: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    page: int = 1,
    per_page: int = 10
):
    filtered = properties_db
    if country:
        filtered = [p for p in filtered if p.country.lower() == country.lower()]
    if city:
        filtered = [p for p in filtered if p.city.lower() == city.lower()]
    if type:
        filtered = [p for p in filtered if p.type.lower() == type.lower()]
    if min_price is not None:
        filtered = [p for p in filtered if p.price >= min_price]
    if max_price is not None:
        filtered = [p for p in filtered if p.price <= max_price]

    start = (page - 1) * per_page
    end = start + per_page
    return filtered[start:end]

@app.get("/properties/{property_id}", response_model=Property)
def get_property(property_id: int):
    for p in properties_db:
        if p.id == property_id:
            return p
    raise HTTPException(status_code=404, detail="Property not found")