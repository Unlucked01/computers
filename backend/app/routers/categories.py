from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import ComponentCategory
from ..schemas.component import ComponentCategoryCreate, ComponentCategoryResponse

router = APIRouter()


@router.get("/categories", response_model=List[ComponentCategoryResponse])
async def get_categories(db: Session = Depends(get_db)):
    """Получить все категории компонентов"""
    categories = db.query(ComponentCategory).order_by(ComponentCategory.order_priority).all()
    return categories


@router.get("/categories/{category_id}", response_model=ComponentCategoryResponse)
async def get_category(category_id: int, db: Session = Depends(get_db)):
    """Получить категорию по ID"""
    category = db.query(ComponentCategory).filter(ComponentCategory.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    return category


@router.get("/categories/slug/{slug}", response_model=ComponentCategoryResponse)
async def get_category_by_slug(slug: str, db: Session = Depends(get_db)):
    """Получить категорию по slug"""
    category = db.query(ComponentCategory).filter(ComponentCategory.slug == slug).first()
    if not category:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    return category


@router.post("/categories", response_model=ComponentCategoryResponse)
async def create_category(category: ComponentCategoryCreate, db: Session = Depends(get_db)):
    """Создать новую категорию"""
    # Проверяем уникальность slug
    existing = db.query(ComponentCategory).filter(ComponentCategory.slug == category.slug).first()
    if existing:
        raise HTTPException(status_code=400, detail="Категория с таким slug уже существует")
    
    db_category = ComponentCategory(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category 