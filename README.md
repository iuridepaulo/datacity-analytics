# DataCity Analytics — Mobilidade Urbana

Projeto acadêmico de Ciência de Dados para a cidade fictícia de Nova Esperança. Usa **Python, MongoDB, PyMongo, Pandas, NumPy e Matplotlib** para gerar dados sintéticos, consultar viagens, limpar inconsistências, calcular indicadores e gerar quatro gráficos.

## Requisitos
- Python 3.10 ou superior
- MongoDB local ativo na porta 27017 **ou** MongoDB Atlas

## Instalação
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
```
Copie `.env.example` para `.env` e configure `MONGODB_URI`. **Nunca publique `.env` ou credenciais.**

## Execução
```bash
python main.py popular
python main.py contar
python main.py consultar --regiao Norte --limite 5
python main.py consultar --linha LIN001 --inicio 2026-09-01 --fim 2026-09-15
python main.py analisar
jupyter notebook notebooks/analise_datacity.ipynb
```
Execute a partir da pasta raiz. O banco `datacity_db` recebe 50 linhas, 500 veículos, 20.000 viagens e 5.000 ocorrências = **25.550 documentos**. A população é determinística com semente 2026 e utiliza `upsert` por `_id`, evitando duplicação por reexecução. Documentos adicionais já existentes não são apagados.

## Organização
- `config/`: conexão MongoDB com variável de ambiente
- `repositories/`: consultas por coleção e filtros
- `scripts/`: geração sintética e população
- `services/`: tratamento, análise e indicadores
- `visualizations/`: gráficos em PNG
- `notebooks/`: notebook de demonstração
- `data/exports/`: tabelas CSV após análise
- `reports/`: resultados e relatório técnico

## Tratamento e premissas
Regiões são normalizadas; horários fora de 00:00–23:59 são marcados ausentes; duplicações lógicas são removidas apenas do DataFrame analítico; passageiros acima de 150% da capacidade e durações não positivas são tratados como ausentes; atraso negativo é mantido como **adiantamento**. Sobrecarga acima da capacidade, mas até 150%, é sinalizada para investigação, não automaticamente apagada. A unidade principal é a **viagem**; ocorrências não são usadas para duplicar viagens.

## Perguntas e interpretação
O programa responde a atrasos por linha/região, demanda por horário, evolução diária, frequência de tipos, relação entre atrasos e avaliações e possível sobrecarga. Três perguntas adicionais: diferença de demanda por acessibilidade (necessita cruzamento adicional), atraso nos fins de semana e relação entre sobrecarga e avaliações. A correlação atraso/avaliação **não prova causalidade**. Os gráficos e números dependem da execução no seu MongoDB.

## Limitações e ética
Todos os registros são **sintéticos**, sem passageiros identificados. Não representam medições reais. Horários e datas são didáticos: `data` é data BSON em UTC, e `hora` é hora local fictícia separada, sem conversão de fuso. Há vieses intencionais na simulação, pouca diversidade de rotas, ausência de GPS real e avaliações artificiais. Não utilizar indicadores como justificativa isolada para políticas públicas. O projeto respeita minimização de dados e princípios da LGPD.

## Arquitetura
```text
Gerador sintético -> MongoDB (datacity_db) -> PyMongo -> Pandas/NumPy
                                                   |-> CSV/indicadores
                                                   |-> Matplotlib/PNG -> relatório
```

## Publicar no GitHub
Crie um repositório vazio `datacity-analytics` no GitHub, abra o terminal na pasta e execute:
```bash
git init
git add .
git commit -m "Projeto DataCity Analytics"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/datacity-analytics.git
git push -u origin main
```
Envie ao professor o **link HTTPS do repositório**. Não inclua `.env`.
