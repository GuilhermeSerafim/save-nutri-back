# 🌾 SaveNutri - Conectando Campo e Escola

> **SaaS B2G (Business to Government)** desenhado para otimizar o cumprimento da Lei 11.947/2009 (PNAE), conectando Escolas Públicas a Agricultores Familiares locais através de Inteligência Artificial e Geoprocessamento.

## 📋 Sobre o Projeto

O **SaveNutri** resolve o desafio logístico e nutricional das prefeituras. A lei exige que **30% do orçamento da merenda** venha da agricultura familiar, mas a falta de dados e conexão dificulta esse processo. Nossa plataforma automatiza o *match* geográfico e utiliza IA para sugerir cardápios baseados na safra local.

## 🚀 Principais Funcionalidades

* 📍 **Matching Geoespacial:** Algoritmo que calcula a distância real (geodésica) entre produtores e escolas.
* 🍎 **IA Nutricionista:** Integração com GPT-3.5 para geração de cardápios semanais baseados no estoque real do agricultor.
* 💰 **Cálculo de Economia Logística:** Estimativa de economia baseada na redução da cadeia de transporte.
* 🗺️ **Visualização Enriquecida:** Mapa interativo via GeoJSON para gestão pública, inicialmente de Teresópolis/RJ.

## 🛠️ Tecnologias e Arquitetura

O projeto foi construído focando em **escalabilidade e manutenibilidade**, aplicando princípios de **Clean Code** e **SOLID**:

* **Linguagem:** Python 3.10+
* **Framework:** FastAPI (Assíncrono e de alta performance)
* **IA:** OpenAI API (GPT-3.5-Turbo com JSON Mode)
* **Geoprocessamento:** Geopy (Cálculos de distância real)
* **Validação:** Pydantic (Garantia de integridade de dados)

---

## 📈 Roadmap & Visão de Futuro

* [ ] **Migração PostGIS:** Substituir o GeoJSON em memória por um banco de dados espacial profissional.
* [ ] **Dashboard B2B:** Expandir para escolas particulares e hospitais (Modelo SaaS).
* [ ] **Comunicação Ativa:** Integração com WhatsApp (Twilio) para confirmação de pedidos direto com o produtor.
* [ ] **Módulo de Sazonalidade:** IA treinada com o calendário agrícola da EMBRAPA para prever escassez de produtos.

## 🔧 Como Executar

1. **Clone o repositório:**
```bash
git clone https://github.com/GuilhermeSerafim/save-nutri.git

```


2. **Instale as dependências:**
```bash
pip install -r requirements.txt

```


3. **Configure o `.env`:**
```env
OPENAI_API_KEY=sua_chave_aqui

```


4. **Rode o servidor:**
```bash
uvicorn main:app --reload

```



---

**Desenvolvido com 💚 para transformar a alimentação escolar brasileira.**