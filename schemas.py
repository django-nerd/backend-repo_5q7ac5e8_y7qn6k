"""
Database Schemas for Fauzan's Relationship Website

Each Pydantic model represents a MongoDB collection. The collection name is the
lowercase of the class name, e.g., LoveNote -> "lovenote".
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import date as Date

class Couple(BaseModel):
    """
    Couple profile
    Collection: "couple"
    """
    person_a: str = Field(..., description="First partner's name")
    person_b: str = Field(..., description="Second partner's name")
    anniversary: Optional[Date] = Field(None, description="Anniversary date")
    story: Optional[str] = Field(None, description="Short relationship story")

class Memory(BaseModel):
    """
    Timeline memories
    Collection: "memory"
    """
    title: str = Field(..., description="Memory title")
    description: Optional[str] = Field(None, description="What happened")
    event_date: Optional[Date] = Field(None, description="When it happened")
    location: Optional[str] = Field(None, description="Where it happened")
    photo_url: Optional[str] = Field(None, description="Link to a photo")

class LoveNote(BaseModel):
    """
    Little love notes/messages
    Collection: "lovenote"
    """
    author: str = Field(..., description="Who wrote the note (e.g., Fauzan)")
    message: str = Field(..., description="The note content")
    mood: Optional[str] = Field(None, description="Happy, grateful, etc.")
