import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, TimeSeriesSplit
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from src.connection.database import engine
from src.querys.querys_dictionary import query_reais_ton_primeiro_contrato


query = query_reais_ton_primeiro_contrato('2017-01-01', '2024-01-01')
with engine.connect() as connection:
    result = connection.execute(query)
    df = pd.DataFrame(result.fetchall(), columns=result.keys())


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
final_series = detrended_series + diferenca_ultimo_valor

# 7. Plotar resultados
plt.figure(figsize=(12, 6))
plt.plot(df['data'], y, label='Original')
plt.plot(df['data'], trend_values, label='Tendência Linear', linestyle='--')
plt.plot(df['data'], final_series, label='Série Detrended')
plt.legend()
plt.title('Detrending com Tendência Linear Simples')
plt.show()

# df['data'] = pd.to_datetime(df['data'])

# df['year'] = df['data'].dt.year
# df['month'] = df['data'].dt.month
# df['day'] = df['data'].dt.day
# df['dayofweek'] = df['data'].dt.dayofweek  # Monday=0 to Sunday=6
# df['dayofyear'] = df['data'].dt.dayofyear

# # Encode months (period = 12)
# df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12)
# df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12)

# # Encode day of week (period = 7)
# df['dayofweek_sin'] = np.sin(2 * np.pi * df['dayofweek'] / 7)
# df['dayofweek_cos'] = np.cos(2 * np.pi * df['dayofweek'] / 7)

# df['date_ordinal'] = df['data'].apply(lambda x: x.toordinal())

# # Select features (adjust based on model type)
# features = ['date_ordinal', 'month_sin', 'month_cos', 'dayofweek_sin', 'dayofweek_cos']
# X = df[features]
# y = df['reais_ton']
    
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# tscv = TimeSeriesSplit(n_splits=5)
# for train_index, test_index in tscv.split(X):
#     X_train, X_test = X.iloc[train_index], X.iloc[test_index]
#     y_train, y_test = y.iloc[train_index], y.iloc[test_index]

# y = y.astype(float)

# # Escalonamento dos dados
# scaler = StandardScaler()
# X_scaled = scaler.fit_transform(X)  # Escala todo o conjunto de dados

# # Treinamento do modelo com todos os dados
# model = LinearRegression()
# model.fit(X_scaled, y)

# # Previsões para todos os dados
# trend_values = model.predict(X_scaled)

# # Verifique os tamanhos
# print("Tamanho de y:", len(y))
# print("Tamanho de trend_values:", len(trend_values))

# # Detrending: subtrai a tendência dos valores originais
# detrended_series = y - trend_values

# # Normalização: mantém o último valor original
# last_value_diff = y.iloc[-1] - trend_values[-1]
# final_series = detrended_series + last_value_diff

# # Plot dos resultados
# plt.figure(figsize=(12, 6))
# plt.plot(df['data'], y, label='Original')
# plt.plot(df['data'], trend_values, label='Tendência Linear', linestyle='--')
# plt.plot(df['data'], final_series, label='Série Detrended')
# plt.legend()
# plt.title('Detrending da Série Temporal')
# plt.show()

# # Vetor de regressão (intercept + coeficientes)
# regression_vector = np.concatenate([[model.intercept_], model.coef_])
# print("Vetor de regressão:", regression_vector)