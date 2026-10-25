from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def gerar(df, resultados, pasta='reports/graficos'):
    pasta=Path(pasta);pasta.mkdir(parents=True,exist_ok=True)
    def salvar(nome):
        plt.tight_layout();plt.savefig(pasta/f'{nome}.png',dpi=160);plt.close()
    r=resultados['regiao'].sort_values('atraso_medio',ascending=False)
    plt.figure(figsize=(8,4));plt.bar(r['regiao'],r['atraso_medio']);plt.title('Atraso médio por região');plt.ylabel('Minutos');salvar('01_atraso_regiao')
    d=resultados['diario'];plt.figure(figsize=(10,4));plt.plot(d['data'],d['atraso_medio']);plt.xticks(rotation=60);plt.title('Evolução diária do atraso médio');plt.ylabel('Minutos');salvar('02_evolucao')
    plt.figure(figsize=(8,4));plt.hist(df['atraso_minutos'].dropna(),bins=35);plt.title('Distribuição dos atrasos e adiantamentos');plt.xlabel('Minutos (negativo = adiantamento)');plt.ylabel('Viagens');salvar('03_distribuicao')
    plt.figure(figsize=(8,4));plt.scatter(df['atraso_minutos'],df['avaliacao'],s=5,alpha=.13);plt.title('Atraso x avaliação (associação, não causalidade)');plt.xlabel('Atraso (min)');plt.ylabel('Avaliação');salvar('04_relacao')
    return sorted(str(x) for x in pasta.glob('*.png'))
