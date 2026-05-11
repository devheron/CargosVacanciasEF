import sqlite3
import os

def load_database(df):
    print('a salvar na database')

    db_path = '../database/db.sqlite'
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    conn = sqlite3.connect(db_path)

    df.to_sql(
        'projetos',
        conn,
        if_exists='replace',
        index=False
    )

    conn.commit()
    conn.close()

    print('dados foram salvos no sqlite')