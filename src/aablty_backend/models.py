from sqlalchemy import Column, String, Text, JSON
import uuid
from .db import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    type = Column(String, nullable=False)
    title_ru = Column(String, nullable=False)
    title_en = Column(String, nullable=False)
    description_ru = Column(Text, nullable=False)
    description_en = Column(Text, nullable=False)
    image = Column(String, nullable=False)
    image_public_id = Column(String, nullable=False)
    stack = Column(JSON, nullable=False, default=lambda: [])  # List[str]
    links = Column(JSON, nullable=False)  # List[dict] keys: "label", "link"


class SkillCategory(Base):
    __tablename__ = "skills"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title_ru = Column(String, nullable=False)
    title_en = Column(String, nullable=False)
    items = Column(JSON, nullable=False)  # List[str]


class Fact(Base):
    __tablename__ = "facts"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    content_ru = Column(Text, nullable=False)
    content_en = Column(Text, nullable=False)


class Education(Base):
    __tablename__ = "education"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    institution_ru = Column(String, nullable=False)
    institution_en = Column(String, nullable=False)
    degree_ru = Column(String, nullable=False)
    degree_en = Column(String, nullable=False)
    start_year = Column(String, nullable=False)
    end_year = Column(String, nullable=True)
    status_ru = Column(String, nullable=False)
    status_en = Column(String, nullable=False)
    location_ru = Column(String, nullable=False)
    location_en = Column(String, nullable=False)


class Certification(Base):
    __tablename__ = "certifications"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name_ru = Column(String, nullable=False)
    name_en = Column(String, nullable=False)
    provider_ru = Column(String, nullable=False)
    provider_en = Column(String, nullable=False)
    year = Column(String, nullable=False)
    status_ru = Column(String, nullable=False)
    status_en = Column(String, nullable=False)
