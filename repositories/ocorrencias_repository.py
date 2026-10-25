def consultar(db, filtro=None, campos=None, limite=0):
    cursor = db['ocorrencias'].find(filtro or {}, campos)
    return list(cursor.limit(limite)) if limite else list(cursor)
