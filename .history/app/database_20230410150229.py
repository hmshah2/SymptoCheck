"""Defines all the functions related to the database"""
from app import db

def fetch_todo() -> dict:
    """Reads all tasks listed in the todo table

    Returns:
        A list of dictionaries
    """

    conn = db.connect()
    query_results = conn.execute("Select * from tasks;").fetchall()
    conn.close()
    todo_list = []
    for result in query_results:
        item = {
            "id": result[0],
            "task": result[1],
            "status": result[2]
        }
        todo_list.append(item)

    return todo_list




# search in db for diseases
def find_sym(sym,sev) -> list:
    #Returns : list
    conn = db.connect()
    if type(sev) == NoneType:
        sev = "1"
    if type(sym) != NoneType:
        indicator = 1
        query = conn.execute("SELECT IllnessName FROM Has_Symptom WHERE SymptomName LIKE '%s' AND Severity = '%s' GROUP BY IllnessName ORDER BY COUNT(IllnessName)DESC LIMIT 5;").fetchall()
    conn.close()
    ill_list = []
    if indicator == 1:
        for result in query:
            ill_list.append(result)
    return ill_list

# register
def create_user(user:str,pwd:str,age:int,sex:str) -> None:
    conn = db.connect()
    if type(user) != NoneType:
        indicator = 1
        query = 'INSERT INTO User(user_name,password,age,sex) VALUES({},{},{},{})'.format(user,pwd,age,sex)
        conn.execute(query)
    conn.close()
    
# update_record
def update_record(user:str,sym:str,age:int,sex:str,sev:int) -> None:
    conn = db.connect()
    query_check = 'SELECT * FROM Records WHERE user_id = {} AND age = {} AND sex = {} AND trackable_type = "Symptom" AND trackable_name = {} and trackable_value = {}'.format(user,age,sex,sym,sev)
    if 

def update_task_entry(task_id: int, text: str) -> None:
    """Updates task description based on given `task_id`

    Args:
        task_id (int): Targeted task_id
        text (str): Updated description

    Returns:
        None
    """

    conn = db.connect()
    query = 'Update tasks set task = "{}" where id = {};'.format(text, task_id)
    conn.execute(query)
    conn.close()


def update_status_entry(task_id: int, text: str) -> None:
    """Updates task status based on given `task_id`

    Args:
        task_id (int): Targeted task_id
        text (str): Updated status

    Returns:
        None
    """

    conn = db.connect()
    query = 'Update tasks set status = "{}" where id = {};'.format(text, task_id)
    conn.execute(query)
    conn.close()


def insert_new_task(text: str) ->  int:
    """Insert new task to todo table.

    Args:
        text (str): Task description

    Returns: The task ID for the inserted entry
    """

    conn = db.connect()
    query = 'Insert Into tasks (task, status) VALUES ("{}", "{}");'.format(
        text, "")
    conn.execute(query)
    query_results = conn.execute("Select LAST_INSERT_ID();")
    query_results = [x for x in query_results]
    task_id = query_results[0][0]
    conn.close()

    return task_id


def remove_task_by_id(task_id: int) -> None:
    """ remove entries based on task ID """
    conn = db.connect()
    query = 'Delete From tasks where id={};'.format(task_id)
    conn.execute(query)
    conn.close()
