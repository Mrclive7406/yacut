from flask import flash, redirect, render_template, url_for

from . import app
from .forms import UrlForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = UrlForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    try:
        url_map = URLMap.create_entry(form.original_link.data,
                                      form.custom_id.data or None)
    except Exception:
        flash('Предложенный вариант короткой ссылки уже существует.',
              'error')
        return render_template('index.html', form=form)
    short_url = url_for('get_short_url',
                        short=url_map.short, _external=True)
    return render_template('index.html', form=form, short_url=short_url)


@app.route('/<string:short>')
def get_short_url(short):
    return redirect(URLMap.get_or_404(short).original)
