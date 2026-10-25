from datetime import datetime

def consultar(db, linha=None, regiao=None, inicio=None, fim=None, hora=None, ocorrencia=None, limite=0):
    filtro = {}
    if linha: filtro['linha'] = linha
    if regiao: filtro['regiao'] = regiao
    if hora: filtro['hora'] = hora
    if ocorrencia: filtro['tipo_ocorrencia'] = ocorrencia
    if inicio or fim:
        filtro['data'] = {}
        if inicio: filtro['data']['$gte'] = datetime.fromisoformat(inicio)
        if fim: filtro['data']['$lte'] = datetime.fromisoformat(fim)
    cursor = db.viagens.find(filtro, {'_id':1,'data':1,'hora':1,'linha':1,'veiculo':1,'regiao':1,'passageiros':1,'duracao_minutos':1,'atraso_minutos':1,'avaliacao':1,'tipo_ocorrencia':1})
    return list(cursor.limit(limite)) if limite else list(cursor)
