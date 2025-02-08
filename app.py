from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

from helpers import nl_to_sql

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:12345@localhost:3306/23bcp153_dbms_lab2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    if request.method == "GET":
        return render_template('index.html', error=error)
    else:
        nl_query = request.form.get("nl_query")
        if not nl_query:
            return render_template('index.html', error="Query cannot be empty")
        sql_query = nl_to_sql(nl_query)

        if sql_query == "Invalid Query":
            return render_template('index.html', error="Invalid Query")
        else:
            try:
                result = db.session.execute(text(sql_query))
                if sql_query.lower().startswith("select"):
                    columns = result.keys()
                    data = result.fetchall()
                    return render_template('index.html', columns=columns, data=data, sql_query=sql_query)
                else:
                    return render_template('index.html', sql_query=sql_query)
            except Exception as e:
                return render_template('index.html', error=str(e))

if __name__ == '__main__':
    app.run(debug=True)