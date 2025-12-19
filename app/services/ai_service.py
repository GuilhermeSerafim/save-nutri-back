# app/services/ai_service.py
import json
from openai import OpenAI
from app.core.config import settings

class AIService:
    def __init__(self):
        # Inicializa o cliente usando a chave que está no seu .env
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def generate_menu(self, products: list[str]):
        """Cria sugestão de cardápio via GPT."""
        
        # 1. Prepara o texto dos ingredientes
        ingredientes_texto = ", ".join(products)
        
        # 2. Monta o Prompt
        prompt = f"""
        Você é uma Nutricionista especialista no PNAE (Programa Nacional de Alimentação Escolar).
        CONTEXTO: O agricultor local dispõe de: {ingredientes_texto}.
        Crie um cardápio para Segunda e Terça-feira.
        RESPOSTA (OBRIGATORIAMENTE JSON PURO):
        {{
            "menu_suggestion": {{
                "segunda": {{ "prato": "...", "ingredientes_usados": [...], "analise_ia": "..." }},
                "terca": {{ "prato": "...", "ingredientes_usados": [...], "analise_ia": "..." }}
            }}
        }}
        """

        try:
            # 3. Chama a API da OpenAI
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Você é um assistente que responde apenas em JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            
            # 4. PARTE CRUCIAL: Retornar o conteúdo processado
            content = response.choices[0].message.content
            return json.loads(content) # <--- O retorno deve ser o dicionário JSON

        except Exception as e:
            print(f"❌ Erro na OpenAI: {e}")
            # Fallback para não retornar null se a IA falhar
            return self._get_fallback_menu(products)

    def _get_fallback_menu(self, products):
        """Retorno padrão caso a API da OpenAI falhe."""
        return {
            "menu_suggestion": {
                "segunda": {"prato": "Arroz, Feijão e Salada", "ingredientes_usados": products[:2], "analise_ia": "Menu de contingência."},
                "terca": {"prato": "Sopa de Legumes", "ingredientes_usados": products, "analise_ia": "Menu de contingência."}
            }
        }