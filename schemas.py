"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogpost" collection
"""

from pydantic import BaseModel, Field, EmailStr, HttpUrl
from typing import Optional, List
from datetime import datetime

# Core examples
class User(BaseModel):
    name: str = Field(..., description="Full name")
    email: EmailStr = Field(..., description="Email address")
    address: Optional[str] = Field(None, description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# NEXORA SYNERGY content models
class Service(BaseModel):
    icon: str = Field(..., description="Icon name (e.g., 'Code', 'Shield')")
    title: str
    slug: str
    summary: str
    content: Optional[str] = None
    featured: bool = False

class Project(BaseModel):
    title: str
    slug: str
    summary: str
    content: Optional[str] = None
    images: Optional[List[HttpUrl]] = None
    tags: Optional[List[str]] = None
    metrics: Optional[dict] = None

class BlogPost(BaseModel):
    title: str
    slug: str
    author: str
    date: datetime
    tags: Optional[List[str]] = None
    excerpt: Optional[str] = None
    coverImage: Optional[HttpUrl] = None
    content: str

class Testimonial(BaseModel):
    name: str
    role: Optional[str] = None
    company: Optional[str] = None
    quote: str
    avatar: Optional[HttpUrl] = None

class NewsletterSubscriber(BaseModel):
    email: EmailStr

class ContactMessage(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    message: str
