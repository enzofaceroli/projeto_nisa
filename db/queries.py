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
            AVG(p.peso) AS valor
        FROM pesagem p
        JOIN coleta c ON p.id_coleta = c.id_coleta
        GROUP BY c.data_coleta
        ORDER BY c.data_coleta;
    """

    return fetch_dataframe(query)

def peso_medio_por_sistema():
    query = """
        SELECT
            ra.sistema AS categoria,
            AVG(p.peso) AS valor
        FROM pesagem p
        JOIN registro_animal ra ON ra.codigo = p.codigo_animal
        GROUP BY ra.sistema
        ORDER BY ra.sistema;
    """
    return fetch_dataframe(query)
