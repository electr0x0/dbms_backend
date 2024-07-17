from django.db import connection

def execute_raw_sql(query, params=None):
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        if query.strip().lower().startswith("select"):
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
            return [dict(zip(columns, row)) for row in rows]

def execute_raw_sql2(query, params=None):
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        if cursor.description:
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
            return [dict(zip(columns, row)) for row in rows]
        return None