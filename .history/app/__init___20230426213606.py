from flask import Flask,render_template
import os
import sqlalchemy 
from yaml import load,Loader
from sqlalchemy.engine import URL
from sqlalchemy import event,text,DDL


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
        sqlalchemy.engine.url.URL(
            drivername="mysql+pymysql",
            username=os.environ.get('MYSQL_USER'),
            password=os.environ.get('MYSQL_PASSWORD'),
            database=os.environ.get('MYSQL_DB'),
            host=os.environ.get('MYSQL_HOST'),
            port = 3306,
            query = {}
        )
    )
    print(pool)
    return pool

trigger = DDL( """
        CREATE TRIGGER password_update_trigger 
        BEFORE UPDATE ON User 
        FOR EACH ROW 
        BEGIN 
            IF OLD.password != :old_pwd THEN 
                
                SET @message = 'Incorrect old password entered.'; 
            ELSEIF :new_pwd = OLD.password THEN 
                
                SET @message = 'New password cannot be the same as the old password.'; 
            ELSE 
                UPDATE User 
                SET NEW.password = :new_pwd 
                WHERE user_name = :user;
                SET @message = 'Password updated successfully.'; 
            END IF; 
        END;
        """)



app = Flask(__name__)
app.config['SECRET_KEY']  = 'team019'
db = init_connection_engine()




class User(db.Model):
    __tablename__ = 'User'
    user_name = db.Column(db.String(250), primary_key=True)
    password = db.Column(db.String(50))
    age= db.Column(db.Integer)
    sex = db.Column(db.String(10))

db.event.listen(User.__table__, 'after_create', trigger)



# To prevent from using a blueprint, we use a cyclic import
# This also means that we need to place this import here
# pylint: disable=cyclic-import, wrong-import-position
from app import routes








