import json

import psycopg2 as ps


def read_config(path: str = "config.json") -> dict:
    try:
        config = {}
        with open(path, "r") as f:
            config = json.loads(f.read())
        return config
    except Exception as e:
        print(f"Eroare la citire config. {e}")
        return config


def select_data_from_db(config: dict, sql_query: str = "select * from basket.teams") -> list:
    with ps.connect(**config) as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql_query)
            items = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            items_list = []
            for item in items:
                items_list.append(dict(zip(columns, item)))

            return items_list




if __name__ == '__main__':
    config = read_config()
    teams = select_data_from_db(config)
    print(teams)