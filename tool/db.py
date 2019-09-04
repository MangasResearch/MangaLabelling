import psycopg2
import psycopg2.extras

import glob
from os.path import join
import os

from flask import current_app, g
import click
from flask.cli import with_appcontext

def _get_faces():
    path = os.environ["FOLDER_IMGS"]
    faces = []
    for f in glob.glob(join(path, "*/*.jpg"), recursive=True):
        faces.append((f, 'unlabeled', False, False))
    return faces

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect(
                database = os.environ["POSTGRES_DB"],
                user = os.environ["POSTGRES_USER"],
                password = os.environ["POSTGRES_PW"],
                host = os.environ["POSTGRES_HOST"],
            )
    return g.db

def close_db(exception=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    sql = "INSERT INTO dataset (ref, label, busy, marked) VALUES %s"
    db = get_db()
    cursor = db.cursor()
    with current_app.open_resource('schema.sql') as f:
        faces = _get_faces()
        # cria a tabela no banco de dados
        cursor.execute(f.read().decode('utf8'))
        # insere dados no banco de dados
        psycopg2.extras.execute_values(cursor, sql, faces, template=None)
        db.commit()
    cursor.close()

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Apaga os dados existentes e cria uma nova tabela."""
    init_db()
    click.echo('Initialized the database.')
