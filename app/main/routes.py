from flask import render_template, request, jsonify, redirect
from app.main import bp
from app.databases.url import *
from app import db
import re
from datetime import datetime
import requests
import re


@bp.route('/', methods=['GET'])
@bp.route('/index/', methods=['GET'])
def index_view():
    return render_template('main/index.html')

@bp.route('/cut_url/', methods=['POST'])
def cut_url():
    if not request.is_json:
        return jsonify({'status': 'fail', 'text': 'Что-то пошло не так...'})

    data = request.json
    
    try:
        payload = re.findall(f'(https?://)([^$]+)', data['url'])[0]
    except:
        return jsonify({'status': 'fail', 'text': 'Неверный формат URL!'})

    response = requests.get(data['url'])
    if response.status_code // 100 == 4 or response.status_code // 100 == 5:
        return jsonify({'status': 'fail', 'text': 'Сайт не отвечает.'})

    saved_url = URLAssociate.query.with_entities(URLAssociate).filter(URLAssociate.long == payload[1]).first()

    if saved_url is not None:
        if len(saved_url.banned_datetime) == 0:
            return jsonify({'short_url': saved_url.short})
        else:
            return jsonify({'status': 'fail', 'text': 'Запрещенный URL!'})

    url_obj = URLAssociate(protocol=payload[0], long=payload[1])
    db.session.add(url_obj)
    db.session.commit()

    return jsonify({'short_url': url_obj.short})

@bp.route('/<short_url>')
def redirection(short_url):
    url = URLAssociate.query.filter_by(short=short_url).first()

    if url:
        if len(url.banned_datetime) == 0:
            return redirect(f"{url.protocol}{url.long}", code=302)
        else:
            return jsonify({'status': 'fail', 'text': 'Запрещенный URL!'})
    else:
        return f'<h1>Url {short_url} не существует</h1>'

