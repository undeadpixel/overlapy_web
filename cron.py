#!/usr/bin/env python3

import os, os.path

from overlapy_web.models import Job, db

LOCK_FILE = "/tmp/overlapy_cron.lock"

# check if cron is running
if os.path.isfile(LOCK_FILE):
    exit(0)
else:
    # create temp lock file
    lock_file = open(LOCK_FILE, "w+")
    lock_file.close()

pending_jobs = Job.query.filter_by(status="pending").order_by(Job.created_at)

for job in pending_jobs:
    job.process()

os.remove(LOCK_FILE)
