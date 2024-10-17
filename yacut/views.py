from http import HTTPStatus

from flask import flash, redirect, render_template

from . import app
from .forms import UrlForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = UrlForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    try:
        return render_template(
            'index.html',
            form=form,
            short_url=URLMap.create_entry(
                form.original_link.data,
                form.custom_id.data or None).get_short_url())
    except ValueError as error:
        flash(str(error), HTTPStatus.BAD_REQUEST)
        return render_template('index.html', form=form)


@app.route('/<string:short>')
def get_short_url(short):
    return redirect(URLMap.get_or_404(short).original)
