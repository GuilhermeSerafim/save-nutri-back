from pydantic import BaseModel

class MenuRequest(BaseModel):
    """Contrato para solicitação de geração de cardápio."""
    products: list[str]
    school_demand: str = "Hortifruti"