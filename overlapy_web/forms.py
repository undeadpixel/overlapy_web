import flask_wtf
from flask_wtf.file import FileField, FileAllowed, FileRequired

from wtforms import TextField, SelectMultipleField
from wtforms.validators import Email

from werkzeug import secure_filename

from .models import Job, db

# overriden form item
class TagsField(SelectMultipleField):
    def pre_validate(self, form):
        pass

class SubmitForm(flask_wtf.Form):
    first_pdb = FileField('First PDB', [FileRequired(), FileAllowed(['pdb'], 'PDB only')])
    second_pdb = FileField('Second PDB', [FileRequired(), FileAllowed(['pdb'], 'PDB only')])

    first_pdb_chains = TagsField("First PDB chains", choices=[])
    second_pdb_chains = TagsField("Second PDB chains", choices=[])

    email = TextField('E-Mail', [Email()])

    recaptcha = flask_wtf.RecaptchaField("Security check")

    def process_job(self):
        first_pdb, second_pdb = self.__get_secure_pdb_filenames()

        # save Job
        job = Job(first_pdb, second_pdb, self.email.data, self.first_pdb_chains.data, self.second_pdb_chains.data)
        db.session.add(job)
        db.session.commit()
        job.save_pdb_files(self.first_pdb.data, self.second_pdb.data)

        return job

    # PRIVATE

    def __get_secure_pdb_filenames(self):
        first_pdb = secure_filename(self.first_pdb.data.filename)
        second_pdb = secure_filename(self.second_pdb.data.filename)
        return (first_pdb, second_pdb)


