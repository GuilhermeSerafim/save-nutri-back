from openai import OpenAI
from app.core.config import settings

class AIService:
    """Gerencia a comunicação com o motor de IA da OpenAI."""
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def generate_menu(self, ingredients: list[str]):
        """Cria sugestão de cardápio via GPT."""
        # Coloque aqui o prompt e a chamada do client.chat.completions
        pass