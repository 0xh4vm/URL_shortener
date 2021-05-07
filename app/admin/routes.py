from flask import render_template, request, jsonify, redirect
from app.admin import bp
from app.databases.url import *
from app import db
import re
from datetime import datetime
import re


def _active(id):
    bad_url_obj = BadURL.query.get(id)
    if bad_url_obj is not None:
        db.session.delete(bad_url_obj)

def _inactive(id):
    if BadURL.query.get(id) is None:
        bad_url_obj = BadURL(url_id=id)
        db.session.add(bad_url_obj)

def _delete(id):
    o = URLAssociate.query.get(id)
    if o is not None:
        db.session.delete(o)

@bp.route('/', methods=['GET'])
def admin_view():
    return render_template('admin/index.html', urls=URLAssociate.query.all())

@bp.route('/active/<id>/', methods=['GET'])
def active(id):
    _active(id)
    db.session.commit()
    return redirect('/admin/')

@bp.route('/inactive/<id>/', methods=['GET'])
def inactive(id):
    _inactive(id)
    db.session.commit()
    return redirect('/admin/')

@bp.route('/delete/<id>/', methods=['GET'])
def delete(id):
    _delete(id)
    db.session.commit()
    return redirect('/admin/')

@bp.route('/active/', methods=['POST'])
def active_all():
    if not request.is_json:
        return jsonify({'status': 'fail', 'text': 'Что-то пошло не так...'})

    ids = request.json['ids']

    for id in ids:
        _active(id)
    db.session.commit()

    return redirect('/admin/')

@bp.route('/inactive/', methods=['POST'])
def inactive_all():
    if not request.is_json:
        return jsonify({'status': 'fail', 'text': 'Что-то пошло не так...'})

    ids = request.json['ids']

    for id in ids:
        _inactive(id)
    db.session.commit()

    return redirect('/admin/')

@bp.route('/delete/', methods=['POST'])
def delete_all():
    if not request.is_json:
        return jsonify({'status': 'fail', 'text': 'Что-то пошло не так...'})

    ids = request.json['ids']

    for id in ids:
        _delete(id)
    db.session.commit()

    return redirect('/admin/')

@bp.route('/domain_inactive/', methods=['POST'])
def domain_inactive():
    if not request.is_json:
        return jsonify({'status': 'fail', 'text': 'Что-то пошло не так...'})

    domain = request.json['domain']

    urls = URLAssociate.query.filter( 
        URLAssociate.long.op('~')(f"^{domain}/?")
    ).all()

    for url in urls:
        if domain[-1] == '/' or re.match(f"^{domain}/", url.long) or re.match(f"^{domain}$", url.long):
            _inactive(url.id)

    db.session.commit()    
    
    return redirect('/admin/')
    