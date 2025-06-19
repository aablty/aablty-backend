from pydantic import BaseModel, field_validator
from typing import List, Optional
from enum import Enum


# Translation Model
class Translation(BaseModel):
    ru: str
    en: str

    @field_validator("ru", "en")
    def not_empty(cls, v):
        if not v.strip():
            raise ValueError("Translation fields must not be empty.")
        return v


# Project Models
class ProjectType(str, Enum):
    DECENT = "decent"
    SMALL = "small"


class ProjectLink(BaseModel):
    label: str
    link: str


class BaseProject(BaseModel):
    type: ProjectType
    title: Translation
    description: Translation
    image: str
    image_public_id: str
    stack: List[str]
    links: List[ProjectLink]


class CreateProject(BaseProject):
    @field_validator("stack")
    def check_stack_not_empty(cls, v):
        if not v:
            raise ValueError("Stack cannot be empty")
        return v

    @field_validator("links")
    def check_links_not_empty(cls, v):
        if not v:
            raise ValueError("Links cannot be empty")
        return v


class Project(BaseProject):
    id: str

    class Config:
        from_attributes = True


# Skills
class BaseSkillCategory(BaseModel):
    title: Translation
    items: List[str]


class CreateSkillCategory(BaseSkillCategory):
    @field_validator("items")
    def check_items_not_empty(cls, v):
        if not v:
            raise ValueError("Items cannot be empty")
        return v


class SkillCategory(BaseSkillCategory):
    id: str

    class Config:
        from_attributes = True


# Fact
class Fact(BaseModel):
    content: Translation
    id: str

    class Config:
        from_attributes = True


class CreateFact(BaseModel):
    content: Translation


# Education
class EducationStatus(str, Enum):
    CURRENT = "current"
    GRADUATED = "graduated"


class BaseEducation(BaseModel):
    institution: Translation
    degree: Translation
    start_year: str
    end_year: str
    status: Translation
    location: Translation


class CreateEducation(BaseEducation):
    @field_validator("start_year", "end_year")
    def check_years_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Year fields must not be empty.")
        return v


class Education(BaseEducation):
    id: str

    class Config:
        from_attributes = True


# Certification
class CertificationStatus(str, Enum):
    CURRENT = "current"
    COMPLETED = "completed"


class BaseCertification(BaseModel):
    name: Translation
    provider: Translation
    year: str
    status: Translation


class Certification(BaseCertification):
    id: str

    class Config:
        from_attributes = True


class CreateCertification(BaseCertification):
    @field_validator("year")
    def check_year_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Year field must not be empty.")
        return v


# Contact Form
class SendForm(BaseModel):
    name: str
    email: str
    message: str
