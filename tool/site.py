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
from tool.utils import update
from tool.utils import process
from tool.utils import request_batch





bp = Blueprint('App', __name__)




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
    if request.method == 'POST':
        data = request.get_json()
        print(data)
    multi_labels = process(data)
    print(multi_labels)
    update(multi_labels,g.dataset)
    session['checkpoint'] = datetime.datetime.now()
    return redirect(url_for("App.index"))


@bp.route("/reload", methods = ["POST"])
def reload():
    if request.method == 'POST':
        data = request.get_json()
        print(data)
    multi_labels = process(data)
    session['checkpoint'] = None
    print("SALVANDO MARCAÇÕES - QUANDO RECARREGA/SAI DA PÁGINA")
    #labels = request.form.getlist("labels[]")
    #list_labels = [int(l) for l in labels]
    
    print(multi_labels)
    update(multi_labels,g.dataset)

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
