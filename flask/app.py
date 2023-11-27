# Topic: High School English Textbook - Flask Web Searcher
# Tag: [Flask]
# Author: Wei-Hung, Tseng
# CreateDate: 2022/09/03
# SSH: andy@web.glis.ntnu.edu.tw
# Conda env: HSEngT
# Install: pip -r install requirement
# Complie: python -m py_compile filename.py
# Execute: 
#   Local: sudo python app.py
#   Remote: sudo python3 app.py
#   Go to: https://sam4.glis.ntnu.edu.tw:5501
# Reference:
#   How To Use an SQLite Database in a Flask Application:
#       https://www.digitalocean.com/community/tutorials/how-to-use-an-sqlite-database-in-a-flask-application

import sys
import sqlite3
from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__) # referencing this file

# tutorial:
# colon(:)
# three forward slash(///) for relative path
# four forward slash(////) for absolute path

# this is telling our app where our database is located
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/andytseng/project/Flask_for_Accounting/Accounting.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Accounting.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/andy/Documents/project/high_school_eng_textbook/flask/HSEngT.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///HSEngT.db'
# db = SQLAlchemy(app) # initialize database

levelMap = {
    'platinum'  : '1', 
    'diamond'   : '2', 
    'ascendant' : '3', 
    'immortal'  : '4', 
    'radiant'   : '5'
}

def get_db_connection():
    conn = sqlite3.connect('HSEngT.db')
    conn.row_factory = sqlite3.Row
    return conn

def login_legal(account, password):
    conn = get_db_connection()
    results = conn.execute(f'''
        SELECT 
            account, password, level 
        FROM 
            Account 
        WHERE 
            account = '{account}' 
        AND 
            password = '{password}'
    ''').fetchall()
    conn.close()
    # print(results[0][0], results[0][1])
    # print("len(results) = ", len(results), file=sys.stderr)
    if len(results) != 0: return True , results[0][2]
    else:                 return False, 0

def register_legal(account, password, permissions):
    ## If account already exist
    conn = get_db_connection()
    results = conn.execute(f'''
        SELECT 
            account 
        FROM 
            Account 
        WHERE 
            account = '{account}'
    ''').fetchall()
    conn.close()
    if results: return False, 'account have been register'
    
    ## If password already exist
    conn = get_db_connection()
    results = conn.execute(f'''
        SELECT 
            password 
        FROM 
            Account 
        WHERE 
            password = '{password}'
    ''').fetchall()
    conn.close()
    if results: return False, 'password have been register'

    if permissions not in ['platinum', 'diamond', 'ascendant', 'immortal', 'radiant']: return False, 'permissions code error'

    ## Insert
    conn = get_db_connection()
    conn.execute(f'''
        INSERT INTO 
            Account (account, password, level, createDate) 
        VALUES 
            ('{account}', '{password}', '{levelMap[permissions]}', DATETIME('now', '+8 hours'))
    ''')
    conn.commit()
    conn.close()
    return True, ''

def home_func1(root_type, root, word, version, level, lesson, frequency, permissions):
    ## Make select column & where condition string
    select_flag = [1]*7
    where_flag = [0]*7
    select_column = ''
    where_condition = ''
    col_map = {
        'root_type': 0,
        'root':      1,
        'word':      2,
        'version':   3,
        'level':     4,
        'lesson':    5,
        'frequency': 6
    }
    ban_sign = ['!', '！']

    if root_type in ban_sign: select_flag[col_map['root_type']] = 0
    else: 
        select_column += 'root_type'
        if root_type:
            where_condition += f"root_type LIKE '%{root_type}%' "
            where_flag[col_map['root_type']] = 1
    
    if root in ban_sign: select_flag[col_map['root']] = 0
    else: 
        if 1 in select_flag[:1]: select_column += ', '
        select_column += 'root'
        if root: 
            if 1 in where_flag[:1]: where_condition += 'AND '
            where_condition += f"root LIKE '%{root}%' "
            where_flag[col_map['root']] = 1

    if word in ban_sign: select_flag[col_map['word']] = 0
    else: 
        if 1 in select_flag[:2]: select_column += ', '
        select_column += 'word'
        if word: 
            if 1 in where_flag[:2]: where_condition += 'AND '
            where_condition += f"word LIKE '%{word}%' "
            where_flag[col_map['word']] = 1
    
    if version in ban_sign: select_flag[col_map['version']] = 0
    else: 
        if 1 in select_flag[:3]: select_column += ', '
        select_column += 'version'
        if version: 
            if 1 in where_flag[:3]: where_condition += 'AND '
            where_condition += f"version = '{version}' "
            where_flag[col_map['version']] = 1

    ## If level input = '!'
    if level in ban_sign: select_flag[col_map['level']] = 0
    else: 
        if 1 in select_flag[:4]: select_column += ', '
        select_column += 'level'
        
        if 1 in where_flag[:4]: where_condition += 'AND '
        ## If level have input
        if level:
            ## Permissions pass
            if permissions >= level[-1]: where_condition += f"level = '{level}' "
            else:                        where_condition += f"level = 'permissionDeny' "
        ## If level = ''
        else:
            where_condition += f"level <= 'B{permissions}' "
        where_flag[col_map['level']] = 1
    
    if lesson in ban_sign: select_flag[col_map['lesson']] = 0
    else: 
        if 1 in select_flag[:5]: select_column += ', '
        select_column += 'lesson'
        if lesson: 
            if 1 in where_flag[:5]: where_condition += 'AND '
            where_condition += f"lesson = '{lesson}' "
            where_flag[col_map['lesson']] = 1
    
    if frequency in ban_sign: select_flag[col_map['frequency']] = 0
    else: 
        if 1 in select_flag[:6]: select_column += ', '
        select_column += 'frequency'
        if frequency: 
            if 1 in where_flag[:6]: where_condition += 'AND '
            where_condition += f"frequency > '{frequency}' "
            where_flag[col_map['frequency']] = 1

    # print("flag=", flag, file=sys.stderr)
    conn = get_db_connection()
    ## [SELECT, FROM, WHERE, GROUP BY, ORDER BY]
    results = conn.execute(f'''
        SELECT DISTINCT 
            {select_column} 
        FROM
            HSEngT 
        WHERE
            {where_condition} 
        ORDER BY
            {select_column}
    ''').fetchall()
    conn.close()
    return results

@app.route('/', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        inputList = ['']*2
        errorMessage = ''
        return render_template('login.html', inputList = inputList, errorMessage = errorMessage)
    else:
        account = request.form['account'].strip()
        password = request.form['password'].strip()
        inputList = [account, password]
        status, permissions = login_legal(account, password)
        if status:
            inputList = ['']*7
            return render_template('home.html', inputList = inputList, permissions = permissions)
        else:
            errorMessage = 'Input error or you have to register'
            return render_template('login.html', inputList = inputList, errorMessage = errorMessage)

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        inputList = ['']*3
        errorMessage = ''
        return render_template('register.html', inputList = inputList, errorMessage = errorMessage)
    else:
        account = request.form['account'].strip()
        password = request.form['password'].strip()
        permissions = request.form['permissions'].strip()
        inputList = [account, password, permissions]
        status, errorMessage = register_legal(account, password, permissions)
        if status:
            inputList = ['']*7
            return render_template('home.html', inputList = inputList, permissions = levelMap[permissions])
        else:
            return render_template('register.html', inputList = inputList, errorMessage = errorMessage)

@app.route('/home', methods=['POST', 'GET'])
def home():
    ## HSEngT.db
    ## root_type, root, word, version, level, lesson, frequency
    if request.method == 'POST': ## when you click submit button
        ## Get data
        root_type = request.form['root_type'].strip()
        root = request.form['root'].strip()
        word = request.form['word'].strip()
        version = request.form['version'].strip()
        level = request.form['level'].strip()
        lesson = request.form['lesson'].strip()
        frequency = request.form['frequency'].strip()
        permissions = request.form['permissions'].strip()
        ## Create inputList
        inputList = [root_type, root, word, version, level, lesson, frequency]
        # inputList = [word, version, level, lesson, frequency]
        if frequency:
            if frequency != '!' and frequency != '！': int(frequency)
        
        results = home_func1(root_type, root, word, version, level, lesson, frequency, permissions)

        return render_template('home.html', inputList=inputList, permissions = permissions, results=results, result_num = len(results))
    else:
        # root_type = ''; root = ''; word = ''; version = ''; level = ''; lesson = ''; frequency = ''
        # inputList = [root_type, root, word, version, level, lesson, frequency]
        inputList = ['']*7
        return render_template('home.html', inputList=inputList, permissions = permissions)
    
'''Some example
## Insert
conn = get_db_connection()
conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                (title, content))
conn.commit()
conn.close()
return redirect(url_for('index'))



## Select
def get_post(post_id):
conn = get_db_connection()
post = conn.execute('SELECT * FROM posts WHERE id = ?',
                    (post_id,)).fetchone()
conn.close()
if post is None:
    abort(404)
return post



## Accounting.db
@app.route('/delete/<int:id>')
def delete(id):
    # this is going to attempt to get that task by the id and if it doesn't
    #   exist it's just going to 404
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    results = Todo.query.get_or_404(id)

    if request.method == 'POST':
    #if request.method == 'GET':
        results.class_item = request.form['class_item']
        results.objects = request.form['objects']
        results.price = request.form['price']

        try:# don't have to add or delete or anything we just have to commit because 
            # we set the content right here(task.content = request.form['content'])
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', results=results)
'''

if __name__ == "__main__":
    # app.run(debug=True)
    ## if on remote this have to be comment
    app.run(host='localhost', port=5502, debug=True)
    
    ## For deploy
    '''
        To open port 5501, run:
        1. go to remote(ssh: web)
        2. $ sudo ufw allow 5501
        3. $ sudo python3 app.py           # for test
        4. $ nohup sudo python3 app.py &   # for deploy

        p.s.
        get the process ID of the process that is running on the specified port.
            $ sudo lsof -i :5501
        remove it
            $ sudo kill -9 xxxx
    '''

    context = (
        '/etc/letsencrypt/live/sam4.glis.ntnu.edu.tw/fullchain.pem',
        '/etc/letsencrypt/live/sam4.glis.ntnu.edu.tw/privkey.pem'
        )
    # app.run(host='0.0.0.0', port=5501, ssl_context=context, debug=True)
    # app.run(host='0.0.0.0', port=5501, ssl_context=context, debug=False)