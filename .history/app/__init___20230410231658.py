from flask import Flask,render_template
import os
import sqlalchemy
from yaml import load,Loader
from sqlalchemy.engine import URL


def init_connection_engine():
    # detect env local or gcp
    if os.environ.get('GAE_ENV') != 'standard':
        try:
            variables = load(open("app.yaml"), Loader=Loader)
        except OSError as e:
            print("Make sure you have the app.yaml file setup")
            os.exit()

        env_variables = variables['env_variables']
        for var in env_variables:
            os.environ[var] = env_variables[var]

    pool = sqlalchemy.create_engine(
        sqlalchemy.engine.url.URL.create(
            drivername="mysql+pymysql",
            username=os.environ.get('MYSQL_USER'),
            password=os.environ.get('MYSQL_PASSWORD'),
            database=os.environ.get('MYSQL_DB'),
            host=os.environ.get('MYSQL_HOST')
        )
    )
    print(pool)
    return pool


app = Flask(__name__)
app.config['SECRET_KEY']  = 'team019'
db = init_connection_engine()
conn = db.connect()
results = conn.execute("Select * from Illness LIMIT 5;")
# we do this because results is an object, this is just a quick way to verify the content
print([x for x in results])
conn.close()
# To prevent from using a blueprint, we use a cyclic import
# This also means that we need to place this import here
# pylint: disable=cyclic-import, wrong-import-position
from app import routes








