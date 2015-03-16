import datetime
import os

import numpy

from Bio import SeqIO

# HACK!!!
import sys
sys.path.append("../overlapy")
# END HACK
from overlapy.superimposer import Superimposer

from .application import application, db
from .utils import sendmail


class Job(db.Model):

    __tablename__ = 'jobs'

    id = db.Column(db.Integer, primary_key=True)
    first_pdb = db.Column(db.String, nullable=False)
    second_pdb = db.Column(db.String, nullable=False)
    first_pdb_chains = db.Column(db.String)
    second_pdb_chains = db.Column(db.String)
    email = db.Column(db.String, nullable=False)

    status = db.Column(db.String, nullable=False)

    completed_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, nullable=False)

    rmsd = db.Column(db.Float)

    def __init__(self, first_pdb, second_pdb, email, first_chains, second_chains):
        self.first_pdb = first_pdb
        self.second_pdb = second_pdb
        self.email = email

        self.first_pdb_chains = ",".join(first_chains)
        self.second_pdb_chains = ",".join(second_chains)

        self.created_at = datetime.datetime.now()
        self.status = "pending"

    def is_pending(self):
        return self.status == 'pending'

    def is_completed(self):
        return self.status == 'completed'

    def is_error(self):
        return self.status == 'error'

    def process(self):
        try:
            self.__process_overlapy()
        except Exception as e:
            self.status = 'error'
        else:
            self.status = 'completed'

        self.completed_at = datetime.datetime.now()

        db.session.add(self)
        db.session.commit()

        self.__send_mail()

        return True

    def save_pdb_files(self, first_pdb_file, second_pdb_file):
        uploads_path = application.config['UPLOADS_PATH']
        print(self.id)
        uploads_job_path = os.path.join(uploads_path, str(self.id))
        if not os.path.exists(uploads_job_path):
            os.makedirs(uploads_job_path)

        first_pdb_file.save(os.path.join(uploads_path, self.file_path(self.first_pdb)))
        second_pdb_file.save(os.path.join(uploads_path, self.file_path(self.second_pdb)))

    def file_path(self, file_name):
        return os.path.join(str(self.id), file_name)

    def upload_file_path(self, file_name):
        return os.path.join(application.config['UPLOADS_PATH'], self.file_path(file_name))

    def first_pdb_chains_list(self):
        return self.__split_chains(self.first_pdb_chains)

    def second_pdb_chains_list(self):
        return self.__split_chains(self.second_pdb_chains)

    # PRIVATE

    def __split_chains(self, chains):
        return [chain for chain in chains.split(",") if chain]

    def __process_overlapy(self):
        # perform superimposition
        superimposer = Superimposer()
        superimposer.parse(self.upload_file_path(self.first_pdb), self.upload_file_path(self.second_pdb))
        superimposer.select_chains(self.first_pdb_chains_list(), self.second_pdb_chains_list())

        superimposer.superimpose()

        # output matrix
        matrix = superimposer.rotation_matrix
        numpy.savetxt(self.upload_file_path("matrix.tsv"), matrix, delimiter="\t")

        # output superimposed PDB
        superimposer.save_superimposed_pdb(self.upload_file_path("superimposed.pdb"))

        # save to DB
        self.rmsd = superimposer.rmsd
        db.session.add(self)
        db.session.commit()

        # output alignment
        alignment = superimposer.get_multiple_sequence_alignment()
        with open(self.upload_file_path("alignment.clustal"), "w") as handle:
            count = SeqIO.write(alignment, handle, "clustal")

    def __send_mail(self):
        subject = "[Overlapy] Your petition has been processed"
        sender = "no-reply@overlapy.undeadpixels.net"
        recipient = self.email
        body = """
Dear user,

Your petition has been processed with status "{}". Please follow this link to obtain the results:

{}

Note: Your job will be removed in 24 hours.

Regards,

The overlapy team.

""".format(self.status, "http://overlapy.undeadpixels.net/jobs/{}".format(self.id))

        sendmail(sender, recipient, subject, body)

