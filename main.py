import argparse
import json
from pathlib import Path
import pandas as pd
from pymongo.errors import PyMongoError
from config.database import conectar
from repositories.viagens_repository import consultar
from services.preparacao_dados import preparar, COLUNAS
from services.indicadores import calcular
from services.analise_exploratoria import perguntas_adicionais
from visualizations.graficos import gerar
from scripts.popular_banco import popular

def executar(db):
    docs=consultar(db)
    veiculos=list(db.veiculos.find({}, {'_id':1,'capacidade':1,'acessivel':1}))
    df, qualidade=preparar(docs,veiculos)
    resultados=calcular(df)
    pasta=Path('data/exports');pasta.mkdir(parents=True,exist_ok=True)
    df[COLUNAS].to_csv(pasta/'viagens_tratadas.csv',index=False)
    for chave,valor in resultados.items():
        if isinstance(valor,pd.DataFrame): valor.to_csv(pasta/f'indicadores_{chave}.csv',index=False)
    arquivos=gerar(df,resultados)
    rel=Path('reports');rel.mkdir(exist_ok=True)
    (rel/'resultados.json').write_text(json.dumps({'qualidade':qualidade,'resumo':resultados['resumo'],'perguntas_adicionais':perguntas_adicionais(df)},ensure_ascii=False,indent=2,default=str),encoding='utf-8')
    print('Resumo:',json.dumps(resultados['resumo'],ensure_ascii=False,indent=2))
    print('Qualidade:',json.dumps(qualidade,ensure_ascii=False,indent=2))
    print('Gráficos:',*arquivos,sep='\n- ')
    return resultados

def main():
    parser=argparse.ArgumentParser(description='DataCity Analytics')
    parser.add_argument('acao',choices=['popular','analisar','consultar','contar'])
    parser.add_argument('--linha');parser.add_argument('--regiao');parser.add_argument('--inicio');parser.add_argument('--fim');parser.add_argument('--hora');parser.add_argument('--ocorrencia');parser.add_argument('--limite',type=int,default=5)
    args=parser.parse_args()
    try:
        cliente,db=conectar()
        try:
            if args.acao=='popular':popular(db)
            elif args.acao=='analisar':executar(db)
            elif args.acao=='contar':
                for c in ['linhas','veiculos','viagens','ocorrencias']:print(c,db[c].count_documents({}))
            else:
                for d in consultar(db,args.linha,args.regiao,args.inicio,args.fim,args.hora,args.ocorrencia,args.limite):print(d)
        finally:cliente.close()
    except (PyMongoError,ValueError) as e:
        print('Erro:',e);raise SystemExit(1)
if __name__=='__main__':main()
