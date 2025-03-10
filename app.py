from flask import Flask, jsonify, request
import psycopg2

OK_CODE = 200
BAD_REQUEST_CODE = 400

app = Flask(__name__)


def db_conn():
    conn = psycopg2.connect("dbname=db2022118542 user=a2022118542 password=a2022118542")
    return conn


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/emp', methods=['GET'])
def get_employee():
    conn = db_conn()
    cur = conn.cursor()
    cur.execute("select * from emp")
    result = cur.fetchall()
    jsonify(result), OK_CODE
    conn.close()
    return result


@app.route('/get_emp', methods=['GET'])
def get_employee_by_id():
    conn = db_conn()
    cur = conn.cursor()
    id = request.args.get('id')
    cur.execute("select * from emp where empno = %s", (id,))
    emp_detail = cur.fetchone()
    conn.close()
    return jsonify(emp_detail), OK_CODE

@app.route('/insert_emp', methods=['POST'])
def post_employee():
    conn = db_conn()
    cur = conn.cursor()
    data = request.get_json()
    if "empno" not in data or "ename" not in data or "job" not in data:
        return jsonify({"message": "Missing data"}), BAD_REQUEST_CODE
    try:
        cur.execute("""call insert_emp(%s,%s,%s,%s,%s,%s,%s);""",
                    data["ename"], data["job"],
                    data["mgr"], data["hiredate"], data["sal"],
                    data["comm"], data["deptno"]
        )
        conn.commit()
    except Exception as e:
        d = {"message": str(e)}
        return jsonify(d), BAD_REQUEST_CODE
    finally:
        cur.close()
        conn.close()
    return jsonify(data), OK_CODE


if __name__ == '__main__':
    app.run()