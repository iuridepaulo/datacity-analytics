import pandas as pd

COLUNAS = ['id_viagem','data','hora','linha','veiculo','regiao','passageiros','duracao_minutos','atraso_minutos','avaliacao','tipo_ocorrencia']

def preparar(documentos, veiculos):
    df=pd.DataFrame(documentos).rename(columns={'_id':'id_viagem'})
    if df.empty: raise ValueError('Não há viagens. Execute a população do banco primeiro.')
    problemas={}
    problemas['ausentes_antes']=df.isna().sum().to_dict()
    problemas['duplicatas_logicas']=int(df.duplicated(subset=[c for c in COLUNAS if c!='id_viagem'],keep='first').sum())
    df['regiao']=df['regiao'].astype('string').str.strip().str.title()
    df['hora']=df['hora'].astype('string').str.strip().str.zfill(5)
    valido_hora=df['hora'].str.fullmatch(r'(?:[01]\d|2[0-3]):[0-5]\d').fillna(False)
    problemas['horas_invalidas']=int((~valido_hora).sum())
    df.loc[~valido_hora,'hora']=pd.NA
    df['data']=pd.to_datetime(df['data'],errors='coerce',utc=True)
    for c in ['passageiros','duracao_minutos','atraso_minutos','avaliacao']:
        df[c]=pd.to_numeric(df[c],errors='coerce')
    capacidades={v['_id']:v['capacidade'] for v in veiculos}
    df['capacidade']=df['veiculo'].map(capacidades)
    problemas['lotacao_acima_capacidade']=int((df['passageiros']>df['capacidade']).sum())
    problemas['passageiros_impossiveis']=int((df['passageiros']>df['capacidade']*1.5).sum())
    df.loc[(df['passageiros']<0)|(df['passageiros']>df['capacidade']*1.5),'passageiros']=float('nan')
    problemas['duracoes_invalidas']=int((df['duracao_minutos']<=0).sum())
    df.loc[df['duracao_minutos']<=0,'duracao_minutos']=float('nan')
    df.loc[~df['avaliacao'].between(1,5),'avaliacao']=float('nan')
    # Atrasos negativos são adiantamentos e permanecem válidos.
    problemas['adiantamentos']=int((df['atraso_minutos']<0).sum())
    df=df.drop_duplicates(subset=[c for c in COLUNAS if c!='id_viagem'],keep='first')
    problemas['linhas_apos_limpeza']=len(df)
    return df,problemas
