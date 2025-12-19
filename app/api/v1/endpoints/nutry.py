# app/api/v1/endpoints/nutry.py
from fastapi import APIRouter, Depends
from app.services.ai_service import AIService
from app.schemas.menu import MenuRequest

router = APIRouter()

@router.post("/generate_menu")
def generate_menu(request: MenuRequest, service: AIService = Depends()):
    """Endpoint para geração de cardápio inteligente."""
    return service.generate_menu(request.products)