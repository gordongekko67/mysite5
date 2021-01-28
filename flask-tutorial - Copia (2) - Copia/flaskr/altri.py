import functools
import json
#import pycurl
from io import BytesIO


import requests
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

import  paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
from flaskr.auth import login_required
from flaskr.blog import get_post
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('altri', __name__, url_prefix='/altri')


def sendmsgMqtt():
    # inizialize MQTT
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set("fkjqkoul", "wK0aUWpQWS35")
    client.connect("tailor.cloudmqtt.com", 16434, 60)
    client.subscribe("Tutorial2/#", 1)
    client.publish("Tutorial2", "avanti")


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("Tutorial2/#")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print("Message received-> " + msg.topic + " " + str(msg.payload))  # Print a received msg
    if msg.payload.decode() == "prova":
        print("Robot avanti")


def on_publish(client, userdata, msg):
    print("Message published-> " + msg.topic + " " + str(msg.payload))  # Print a received msg


@bp.route('/inserimentovid', methods=['GET', 'POST'])
def insert():
    session.clear()
    return render_template('altri/inserimento.html')


@bp.route('/scelta')
def scelta():
    session.clear()
    return render_template('altri/scelta.html')

@bp.route('/visual', methods=['GET', 'POST'])
def visua():
    db = get_db()
    posts = db.execute(
        'SELECT id, title, created, autor '
        ' FROM libri '

    ).fetchall()

    return render_template('altri/index.html', posts=posts)

@bp.route('/visual2', methods=['GET', 'POST'])
def visua2():
    db = get_db()
    posts2 = db.execute(
        'SELECT id, title, created, autor '
        ' FROM libri '

    ).fetchall()
    return render_template('altri/index3.html', posts=posts2)






@bp.route('/inserimento', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
            title1 = request.form['titolo']
            autore1 = request.form['autore']
            error = None

            if not title1:
                error = 'Title is required.'

            if error is not None:
                flash(error)
            else:
                db = get_db()
                db.execute(
                    'INSERT INTO libri (title, autor,  author_id)'
                    ' VALUES (?, ?, ?)',
                    (title1, autore1, 10)
                   )

                db.commit()

    return redirect(url_for('altri.scelta'))


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    db = get_db()
    post = get_db().execute(
        'SELECT id, author_id, title, autor, created '
        ' FROM libri'
        ' WHERE id = ?',
        (id,)
    ).fetchone()
    return render_template('altri/updatelibri.html', posts=post)

@bp.route('/<int:id>/updaterec', methods=('GET', 'POST'))
@login_required
def updaterec(id):
    db = get_db()
    post = get_post(id)
    if request.method == 'POST':
        titl1 = request.form['title']
        autor1 = request.form['autor']
        error = None

        if not titl1:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE libri SET title = ?, autor = ?'
                ' WHERE id = ?',
                (titl1, autor1, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)



@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM libri WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('altri.scelta'))

@bp.route('/chiamataREST', methods=['GET', 'POST'])
def chiamataREST():
    return "Chiamata REST"


@bp.route('/riceviRequest', methods=['GET', 'POST'])
def riceviRequest():
    if request.method == 'POST':
        payload = {'key1': 'value1', 'key2': ['value2', 'value3']}
        r =requests.get('https://httpbin.org/get', params=payload)
        print(r.url)
        print(r)
        print ("ho ricevuto i dati")
    return "RICEVUTI   DATI"


@bp.route('/lancioJson', methods=['GET', 'POST'])
def lancioJson():
    url = 'https://www.w3schools.com/python/demopage.php'
    headers = {"content-type": "application/json", "Accept-Charset": "UTF-8"}
    myobj = {'somekey': 'somevalue'}
    x = requests.post(url, data=myobj,  headers=headers )
    return "Chiamata post  eseguita "

@bp.route('/chiamataCurl', methods=['GET', 'POST'])
def chiamataCurl():
    url = "https://postman-echo.com/post"
    headers = {"content-type": "application/json", "Accept-Charset": "UTF-8"}
    r = requests.post(url, data={"sample": "data"}, headers=headers)
    return "Chiamata curl eseguita "



@bp.route('/robotAvanti', methods=['GET', 'POST'])
def robotAvanti():
    if request.method == 'GET':
        sendmsgMqtt()
        return render_template('altri/scelta.html')

@bp.route('/letturaFtp', methods=['GET', 'POST'])
def letturaFtp():
    if request.method == 'GET':
        sendmsgMqtt()
        return render_template('altri/scelta.html')

@bp.route('/formato', methods=['GET', 'POST'])
def formato():
    if request.method == 'GET':
        return render_template('form/format.html')
