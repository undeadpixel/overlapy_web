from flask import render_template, redirect, url_for, abort, send_file
from werkzeug.security import safe_join

from .application import application
from .models import Job
from .forms import SubmitForm

@application.route('/')
def index():
    form = SubmitForm()
    return render_template("index.html", form=form)

@application.route('/', methods=['POST'])
def submit_form():
    form = SubmitForm()
    if form.validate_on_submit():
        job = form.process_job()
        if job:
            return redirect(url_for('show_job', job_id=job.id))
        else:
            abort(403)
    else:
        return render_template("index.html", form=form)

@application.route('/jobs/<int:job_id>')
def show_job(job_id):
    job = Job.query.get(job_id)
    if job is None:
        abort(404)
    else:
        return render_template("show_job.html", job=job)

@application.route('/uploads/<path:file_name>')
def uploads(file_name):
    safe_filename = safe_join(application.config['UPLOADS_PATH'], file_name)
    try:
        return send_file(safe_filename, as_attachment=True)
    except:
        abort(404)

