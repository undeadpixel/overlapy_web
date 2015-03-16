# Overlapy web interface

Overlapy is a Python 3 library to perform superimpositon of two protein structures in PDB format. This is a web implementation, using flask and SQLAlchemy to create a job queue and then a cron job that runs each job and sends an email when it's complete.

## Requirements to run it locally

You need to have installed Ruby >= 1.9 with the sass gem.
Also, you should use a virtualenv to locally install the requirements.txt file.

To run it locally you can follow these steps:

```
# I recommend using a virtualenv to manage dependencies!!
# install python libraries
pip install -r requirements.txt

# initialize database
python -c "import overlapy_web.models as models; models.db.create_all()"

# in another terminal, to compile sass files automatically
sass --watch overlapy_web/assets/scss:overlapy_web/static --scss --sourcemap=none

# in another terminal, to run the web server
python run.py
```

If you visit localhost:5000 you should see the website.
