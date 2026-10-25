import pandas as pd

def calcular(df):
    resultados={}
    for nome,grupo in [('linha','linha'),('regiao','regiao'),('horario','hora'),('ocorrencia','tipo_ocorrencia')]:
        resultados[nome]=df.groupby(grupo,dropna=False).agg(viagens=('id_viagem','count'),passageiros=('passageiros','sum'),atraso_medio=('atraso_minutos','mean'),atraso_mediano=('atraso_minutos','median'),duracao_media=('duracao_minutos','mean'),avaliacao_media=('avaliacao','mean')).reset_index()
    resultados['diario']=df.groupby(df['data'].dt.strftime('%Y-%m-%d')).agg(atraso_medio=('atraso_minutos','mean'),duracao_media=('duracao_minutos','mean'),passageiros=('passageiros','sum')).reset_index()
    resultados['resumo']= {'viagens':len(df),'passageiros_medios':float(df['passageiros'].mean()),'duracao_media':float(df['duracao_minutos'].mean()),'atraso_medio':float(df['atraso_minutos'].mean()),'atraso_mediano':float(df['atraso_minutos'].median()),'avaliacao_media':float(df['avaliacao'].mean()),'correlacao_atraso_avaliacao':float(df[['atraso_minutos','avaliacao']].corr().iloc[0,1]),'lotacao_acima_capacidade':int((df['passageiros']>df['capacidade']).sum())}
    return resultados
