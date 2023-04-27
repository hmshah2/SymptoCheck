from flask import Flask,render_template
import os
import sqlalchemy 
from yaml import load,Loader
from sqlalchemy.engine import URL
from sqlalchemy import event,text,DDL,Model


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
DELIMITER $$
        CREATE TRIGGER symptom_check_trigger 
        AFTER INSERT ON Search_Record
        FOR EACH ROW 
        BEGIN 
            SET@cnt = (SELECT COUNT(*)FROM Search_Record WHERE checkin_date = CURDATE());
            IF @cnt >= 3:
                SET @sym1 = (SELECT Symptom
                FROM Search_Record 
                GROUP BY symptom
                ORDER BY COUNT(symptom) DESC
                LIMIT 1
                );
            UPDATE Symptoms SET SymptomRank = 1 WHERE @sym1 = SymptomName;


            
            END IF;
        END$$
DELIMITER ;
        """)



app = Flask(__name__)
app.config['SECRET_KEY']  = 'team019'
db = init_connection_engine()



# To prevent from using a blueprint, we use a cyclic import
# This also means that we need to place this import here
# pylint: disable=cyclic-import, wrong-import-position
from app import routes








