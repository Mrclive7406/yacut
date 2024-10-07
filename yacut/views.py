from flask import flash, redirect, render_template

from . import app
from .forms import UrlForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = UrlForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    original_link = form.original_link.data
    short = form.custom_id.data or None
    url_map, result = URLMap.create_entry(original_link, short)
    if url_map is None:
        flash('Предложенный вариант короткой ссылки уже существует.',
              'error')
        return render_template('index.html', form=form)
    return render_template('index.html', form=form, short_url=result)


@app.route('/<string:url_short>')
def get_short_url(url_short):
    return redirect(URLMap.find_obj_or_404(url_short).original)
