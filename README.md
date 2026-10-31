# SaveNutri — backend de demonstração

Protótipo FastAPI para explorar correspondência geográfica entre escolas e pontos classificados como agricultores em Teresópolis. Este repositório contém o backend; a interface fica em save-nutri-front.

## Implementação e limites

- `app/main.py` expõe grupos de rotas de nutrição, GeoJSON e correspondência.
- `DataService` lê o GeoJSON local e mantém dados em memória. Número de alunos, orçamento, demanda e produtos são gerados aleatoriamente; `tem_dap` é fixado como verdadeiro. Esses campos são simulações, não cadastro validado, estoque real ou prova de habilitação.
- `LocationService` usa distância geodésica; não calcula percurso rodoviário. A economia usa `max(0, 500 - dist_km * 15)`, uma fórmula demonstrativa sem calibração comprovada.
- `AIService` solicita sugestões para segunda e terça-feira usando o modelo configurado no código e retorna menu de contingência em caso de erro. Não comprova adequação nutricional, conformidade legal, redução de desperdício ou impacto ambiental.
- Falha ao carregar o GeoJSON é capturada e impressa; o endpoint de match acessa o primeiro resultado sem tratar lista vazia. Dados indisponíveis podem impedir o resultado; não devem ser interpretados como cálculo completo.

## Ambiente

As dependências estão em `requirements.txt` (FastAPI, Geopy, Pydantic e cliente OpenAI). O entrypoint é `app.main:app`; execute a partir da raiz para resolver o caminho do GeoJSON. A integração de IA depende de configuração própria e pode gerar chamadas pagas.

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
```

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

## Inicialização local

Prepare e ative um ambiente Python próprio. Faça o checkout e instale as dependências:

```bash
git clone https://github.com/GuilhermeSerafim/save-nutri-back.git
cd save-nutri-back
python -m pip install -r requirements.txt
```

Configure `OPENAI_API_KEY` no ambiente do processo, sem versionar seu valor. A partir da raiz do repositório, inicie a API:

```bash
uvicorn app.main:app --reload
```

O carregamento dos dados depende de `data/TeresopolisEscolasELocaisDeProducao.geojson`. Mantenha esse arquivo acessível no checkout; a ausência de dados pode impedir os resultados de correspondência.
