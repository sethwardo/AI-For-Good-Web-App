import os
import json
import pickle
from os.path import join, dirname
from flask import Flask, render_template, request, redirect 
from flaskext.mysql import MySQL

# from app import create_app

# from dotenv import load_dotenv

# dotenv_path = join(dirname(__file__), '.env')  # Address of your .env file
# load_dotenv(dotenv_path)


#config_name = os.getenv('FLASK_CONFIG')
#app = create_app(config_name)
# app = Flask(__name__)
app = Flask(__name__, static_folder='static', static_url_path='')

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'insta_db'



# app = Flask(__name__, template_folder='templates')
mysql = MySQL()
mysql.init_app(app)

def exeStartMYSQL(filename):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        fd = open(filename, 'r')
        sqlFile = fd.read()
        fd.close()
        sqlCommands = sqlFile.split(';')

        for command in sqlCommands:
            try:
                if command.strip() != '':
                    cursor.execute(command)
            except IOError as msg:
                print("Command skipped: ", msg)
        conn.commit()
    except:
        return 'Something went wrong with the execution'

def read_pickle():
    pickle_objects = []
    with (open("./parsefile/htmlParsed.pkl", "rb")) as openfile:
        while True:
            try:
                pickle_objects.append(pickle.load(openfile))
            except EOFError:
                break
    return pickle_objects

def exeInsertDataMYSQL(pickle_data):
    # inputting data
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        for key, item in pickle_data[0].items():
            article_id = int(key)
            article_title = item["title"]
            article_author = item["author"]
            article_date = item["date"]
            graph = item["graph"]
            value = (article_id, article_title, article_author, article_date)
            sql = "INSERT INTO insta_db.article(id, title, author, publish_date) VALUES (%s,%s,%s,%s);"
            cursor.execute(sql, value)
            
            for key_2, item_2 in graph.items(): 
                value = (str(item_2),key_2)
                sql = "UPDATE insta_db.article SET graph = %s WHERE id = %s;"
                cursor.execute(sql,value)
        conn.commit()  
    except:
        return "Something went wrong with inserting the data"

@app.route("/old")
def main():
    try:
        exeStartMYSQL('init.sql')
        pickle_data = read_pickle()
        # return pickle_data[0]
        exeInsertDataMYSQL(pickle_data)
        return app.send_static_file("index.html")
    except Exception as fail:
        print("Something is wrong with your database user name or password {}".format(fail))
        return 'Something went wrong with starting the database'

    return "It was a success, here is the database information"

@app.route("/", methods=['GET', 'POST'])
def search():
    if request.method == "POST":
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            keyword = request.form['keyword']

            #search by keyword
            query = "select * from article where title like '%" + str(keyword) + "%';"
            cursor.execute(query)
            conn.commit()
            data = cursor.fetchall()

            # all in the search box will return all the tuples
            if keyword == 'all': 
                cursor.execute("SELECT * from article;")
                conn.commit()
                data = cursor.fetchall()
            return render_template('search_results.html', data=data)
        except Exception as fail:
            print("Something is wrong with your database user name or password {}".format(fail))
            return 'Something went wrong with the main database'
    return render_template('search_results.html')


@app.route("/graph", methods=['GET', 'POST'])
# @app.route("/graph")
def graph_generating():
    if request.method == "GET" or request.method == "POST":
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            article_id = request.args.get('id')

            #search by keyword
            query = "select graph from article where id = " + str(article_id) + ";"
            cursor.execute(query)
            conn.commit()
            data = cursor.fetchall()

            return render_template('graphs.html', graph = eval(data[0][0]))
        except Exception as fail:
            print("Something is wrong with your database user name or password {}".format(fail))
            return 'Something went wrong with the main database'
    return render_template('graphs.html')

    # return render_template('graphs.html')
    # return app.send_static_file('scalingNodesEdgesLabels.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
