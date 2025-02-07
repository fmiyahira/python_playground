from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class Company(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    places: List["Place"] = Relationship(back_populates="company")

class Place(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str
    company_id: int = Field(foreign_key="company.id")
    company: Optional[Company] = Relationship(back_populates="places")
    