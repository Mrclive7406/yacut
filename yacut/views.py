import random
from string import ascii_letters, digits
from flask import render_template, redirect, flash, url_for
from settings import (MAIN_URL, MAIN_PAGE_TEMPLATE, MAX_GENERATED_LENGTH,
                      STRING_URL_SHORTS)
from . import app, db
from .models import URLMap
from .forms import UrlForm


def check_unique_short_id(short):
    return bool(URLMap.query.filter_by(short=short).first())


def get_unique_short_id():
    letters_and_digits = ascii_letters + digits
    rand_string = ''.join(random.sample(letters_and_digits,
                                        MAX_GENERATED_LENGTH))
    if check_unique_short_id(rand_string):
        get_unique_short_id()
    return rand_string


@app.route(MAIN_URL, methods=['GET', 'POST'])
def index_view():
    form = UrlForm()
    if form.validate_on_submit():
        url_short = form.custom_id.data
        if not url_short:
            url_short = get_unique_short_id()
        if URLMap.query.filter_by(short=url_short).first() is not None:
            flash('Предложенный вариант короткой ссылки уже существует.',
                  'error')
            return render_template(MAIN_PAGE_TEMPLATE, form=form)
        short_link = URLMap(
            original=form.original_link.data,
            short=url_short
        )
        db.session.add(short_link)
        db.session.commit()
        short_url = url_for('get_short_url',
                            url_short=url_short, _external=True)
        flash(short_url, 'get_link')
    return render_template(MAIN_PAGE_TEMPLATE, form=form)


@app.route(STRING_URL_SHORTS)
def get_short_url(url_short):
    short_link = URLMap.query.filter_by(short=url_short).first_or_404()
    return redirect(short_link.original)
