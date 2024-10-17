from flask import flash, redirect, render_template

from . import app
from .forms import UrlForm
from .models import URLMap, MaxAttemptsExceededError


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = UrlForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    try:
        return render_template(
            'index.html',
            form=form,
            short_url=URLMap.create(
                form.original_link.data,
                form.custom_id.data or None).get_short_url())
    except MaxAttemptsExceededError as error:
        flash({str(error)})
        return render_template('index.html', form=form)
    except ValueError as error:
        flash(str(error))
        return render_template('index.html', form=form)


@app.route('/<string:short>')
def get_short_url(short):
    return redirect(URLMap.get_or_404(short).original)
