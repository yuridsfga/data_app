import pandas as pd
import sqlalchemy
from sqlalchemy import text
from src.connection.database import engine

query_primeiro_contrato_acucar = text("""
WITH ranked_data AS (
    SELECT 
        dc.data,
        c.nome_contrato,
        dc.anterior,
        c.vencimento,
        ROW_NUMBER() OVER (
            PARTITION BY dc.data 
            ORDER BY c.vencimento ASC
        ) AS rank_vencimento
    FROM dados_commodity dc
    INNER JOIN contrato c
        ON dc.id_contrato = c.id_contrato
    WHERE dc.data BETWEEN '2023-02-01' AND '2023-03-28'  -- Intervalo desejado
)
SELECT 
    data,
    nome_contrato,
    anterior,
    vencimento
FROM ranked_data
WHERE rank_vencimento = 1
""")


  