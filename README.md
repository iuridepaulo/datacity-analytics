# DataCity Analytics

Projeto desenvolvido para analisar dados de mobilidade urbana da cidade fictícia de Nova Esperança. A aplicação utiliza Python e MongoDB para armazenar e consultar informações de linhas, veículos, viagens e ocorrências do transporte coletivo.

Com os dados, é possível analisar atrasos, quantidade de passageiros, duração das viagens e outros indicadores. As análises utilizam Pandas, e os gráficos são gerados com Matplotlib.

## Pré-requisitos

- Python 3 instalado
- MongoDB instalado e em execução
- Bibliotecas Python utilizadas no projeto
- Terminal ou VS Code para executar os scripts

## Instalação

Baixe o projeto e abra a pasta no VS Code ou no terminal.

Para instalar as bibliotecas necessárias, execute:

```bash
pip install -r requirements.txt
```

## Configuração

O projeto utiliza o banco `datacity_db` no MongoDB, com as coleções `linhas`, `veiculos`, `viagens` e `ocorrencias`.

Configure a conexão com o MongoDB no arquivo de ambiente, conforme as variáveis utilizadas em `config/database.py`. Caso exista um arquivo `.env.example`, ele pode ser usado como referência para criar o `.env`.

O arquivo `.env` não deve ser publicado no repositório, pois pode conter dados de acesso ao banco.

## Execução

Primeiro, verifique se o MongoDB está em execução.

Para gerar os dados de teste e preencher o banco, execute na pasta principal do projeto:

```bash
python -m scripts.popular_banco
```

Depois, execute a aplicação principal:

```bash
python main.py
```

Os scripts de análise consultam os registros do MongoDB para calcular indicadores e gerar gráficos. Os resultados podem ser utilizados para comparar linhas, regiões, horários e ocorrências.

## Organização do projeto

- `config/`: conexão com o banco de dados
- `repositories/`: consultas às coleções do MongoDB
- `services/`: análises e cálculos dos indicadores
- `scripts/`: geração dos dados utilizados no projeto
- `main.py`: execução principal da aplicação
- `requirements.txt`: bibliotecas necessárias

## Dados utilizados

Os dados são sintéticos, ou seja, foram gerados para simular situações do transporte coletivo. Não representam viagens reais nem contêm informações pessoais de passageiros.
