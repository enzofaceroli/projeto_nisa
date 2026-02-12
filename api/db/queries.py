from api.db.connection import fetch_dataframe

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

def diferenca_peso_por_sistema_por_composicao():
    query = """
        WITH primeira_coleta AS (
            SELECT id_coleta
            FROM coleta
            ORDER BY data_coleta ASC
            LIMIT 1
        ), 
        
        ultima_coleta AS (
            SELECT id_coleta
            FROM coleta
            ORDER BY data_coleta DESC
            LIMIT 1
        ),
        
        peso_primeira AS (
            SELECT ra.sistema, 
            ra.composicao_racial,
            AVG (p.peso) as peso_medio_primeira
            
            FROM pesagem p
            JOIN registro_animal ra
                ON ra.codigo = p.codigo_animal
                
            WHERE p.id_coleta = (SELECT id_coleta FROM primeira_coleta)
            GROUP BY
                ra.sistema,
                ra.composicao_racial
        ),
        
        peso_ultima AS (
            SELECT ra.sistema, 
            ra.composicao_racial,
            AVG (p.peso) as peso_medio_ultima
            
            FROM pesagem p
            JOIN registro_animal ra
                ON ra.codigo = p.codigo_animal
                
            WHERE p.id_coleta = (SELECT id_coleta FROM ultima_coleta)
            GROUP BY
                ra.sistema,
                ra.composicao_racial
        )
        
        SELECT u.sistema,
        u.composicao_racial,
        u.peso_medio_ultima - p.peso_medio_primeira as diferenca_peso
        
        FROM peso_ultima u
        JOIN peso_primeira p
        ON
            p.sistema = u.sistema
            AND p.composicao_racial = u.composicao_racial
        
        ORDER BY
            u.sistema,
            u.composicao_racial;
    """
    
    return fetch_dataframe(query)

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

def reatividade_media_por_sistema_por_composicao():
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

def distribuicao_parasitas_por_sistema():
    query = """
    WITH ultima_coleta AS (
        SELECT id_coleta
        FROM coleta
        ORDER BY data_coleta DESC
        LIMIT 1
    )
    SELECT
        ra.sistema,
        p.parasita,
        COUNT(DISTINCT p.codigo_animal) AS qtd_animais
    FROM parasita p
    JOIN registro_animal ra
        ON ra.codigo = p.codigo_animal
    WHERE p.id_coleta = (SELECT id_coleta FROM ultima_coleta)
    GROUP BY
        ra.sistema,
        p.parasita
    ORDER BY
        ra.sistema,
        p.parasita;
    """
    df = fetch_dataframe(query)
    df['parasita'] = df['parasita'].astype(str)
    
    return df