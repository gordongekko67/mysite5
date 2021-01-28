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

bp = Blueprint('form', __name__, url_prefix='/form')

@bp.route('/riceviform', methods=['GET', 'POST'])
def riceviform():
    if request.method == 'POST':
        nome = request.form['fname']
        cognome = request.form['lname']
        print(nome)
        print(cognome)
        return redirect(url_for('altri.scelta'))

@bp.route('/riceviform2', methods=['GET', 'POST'])
def riceviform2():
    if request.method == 'POST':
        nome = request.form['myForm']
        print(nome)
        return redirect(url_for('altri.scelta'))


# passaggio parametri in Flask da Html a Html
@bp.route('/lanciaForm', methods=['GET', 'POST'])
def lanciaForm():
    if request.method == 'POST':
        nome = request.form['fname2']
        cognome = request.form['lname2']
        campo = "prova"
        array = {'valore1', 'valore2', 'valore3'}

        # reperimento dati
        db = get_db()
        posts2 = db.execute(
            'SELECT id, title, created, autor '
            ' FROM libri '

        ).fetchall()

        return render_template('form/format2.html', value1= nome, value2 =  cognome, value3 = campo, value4 = array, value5 = posts2)

        # passaggio parametri in Flask da Html a Html

    @bp.route('/lanciacorr', methods=['GET', 'POST'])
    def lanciacorr():
        if request.method == 'POST':
            id = request.form['id']
            title = request.form['title']
            autor = request.form['autor']

            return render_template('form/format3.html', value1=id, value2=title, value3=autor)


