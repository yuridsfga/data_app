import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, TimeSeriesSplit
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from src.connection.database import engine
from src.querys.querys_dictionary import query_reais_ton_primeiro_contrato


def detrending(df):    
    df['data'] = pd.to_datetime(df['data'])
    df['date_ordinal'] = df['data'].apply(lambda x: x.toordinal())

    # 2. Selecionar apenas a variável de tempo (date_ordinal)
    X = df[['date_ordinal']]  # <-- Usando somente date_ordinal
    y = df['reais_ton'].astype(float)

    # 3. Ajustar a regressão linear simples
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = LinearRegression()
    model.fit(X_scaled, y)

    # 4. Gerar a tendência (predição) para todos os pontos
    trend_values = model.predict(X_scaled)

    # 5. Subtrair a tendência da série original
    detrended_series = y - trend_values

    # 6. Ajuste final para manter o último valor inalterado (opcional)
    diferenca_ultimo_valor = trend_values[-1]
    df['detrending'] = detrended_series + diferenca_ultimo_valor
      
    return df
