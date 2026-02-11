from db.connection import fetch_dataframe

def peso_por_animal(codigo_animal: str):
    query = """
        SELECT
            c.data_coleta,
            p.peso
        FROM pesagem p
        JOIN coleta c
            ON p.id_coleta = c.id_coleta
        WHERE p.codigo_animal = %s
        ORDER BY c.data_coleta;
    """
    return fetch_dataframe(query, params=(codigo_animal,))

def peso_medio_por_coleta():
    query = """
        SELECT
            c.data_coleta,
            AVG(p.peso) AS peso_medio
        FROM pesagem p
        JOIN coleta c ON p.id_coleta = c.id_coleta
        GROUP BY c.data_coleta
        ORDER BY c.data_coleta;
    """

    return fetch_dataframe(query)

def peso_medio_por_sistema():
    query = """
        SELECT
            ra.sistema AS sistema,
            AVG(p.peso) AS peso_medio
        FROM pesagem p
        JOIN registro_animal ra ON ra.codigo = p.codigo_animal
        GROUP BY ra.sistema
        ORDER BY ra.sistema;
    """
    return fetch_dataframe(query)

def peso_medio_por_sistema_por_composicao():
    query = """
        WITH ultima_coleta AS (
            SELECT id_coleta
            FROM coleta
            ORDER BY data_coleta DESC
            LIMIT 1
        )
        SELECT
            ra.sistema,
            ra.composicao_racial,
            AVG(p.peso) AS peso_medio
        FROM pesagem p
        JOIN registro_animal ra
            ON ra.codigo = p.codigo_animal
        WHERE p.id_coleta = (SELECT id_coleta FROM ultima_coleta)
        GROUP BY
            ra.sistema,
            ra.composicao_racial
        ORDER BY
            ra.sistema,
            ra.composicao_racial;
    """
    
    return fetch_dataframe(query)

def distribuicao_parasitas():
    query = """
        SELECT parasita, count(parasita) as quantidade_parasita
        FROM parasita
        GROUP BY parasita
        ORDER BY parasita;
    """
    
    return fetch_dataframe(query)

def reatividade_media_por_composicao_por_sistema():
    query = """
    WITH ultima_coleta AS (
        SELECT id_coleta
        FROM coleta
        ORDER BY data_coleta DESC
        LIMIT 1
    )
    SELECT
        ra.sistema,
        ra.composicao_racial,
        AVG(r.reatividade) AS reatividade_media
    FROM reatividade r
    JOIN registro_animal ra
        ON ra.codigo = r.codigo_animal
    WHERE r.id_coleta = (SELECT id_coleta FROM ultima_coleta)
    GROUP BY
        ra.sistema,
        ra.composicao_racial
    ORDER BY
        ra.sistema,
        ra.composicao_racial;
    """
    
    return fetch_dataframe(query)