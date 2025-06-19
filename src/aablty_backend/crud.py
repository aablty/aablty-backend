from sqlalchemy.orm import Session
from typing import List, Optional
from . import models, schemas


# Project CRUD
def create_project(db: Session, project: schemas.CreateProject) -> models.Project:
    db_project = models.Project(
        title_ru=project.title.ru,
        title_en=project.title.en,
        description_ru=project.description.ru,
        description_en=project.description.en,
        image=project.image,
        image_public_id=project.image_public_id,
        stack=project.stack,
        type=project.type.value if project.type else None,
        links=[link.model_dump() for link in project.links]
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def get_project(db: Session, project_id: str) -> Optional[models.Project]:
    return db.query(models.Project).filter(models.Project.id == project_id).first()


def get_projects(db: Session, skip: int = 0, limit: int = 100) -> List[models.Project]:
    return db.query(models.Project).offset(skip).limit(limit).all()


def delete_project(db: Session, project_id: str) -> bool:
    db_project = db.query(models.Project).filter(
        models.Project.id == project_id).first()
    if not db_project:
        return False

    db.delete(db_project)
    db.commit()
    return True


# Skills CRUD
def create_skill_category(db: Session, skill_category: schemas.CreateSkillCategory) -> models.SkillCategory:
    db_skill_category = models.SkillCategory(
        title_ru=skill_category.title.ru,
        title_en=skill_category.title.en,
        items=skill_category.items
    )
    db.add(db_skill_category)
    db.commit()
    db.refresh(db_skill_category)
    return db_skill_category


def get_skill_category(db: Session, skill_category_id: str) -> Optional[models.SkillCategory]:
    return db.query(models.SkillCategory).filter(models.SkillCategory.id == skill_category_id).first()


def get_skills(db: Session, skip: int = 0, limit: int = 100) -> List[models.SkillCategory]:
    return db.query(models.SkillCategory).offset(skip).limit(limit).all()


def delete_skill_category(db: Session, skill_category_id: str) -> bool:
    db_skill_category = db.query(models.SkillCategory).filter(
        models.SkillCategory.id == skill_category_id).first()
    if not db_skill_category:
        return False

    db.delete(db_skill_category)
    db.commit()
    return True


# Fact CRUD
def create_fact(db: Session, fact: schemas.CreateFact) -> models.Fact:
    db_fact = models.Fact(
        content_ru=fact.content.ru,
        content_en=fact.content.en
    )
    db.add(db_fact)
    db.commit()
    db.refresh(db_fact)
    return db_fact


def get_facts(db: Session, skip: int = 0, limit: int = 100) -> List[models.Fact]:
    return db.query(models.Fact).offset(skip).limit(limit).all()


def delete_fact(db: Session, fact_id: str) -> bool:
    db_fact = db.query(models.Fact).filter(models.Fact.id == fact_id).first()
    if not db_fact:
        return False

    db.delete(db_fact)
    db.commit()
    return True


# Education CRUD
def create_education(db: Session, education: schemas.CreateEducation) -> models.Education:
    db_education = models.Education(
        institution_ru=education.institution.ru,
        institution_en=education.institution.en,
        degree_ru=education.degree.ru,
        degree_en=education.degree.en,
        start_year=education.start_year,
        end_year=education.end_year,
        status_ru=education.status.ru,
        status_en=education.status.en,
        location_ru=education.location.ru,
        location_en=education.location.en
    )
    db.add(db_education)
    db.commit()
    db.refresh(db_education)
    return db_education


def get_educations(db: Session, skip: int = 0, limit: int = 100) -> List[models.Education]:
    return db.query(models.Education).offset(skip).limit(limit).all()


def delete_education(db: Session, education_id: str) -> bool:
    db_education = db.query(models.Education).filter(
        models.Education.id == education_id).first()
    if not db_education:
        return False

    db.delete(db_education)
    db.commit()
    return True


# Certification CRUD
def create_certification(db: Session, certification: schemas.CreateCertification) -> models.Certification:
    db_certification = models.Certification(
        name_ru=certification.name.ru,
        name_en=certification.name.en,
        provider_ru=certification.provider.ru,
        provider_en=certification.provider.en,
        year=certification.year,
        status_ru=certification.status.ru,
        status_en=certification.status.en
    )
    db.add(db_certification)
    db.commit()
    db.refresh(db_certification)
    return db_certification


def get_certifications(db: Session, skip: int = 0, limit: int = 100) -> List[models.Certification]:
    return db.query(models.Certification).offset(skip).limit(limit).all()


def delete_certification(db: Session, certification_id: str) -> bool:
    db_certification = db.query(models.Certification).filter(
        models.Certification.id == certification_id).first()
    if not db_certification:
        return False

    db.delete(db_certification)
    db.commit()
    return True
