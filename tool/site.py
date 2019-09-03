import functools
import os.path
import psycopg2.extras
import uuid
import random
import datetime

from flask import (
    Blueprint, flash,jsonify,  g, redirect, render_template, request, session, url_for
)
from tool.db import get_db
from tool.utils import resize_images
from tool.utils import remove_images


request_query = """
        WITH subquery AS (
           SELECT * FROM dataset WHERE MARKED = False and BUSY = False LIMIT 5 
        )
        UPDATE dataset
        SET busy=TRUE
        FROM subquery
        WHERE dataset.id=subquery.id
        RETURNING dataset.*;
    """
update_query = """UPDATE dataset AS data
                   SET label=new.label, busy=False, marked=new.marked 
                   FROM (VALUES %s) AS new(id, ref, label, busy, marked) 
                   WHERE data.id=new.id;
                """


bp = Blueprint('App', __name__)


def request_batch():
    # Obter faces do BD
    global request_query 
    curr_batch = []
    db = get_db()
    cur = db.cursor()
    cur.execute("LOCK TABLE dataset IN ACCESS EXCLUSIVE MODE;")
    cur.execute(request_query)
    db.commit()
    batch = cur.fetchall()
    for row in batch:
       curr_batch.append(list(row))
    #session['curr_batch'] = curr_batch

    cur.close()
    return curr_batch


def update(labels):
    curr_batch = g.dataset
    global update_query
    for i in range(len(labels)):
        curr_batch[i][2] = labels[i]
        # Confirma quem foram as faces marcadas. 
        # Se label for 42, a face nao foi marcada
        if(labels[i]!=42):
            curr_batch[i][4] = True
        else:
            curr_batch[i][3] = False

    db = get_db()
    cursor = db.cursor()
    psycopg2.extras.execute_values (
        cursor, update_query,curr_batch
    )
    db.commit()
    cursor.close()



@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    dataset = session.get('dataset')
    curr_imgs = session.get('curr_imgs')
    if user_id is not None:
        g.user_id = user_id
        g.dataset = dataset
        g.curr_imgs = curr_imgs 
        g.checkpoint = session.get('checkpoint')


@bp.route('/')
def init():
    session.clear()
    session['user_id'] = str(uuid.uuid4())
    session['dataset'] = request_batch()
    session['checkpoint'] = None
    session['curr_imgs'] = resize_images(session.get('dataset'))
    session['indice'] = 0
    return redirect(url_for("App.index"))


@bp.route('/index')
def index(): 
    print("INDEX - ENTRANDO NO INDEX PARA REQUISITAR DADOS!!!")
    print('curr_batch: ',g.dataset)
    indice = session.get('indice')
    if(indice!=0):
        dataset  = request_batch()
        curr_imgs = resize_images(dataset)
    else:
        dataset = session.get('dataset')
        curr_imgs = session['curr_imgs']

    session['curr_imgs'] = curr_imgs
    session['dataset'] = dataset
    session['indice'] = 1

    return render_template('index.html', imgs=curr_imgs, page = "index")

@bp.route('/about')
def about(): 
    return render_template('about.html', page = "about")

@bp.route("/request_faces", methods = ["POST"])
def request_faces():
    session['checkpoint'] = datetime.datetime.now()
    return redirect(url_for("App.index"))


@bp.route("/reload", methods = ["POST"])
def reload():
    session['checkpoint'] = None
    print("SALVANDO MARCAÇÕES - QUANDO RECARREGA/SAI DA PÁGINA")
    labels = request.form.getlist("labels[]")
    list_labels = [int(l) for l in labels]
    
    print(list_labels)
    update(list_labels)

    print("REMOVENDO IMAGENS")
    curr_imgs = session.get('curr_imgs')
    remove_images(curr_imgs)
    curr_imgs = []

    session.pop('username', None)
    session.pop('curr_imgs', None)

    return jsonify({"STATUS": "OK"})
    
# @bp.after_request
# def add_header(response):
#     # response.cache_control.no_store = True
#     response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
#     response.headers['Pragma'] = 'no-cache'
#     response.headers['Expires'] = '-1'
#     return response
