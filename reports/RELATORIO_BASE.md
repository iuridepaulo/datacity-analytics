# Relatório técnico — DataCity Analytics

## 1. Introdução
Nova Esperança é uma cidade fictícia de aproximadamente 750 mil habitantes. O projeto demonstra como dados de mobilidade podem apoiar a análise de atrasos, duração, demanda, avaliações e ocorrências.

## 2. Objetivos e continuidade
A etapa inicial identificou fontes e problemas de arquitetura. Nesta etapa, os dados sintéticos são armazenados no MongoDB, consultados via PyMongo e analisados com Pandas, produzindo gráficos e recomendações.

## 3. Arquitetura e modelagem
Fluxo: gerador sintético → MongoDB → PyMongo → Pandas/NumPy → Matplotlib → indicadores/relatório. Coleções: linhas (50), veículos (500), viagens (20.000) e ocorrências (5.000). IDs permitem referências lógicas. Datas BSON, hora em string local fictícia.

## 4. Metodologia e qualidade
Geração determinística (seed 2026). Tratamentos: normalização de região/hora, checagem de ausências, remoção de duplicatas lógicas na análise, validação de duração e capacidade. Atrasos negativos são adiantamentos válidos. Reexecução da população não cria novas IDs.

## 5. Resultados e indicadores
**Preencher após executar `python main.py analisar` e consultar `reports/resultados.json` e os CSVs.** Não se devem inventar resultados numéricos sem execução.

## 6. Gráficos e interpretação
1. Atraso médio por região: comparar regiões mais afetadas.
2. Evolução diária: investigar oscilação de atraso ao longo de setembro.
3. Histograma: diferenciar adiantamentos e atrasos altos.
4. Dispersão atraso/avaliação: verificar associação, sem inferir causalidade.

## 7. Três decisões com DIKW
1. **Revisar horários** das linhas com maiores atrasos (dados de viagens → média/mediana → identificação de padrões → proposta de ajuste).
2. **Redistribuir veículos** nos horários de maior demanda (passageiros por viagem → agregação horária → identificação de pico → reforço operacional).
3. **Investigar ocorrências** nas regiões críticas (tipos e frequência → agrupamentos → prioridade operacional → inspeção e ações específicas).
São hipóteses de decisão, sujeitas à validação com dados reais.

## 8. Cinco limitações
1. Dados sintéticos não refletem a cidade real.
2. Sazonalidade limitada a setembro de 2026.
3. Avaliações são simuladas e dependem parcialmente dos atrasos por construção.
4. Não há informação real de trânsito, GPS ou clima.
5. A amostragem não representa adequadamente todas as rotas e usuários.

## 9. Ética, LGPD e conclusão
Não são utilizados dados pessoais. Recomendações devem ser auditadas e validadas antes de uso público. A aplicação demonstra a cadeia dados → informação → conhecimento → decisão, sem substituir análise contextual.

## Referências
- Enunciado UNIVAP: DataCity — Ciência de Dados Aplicada à Mobilidade Urbana (Parte 2).
- Documentação oficial: Python, MongoDB, PyMongo, Pandas e Matplotlib.
