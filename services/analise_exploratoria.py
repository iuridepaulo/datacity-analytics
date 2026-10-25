def perguntas_adicionais(df):
    return {
      'Acessibilidade: veículos acessíveis recebem demanda diferente?': 'Comparar passageiros médios por acessibilidade, após cruzar veículos.',
      'Os finais de semana têm atrasos diferentes?': df.assign(fim_de_semana=df['data'].dt.dayofweek>=5).groupby('fim_de_semana')['atraso_minutos'].mean().round(2).to_dict(),
      'Viagens com lotação acima da capacidade têm avaliação menor?': df.assign(sobrecarga=df['passageiros']>df['capacidade']).groupby('sobrecarga')['avaliacao'].mean().round(2).to_dict(),
    }
