from PIL import Image
import uuid
from os.path import join
import os
import glob
from tool.db import get_db
import functools
import os.path
import psycopg2.extras
import random
import datetime

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


def resize_images(table):
    new_images = []
    for row in table:
        path = row[1]
        basewidth = 150
        filename = str(uuid.uuid4())
        img = Image.open(path)
        wpercent = (basewidth / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((basewidth, hsize), Image.ANTIALIAS)
        filepath = "static/temp/{}.bmp".format(filename)
        new_images.append(filepath)
        img.save(join("tool/", filepath))
    return new_images


def remove_images(imgs):
    print("Deletando arquivos!!!")
    for img in imgs:
        print(os.getcwd()+'/tool/'+img)
        if os.path.exists(os.getcwd()+'/tool/'+img):
            os.remove(os.getcwd()+'/tool/'+img)




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


def update(labels,curr_batch):
    print("UPDATE!!")
    print('curr_batch:',curr_batch)
    global update_query
    for i in range(len(labels)):
        print(labels[i][:2])
        if(labels[i]!='unlabeled' and labels[i][:2]!='[]'):
            curr_batch[i][2] = labels[i]
            curr_batch[i][4] = True
        else:
            curr_batch[i][3] = False
            curr_batch[i][2] = 'unlabeled'

    db = get_db()
    cursor = db.cursor()
    psycopg2.extras.execute_values (
        cursor, update_query,curr_batch
    )
    db.commit()
    cursor.close()


def process(data):
    senti_labels = data['labels']
    confi_labels = data['confidence']
    labels = []
    for d in range(len(senti_labels)):
        senti_labels[d]= ",".join(senti_labels[d])
        labels.append(senti_labels[d]+':'+str(confi_labels[d]))


    return labels

