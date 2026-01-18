# 🌾 SaveNutri — Conectando Campo e Escola

> **Otimizei a gestão da merenda escolar: substituímos processos burocráticos por uma logística inteligente que elimina o desperdício, assegura conformidade legal e garante alimentos frescos para os alunos**.

---

## 📋 Sobre o Projeto

O **SaveNutri** resolve um dos principais desafios logísticos e nutricionais enfrentados por prefeituras.  
A legislação exige que **30% do orçamento da merenda escolar** seja destinado à agricultura familiar, porém a ausência de dados estruturados e de conexão direta entre oferta e demanda dificulta o cumprimento dessa meta.

A plataforma automatiza o **match geográfico** entre escolas e produtores e utiliza **IA** para sugerir **cardápios baseados na safra local**, reduzindo custos, desperdícios e impacto ambiental.

---

## 🚀 Principais Funcionalidades

- 📍 **Matching Geoespacial**  
  Algoritmo que calcula a distância real (geodésica) entre produtores e escolas.

- 🍎 **IA Nutricionista**  
  Integração com **GPT-3.5** para geração de cardápios semanais baseados no estoque real do agricultor.

- 💰 **Cálculo de Economia Logística**  
  Estimativa de economia financeira e ambiental com base na redução da cadeia de transporte.

- 🗺️ **Visualização Enriquecida**  
  Mapa interativo em **GeoJSON** para gestão pública, inicialmente focado em **Teresópolis/RJ**.

---

## 🛠️ Tecnologias e Arquitetura

O projeto foi construído com foco em **escalabilidade**, **manutenibilidade** e **boas práticas**, aplicando princípios de **Clean Code** e **SOLID**.

- **Linguagem:** Python 3.10+
- **Framework:** FastAPI (assíncrono e de alta performance)
- **IA:** OpenAI API (GPT-3.5-Turbo com JSON Mode)
- **Geoprocessamento:** Geopy (cálculo de distância real)
- **Validação de Dados:** Pydantic

---

## 🗺️ Geoprocessamento (Data Acquisition)

Para alimentar o motor de busca, são utilizados dados do **OpenStreetMap (OSM)** extraídos via **Overpass API**.  
A query abaixo mapeia **demanda (escolas)** e **oferta (zonas agrícolas e mercados)**:

```overpass
/* QUERY HACKATHON: ESCOLAS + AGRICULTURA (Teresópolis/RJ) */
[out:json][timeout:25];
(
  // DEMANDA (ESCOLAS)
  node["amenity"="school"]({{bbox}});
  way["amenity"="school"]({{bbox}});
  relation["amenity"="school"]({{bbox}});

  // OFERTA (PRODUTORES E PONTOS DE VENDA)
  node["place"="farm"]({{bbox}});
  node["place"="isolated_dwelling"]({{bbox}});
  way["landuse"="farmland"]({{bbox}});
  way["landuse"="orchard"]({{bbox}});
  way["landuse"="meadow"]({{bbox}});
  node["shop"="greengrocer"]({{bbox}});
  node["shop"="farm"]({{bbox}});
  node["amenity"="marketplace"]({{bbox}});
);
out center;
````

---

## 📈 Roadmap & Visão de Futuro

* [ ] **Migração para PostGIS**
  Substituir GeoJSON em memória por um banco de dados espacial profissional.

* [ ] **Dashboard B2B**
  Expansão para escolas particulares e hospitais (modelo SaaS).

* [ ] **Comunicação Ativa**
  Integração com WhatsApp (Twilio) para confirmação de pedidos direto com o produtor.

* [ ] **Módulo de Sazonalidade**
  IA treinada com o calendário agrícola da **EMBRAPA** para prever escassez e otimizar cardápios.

---

## 🔧 Como Executar o Projeto

1. **Clone o repositório**

```bash
git clone https://github.com/GuilhermeSerafim/save-nutri.git
```

2. **Instale as dependências**

```bash
pip install -r requirements.txt
```

3. **Configure o arquivo `.env`**

```env
OPENAI_API_KEY=sua_chave_aqui
```

4. **Inicie o servidor**

```bash
uvicorn main:app --reload
```

---

**Desenvolvido com 💚 para transformar a alimentação escolar brasileira.**
