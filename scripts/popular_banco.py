"""Gera 50 linhas, 500 veículos, 20.000 viagens e 5.000 ocorrências (25.550 registros)."""
from datetime import datetime, timedelta
import random
from pymongo import ReplaceOne
from config.database import conectar

REGIOES = ['Norte', 'Sul', 'Leste', 'Oeste', 'Centro']
TIPOS = ['nenhuma', 'transito', 'falha_mecanica', 'clima', 'outros']

def popular(db, seed=2026):
    rng = random.Random(seed)
    linhas = [{'_id':f'LIN{i:03}', 'nome':f'Linha {i:03} - {REGIOES[(i-1)//10]}', 'regiao':REGIOES[(i-1)//10], 'tipo':'urbana', 'ativa':True} for i in range(1,51)]
    veiculos = [{'_id':f'VEI{i:04}', 'linha_id':linhas[(i-1)//10]['_id'], 'capacidade':rng.choice([45,60,80]), 'acessivel':i%3!=0, 'ativo':True} for i in range(1,501)]
    viagens=[]; ocorrencias=[]
    for i in range(1,20001):
        veiculo=veiculos[rng.randrange(500)]
        linha=linhas[int(veiculo['linha_id'][-3:])-1]
        dia=datetime(2026,9,1)+timedelta(days=rng.randrange(30))
        hora=rng.randrange(5,24)
        pico=hora in (7,8,17,18)
        capacidade=veiculo['capacidade']
        passageiros=min(capacidade+10, max(0,int(rng.gauss(capacidade*(0.85 if pico else 0.53),10))))
        tipo=rng.choices(TIPOS,weights=[75,14,4,4,3])[0]
        atraso=round(rng.gauss(9 if pico else 4,7)) + (10 if tipo!='nenhuma' else 0)
        avaliacao=max(1,min(5,round(4.6-max(0,atraso)/12+rng.gauss(0,0.65))))
        viagens.append({'_id':f'VIA{i:05}', 'data':dia, 'hora':f'{hora:02}:{rng.choice([0,15,30,45]):02}', 'linha':linha['_id'], 'veiculo':veiculo['_id'], 'regiao':linha['regiao'], 'passageiros':passageiros, 'duracao_minutos':max(12,round(rng.gauss(38+max(0,atraso)*0.5,9))), 'atraso_minutos':atraso, 'avaliacao':avaliacao, 'tipo_ocorrencia':tipo})
    # Registros de qualidade controlados, sem afetar as referências entre coleções.
    viagens[0]['avaliacao']=None
    viagens[1]['regiao']='norte '
    viagens[2]['hora']='7:30'
    viagens[3]['atraso_minutos']=-15 # adiantamento válido
    viagens[4]['passageiros']=450 # inválido frente à capacidade
    viagens[5]['passageiros']=None
    viagens[6]['duracao_minutos']=-8
    viagens[7]['hora']='99:99'
    # Duplicação lógica dos valores analíticos, com identificador distinto.
    viagens[8].update({k:v for k,v in viagens[9].items() if k!='_id'})
    for i in range(1,5001):
        viagem=viagens[(i-1)*4]
        tipo=viagem['tipo_ocorrencia'] if viagem['tipo_ocorrencia']!='nenhuma' else 'monitoramento'
        ocorrencias.append({'_id':f'OCO{i:05}', 'viagem_id':viagem['_id'], 'tipo':tipo, 'gravidade':rng.choice(['leve','moderada','alta']), 'descricao':f'Registro sintético de {tipo}'})
    for nome, docs in [('linhas',linhas),('veiculos',veiculos),('viagens',viagens),('ocorrencias',ocorrencias)]:
        col=db[nome]
        for inicio in range(0,len(docs),1000):
            col.bulk_write([ReplaceOne({'_id':d['_id']},d,upsert=True) for d in docs[inicio:inicio+1000]],ordered=False)
        print(f'{nome}: {col.count_documents({})} documentos (esperado ao menos {len(docs)})')
    db.viagens.create_index([('linha',1),('data',1)])
    db.viagens.create_index([('regiao',1),('hora',1)])
    db.ocorrencias.create_index('viagem_id')
    for nome in ('linhas','veiculos','viagens','ocorrencias'):
        print(f'Exemplo {nome}: {db[nome].find_one()}')

if __name__=='__main__':
    cliente, db=conectar()
    try: popular(db)
    finally: cliente.close()
