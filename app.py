from flask import Flask, request, jsonify
import psycopg2 as db
import json
import datetime
import os

app = Flask(__name__)

server_params = {
    'dbname': 'nl1023',
    'host': 'db.doc.ic.ac.uk',
    'port': '5432',
    'user': 'nl1023',
    'password': '08SJ88h7/31',
    'client_encoding': 'utf-8'
}


@app.route('/')
def hello_world():
    return "hello"

@app.route('/retrieve_data', methods=['GET'])
def retrieve_data():
    user_id = request.args.get('user_id')
    conn = db.connect(**server_params)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT *
        FROM notes
        WHERE user_id=%s
    """, [user_id])
    recs = cursor.fetchall()
    if not recs:
        conn.close()
        return jsonify({})
    else:
        results = []
        for rec in recs:
            rec_list = list(rec)
            rec_list[4] = rec_list[4].strftime('%Y-%m-%d %H:%M:%S')
            columns = [desc[0] for desc in cursor.description]
            result = dict(zip(columns, rec_list))
            results.append(result)
        return json.dumps(results)

@app.route('/create_data', methods=['GET'])
def create_data():
    user_id = request.args.get('user_id')
    time = request.args.get('time')
    color = request.args.get('color')
    content = request.args.get('content')
    conn = db.connect(**server_params)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO notes (user_id, color, content, time)
        VALUES (%s, %s, %s, %s)
    """, [user_id, color, content, time])
    conn.commit()
    conn.close()
    
    return "Data created successfully."

@app.route('/update_data', methods=['GET'])
def update_data():
    note_id = request.args.get('note_id')
    user_id = request.args.get('user_id')
    time = request.args.get('time')
    color = request.args.get('color')
    content = request.args.get('content')
    
    conn = db.connect(**server_params)
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM notes WHERE note_id=%s
    """, [note_id])
    
    cursor.execute("""
        INSERT INTO notes (user_id, color, content, time)
        VALUES (%s, %s, %s, %s)
    """, [user_id, color, content, time])
    conn.commit()
    conn.close()

    return "Data updated successfully."

@app.route('/delete_data', methods=['GET'])
def delete_data():
    id = request.args.get('note_id')
    conn = db.connect(**server_params)
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM notes WHERE note_id=%s
    """, [id])
    conn.commit()
    conn.close()

    return "Data deleted successfully."

if __name__ == '__main__':
    app.run(debug=True)
