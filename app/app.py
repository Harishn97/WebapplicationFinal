from typing import List, Dict
import simplejson as json
from flask import Flask, request, Response, redirect
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'BMI'
mysql.init_app(app)


@app.route('/', methods=['GET'])
def index():
    user = {'username': 'BMI Project'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM freshman_kgs')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, people=result)


@app.route('/view/<int:ppl_id>', methods=['GET'])
def record_view(ppl_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM freshman_kgs WHERE id=%s', ppl_id)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', people=result[0])


@app.route('/edit/<int:ppl_id>', methods=['GET'])
def form_edit_get(ppl_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM freshman_kgs WHERE id=%s', city_id)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', people=result[0])


@app.route('/edit/<int:ppl_id>', methods=['POST'])
def form_update_post(ppl_id):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('Sex'), request.form.get('Weight_Sep'), request.form.get('Weight_Apr'),
                 request.form.get('BMI_Sep'), request.form.get('BMI_Apr'), ppl_id)
    sql_update_query = """UPDATE freshman_kgs t SET t.Sex = %s, t.Weight_Sep = %s, t.Weight_Apr = %s, t.BMI_Sep = 
        %s, t.BMI_Apr = %s WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

@app.route('/people/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New People Form')


@app.route('/people/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('Sex'), request.form.get('Weight_Sep'), request.form.get('Weight_Apr'),
                 request.form.get('BMI_Sep'), request.form.get('BMI_Apr'))
    sql_insert_query = """INSERT INTO freshman_kgs (Sex,Weight_Sep,Weight_Apr,BMI_Sep,BMI_Apr) VALUES (%s, %s,%s, %s,%s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

@app.route('/delete/<int:ppl_id>', methods=['POST'])
def form_delete_post(ppl_id):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM freshman_kgs WHERE id = %s """
    cursor.execute(sql_delete_query, ppl_id)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/api/v1/people', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM freshman_kgs')
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/people/<int:ppl_id>', methods=['GET'])
def api_retrieve(ppl_id) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM freshman_kgs WHERE id=%s', ppl_id)
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/people/<int:ppl_id>', methods=['PUT'])
def api_edit(ppl_id) -> str:
    cursor = mysql.get_db().cursor()
    content = request.json
    inputData = (content['Sex'], content['Weight_Sep'], content['Weight_Apr'],
                 content['BMI_Sep'], content['BMI_Apr'],ppl_id)
    sql_update_query = """UPDATE freshman_kgs t SET t.Sex = %s, t.Weight_Sep = %s, t.Weight_Apr = %s, t.BMI_Sep = 
        %s, t.BMI_Apr = %s WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp

@app.route('/api/v1/people', methods=['POST'])
def api_add() -> str:

    content = request.json

    cursor = mysql.get_db().cursor()
    inputData = (content['Sex'], content['Weight_Sep'], content['Weight_Apr'],
                 content['BMI_Sep'], content['BMI_Apr'], request.form.get('fldPopulation'))
    sql_insert_query = """INSERT INTO freshman_kgs (Sex,Weight_Sep,Weight_Apr,BMI_Sep,BMI_Apr) VALUES (%s, %s,%s, %s,%s,) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=201, mimetype='application/json')
    return resp

@app.route('/api/v1/people/<int:ppl_id>', methods=['DELETE'])
def api_delete(ppl_id) -> str:
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM freshman_kgs WHERE id = %s """
    cursor.execute(sql_delete_query, ppl_id)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)