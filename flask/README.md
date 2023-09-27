# Flask Introduction

This repo has been updated to work with `Python v3.8` and up.

### How To Run
(if no venv)
1. Install `virtualenv`:
```
$ pip install virtualenv
```

2. Open a terminal in the project root directory and run:(create a environment name env)
```
$ virtualenv env
```

3. Then run the command:
```
$ source env/bin/activate
```
(have venv)
4. Then install the dependencies:
```
$ (env) pip install -r requirements.txt
```

5. Finally start the web server:
```
$ (env) python app.py
```

<create a db>https://www.maxlist.xyz/2019/11/10/flask-sqlalchemy-setting/

1. (base) CindyMBA:Flask_for_Accounting andytseng$ source /Users/andytseng/project/Flask_for_Accounting/env/bin/activate

2. (env) (base) CindyMBA:Flask_for_Accounting andytseng$ python3

3. >>> from app import db

4. >>> db.create_all()

5. >>> exit()

This server will start on port 5000 by default. You can change this in `app.py` by changing the following line to this:

```python
if __name__ == "__main__":
    app.run(debug=True, port=<desired port>)
```

    <!-- tutorial in base.html
        {%   %}: bracket percent this is stuff like if-else statement for loops
        {{   }}: these are for things you want to be printed in I guess strings
        so this is basically going to take the code you write in here and it's
        going to give you the result of that as a string
    -->