import pandas as pd
import sqlalchemy
from sqlalchemy import text
from src.connection.database import engine

def query_primeiro_contrato_acucar(min_date, max_date, contrato: int): 
    query = text(f"""
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
            WHERE dc.data BETWEEN '{min_date}' AND '{max_date}'  -- Intervalo desejado
        )
        SELECT 
            data,
            nome_contrato,
            anterior,
            vencimento
        FROM ranked_data
        WHERE rank_vencimento = {contrato}
        """)
    
    return query

def query_contratos_ativos(min_date, max_date):
    query = text(f"""
        WITH contrato_diario AS (
            SELECT
                dc.data,
                c.nome_contrato,
                dc.anterior,
                c.vencimento,
                ROW_NUMBER() OVER (PARTITION BY dc.data ORDER BY c.vencimento ASC) AS row_num
            FROM dados_commodity dc
            INNER JOIN contrato c
                ON dc.id_contrato = c.id_contrato  -- Certifique-se de que há uma chave de relacionamento adequada
            WHERE dc.data BETWEEN '{min_date}' AND '{max_date}'
        )
        SELECT
            data,
            nome_contrato,
            anterior,
            vencimento
        FROM contrato_diario
    """)

    return query


def query_reais_ton_primeiro_contrato(min_date, max_date, contrato: int):
    query = text(f"""
    WITH reais_ton_prim AS (
    SELECT
        c.nome_contrato,
        dc.data,
        (dc.anterior * df.valor * 22.0562 * 1.042) AS reais_ton,
        ROW_NUMBER() OVER (
            PARTITION BY dc.data 
            ORDER BY c.vencimento ASC  -- Order by expiration date
        ) AS row_num
    FROM 
        dados_commodity dc
    INNER JOIN 
        contrato c ON dc.id_contrato = c.id_contrato
    INNER JOIN 
        dolar_futuro df ON c.vencimento = df.vencimento AND dc.data = df.data
    WHERE 
        dc.data BETWEEN '{min_date}' AND '{max_date}'
) 
SELECT 
    data,
    nome_contrato,
    reais_ton
FROM 
    reais_ton_prim
WHERE 
    row_num = {contrato}
ORDER BY data ASC;
    """)

    return query

def query_reais_ton(min_date, max_date):
    query = text(f"""
    SELECT
        c.nome_contrato,
        dc.data,
        (dc.anterior * df.valor * 22.0562 * 1.042) AS reais_ton
    FROM 
        dados_commodity dc
    INNER JOIN 
        contrato c ON dc.id_contrato = c.id_contrato
    INNER JOIN 
        dolar_futuro df ON c.vencimento = df.vencimento AND dc.data = df.data
    WHERE dc.data BETWEEN '{min_date}' AND '{max_date}'
    GROUP BY c.nome_contrato, dc.data, dc.anterior, df.valor;
    """)

    return query

def query_serie_inflacinada(min_date, max_date):
    query = text(f"""
    WITH ipca_adjusted AS (
    SELECT
        dc.data AS commodity_date,
        c.nome_contrato,
        dc.anterior,
        df.valor AS df_valor,
        EXP(
            SUM(
                LOG(1 + COALESCE(i.valor, 0)) 
                * CASE 
                    WHEN i.ipca_data = DATE_FORMAT(dc.data, '%Y-%m-01') 
                        THEN (DATEDIFF(LAST_DAY(dc.data), dc.data) + 1) / i.total_days_in_month
                    ELSE 1 
                END
            ) OVER (
                PARTITION BY c.nome_contrato, dc.data 
                ORDER BY i.ipca_data
                ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
            )
        ) AS inflation_factor
    FROM 
        dados_commodity dc
    INNER JOIN 
        contrato c ON dc.id_contrato = c.id_contrato
    INNER JOIN 
        dolar_futuro df ON c.vencimento = df.vencimento AND dc.data = df.data
    LEFT JOIN (
        SELECT 
            DATE_FORMAT(data, '%Y-%m-01') AS ipca_data,
            valor,
            DAY(LAST_DAY(data)) AS total_days_in_month
        FROM ipca
        WHERE valor > -1
    ) i ON i.ipca_data >= DATE_FORMAT(dc.data, '%Y-%m-01')
    WHERE 
        dc.data BETWEEN '{min_date}' AND '{max_date}'
    )
    SELECT
        nome_contrato,
        commodity_date AS data,
        -- Use MAX() to satisfy sql_mode=only_full_group_by (redundant here but safe)
        MAX(anterior * df_valor * 22.0462 * 1.042 * inflation_factor) AS reais_ton
    FROM 
        ipca_adjusted
    GROUP BY 
        nome_contrato, commodity_date, anterior, df_valor;  -- Include all non-aggregated columns    
    """)

    return query

# def query_inflacionar_ipca(min_date, max_date): 
#     try:
#         ano, mes, dia = min_date.split("-")

#         mes, dia = int(mes), int(dia)

#         dias_por_mes = {
#             1: 31,  # Janeiro
#             2: 28,  # Fevereiro (28 dias por padrão)
#             3: 31,  # Março
#             4: 30,  # Abril
#             5: 31,  # Maio
#             6: 30,  # Junho
#             7: 31,  # Julho
#             8: 31,  # Agosto
#             9: 30,  # Setembro
#             10: 31, # Outubro
#             11: 30, # Novembro
#             12: 31  # Dezembro
#         }

        
#         if dia != 1:
#             query = text(f"""
            
            



#             """)
            


  