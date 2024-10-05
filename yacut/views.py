from flask import flash, redirect, render_template, url_for

from . import app
from .forms import UrlForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = UrlForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    short = form.custom_id.data or URLMap.get_unique_short_id()
    if URLMap.is_short_id_exists(short):
        flash('Предложенный вариант короткой ссылки уже существует.',
              'error')
        return render_template('index.html', form=form)
    URLMap.create_entry(form.original_link.data, short)
    short_url = url_for('get_short_url',
                        url_short=short, _external=True)
    return render_template('index.html', form=form, short_url=short_url)


@app.route('/<string:url_short>')
def get_short_url(url_short):
    return redirect(URLMap.find_obj_or_404(url_short).original)
