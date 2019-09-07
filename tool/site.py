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

# Entrar na aplicação
@bp.route('/')
def login():
    print("LOGIN!!")
    if('user_id' in session):
        print('There is a user online, going for index')
        return redirect(url_for("App.index"))
    session.clear()
    session['user_id'] = str(uuid.uuid4()) # 1
    #if(not 'curr_imgs' in session):
    session['dataset'] = request_batch() # 2
    # session['checkpoint'] = None
    session['curr_imgs'] = resize_images(session.get('dataset')) # 3
    session['indice'] = 0

    #print(g.curr_imgs)
    #return render_template('index.html', page = "index")
    return redirect(url_for("App.index"))


@bp.before_app_request
def load_logged_in_user():
    print("LOAD LOGGED!!")
    """
    registers a function that runs before the view function,
    no matter what URL is requested. load_logged_in_user
    checks if a user id is stored in the session and gets 
    that user’s data from the database.
    """
    user_id = session.get('user_id')
    dataset = session.get('dataset')
    if('curr_imgs' in session):
        curr_imgs = session.get('curr_imgs')
    else:
       print("Não ha curr imgs")
    """
    if user_id is not None:
        g.user_id = user_id
        g.dataset = dataset
        g.curr_imgs = curr_imgs 
        # g.checkpoint = session.get('checkpoint')
    else:
        g.user_id = None
    """
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        #if g.user_id is None:
        if 'user_id' not in session:
            return redirect(url_for('App.login'))

        return view(**kwargs)

    return wrapped_view

@bp.route('/index')
@login_required
def index(): 
    print("INDEX - ENTRANDO NO INDEX PARA REQUISITAR DADOS!!!")
    curr_imgs = session.get('curr_imgs')
    print(curr_imgs)
    return render_template('index.html', page = "index")


@bp.route("/getData", methods=['GET'])
def getData():

    flag = request.args.get('flag')
    print('GET DATA!!!')
    if(not 'curr_imgs' in session ):
        print("ONE")
        session['dataset'] = request_batch()
        session['curr_imgs'] = resize_images(session.get('dataset'))
        curr_imgs = session.get('curr_imgs')
        return jsonify({ 'imgs': curr_imgs})
    return jsonify({ 'imgs': session.get('curr_imgs')})

@bp.route('/about')
def about(): 
    return render_template('about.html', page = "about")

@bp.route("/request_faces", methods = ["POST"])
def request_faces():
    print("REQUEST FACES!!")
    print("removendo imagens antigas")
    curr_imgs = session.get('curr_imgs')
    dataset = session.get('dataset')
    print("antigo batch de images:",curr_imgs)
    remove_images(curr_imgs)
    curr_imgs = []
    if request.method == 'POST':
        data = request.get_json()
        print(data)
    multi_labels = process(data)
    print(multi_labels)
    update(multi_labels,dataset)
    # Atualizar dados da sessão
    session['dataset'] = request_batch()
    curr_imgs = resize_images(session.get('dataset'))
    session['curr_imgs'] = curr_imgs 
    print("novo batch de images:",curr_imgs)
    # session['checkpoint'] = datetime.datetime.now()
    # return redirect(url_for("App.index"))
    return jsonify({ 'imgs': session['curr_imgs']})
"""
@bp.route("/reload", methods = ["POST"])
def reload():
    print("RELOAD!!!")
    if request.method == 'POST':
        data = request.get_json()
        print(data)
    multi_labels = process(data)
    session['checkpoint'] = None
    print("SALVANDO MARCAÇÕES - QUANDO RECARREGA/SAI DA PÁGINA")
    #labels = request.form.getlist("labels[]")
    #list_labels = [int(l) for l in labels]
    
    print(multi_labels)
    if('dataset' in session):
        update(multi_labels,g.dataset)

        print("REMOVENDO IMAGENS")
        curr_imgs = session.get('curr_imgs')
        remove_images(curr_imgs)
        curr_imgs = []
    
    session.clear()
    return jsonify({"STATUS": "OK"})

    return redirect(url_for("App.index"))
"""
@bp.after_request
def add_header(response):
    # response.cache_control.no_store = True
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

