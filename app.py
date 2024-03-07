from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

# Environment variable for database password
DB_PASSWORD = os.environ.get("DB_PASSWORD")

# Database connection parameters
server_params = {
    "dbname": "nl1023",
    "host": "db.doc.ic.ac.uk",
    "port": "5432",
    "user": "nl1023",
    "password": DB_PASSWORD,
    "client_encoding": "utf-8",
}


# Establish database connection
def get_db_connection():
    return psycopg2.connect(**server_params)


@app.route("/retrieve_notes", methods=["GET"])
def retrieve_notes():
    user_id = request.args.get("user_id")
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM notes WHERE user_id = %s", (user_id,))
            notes = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            result = [dict(zip(columns, note)) for note in notes]
            return jsonify(result)


@app.route("/create_note", methods=["POST"])
def create_note():
    data = request.get_json()
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO notes (user_id, color, content, time) VALUES (%s, %s, %s, %s)",
                (data["user_id"], data["color"], data["content"], data["time"]),
            )
            conn.commit()
    return jsonify({"message": "Note created successfully"}), 201


@app.route("/update_note", methods=["POST"])
def update_note():
    data = request.get_json()
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE notes SET color = %s, content = %s, time = %s WHERE note_id = %s",
                (data["color"], data["content"], data["time"], data["note_id"]),
            )
            conn.commit()
    return jsonify({"message": "Note updated successfully"}), 200


@app.route("/delete_note", methods=["POST"])
def delete_note():
    data = request.get_json()
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM notes WHERE note_id = %s", (data["note_id"],))
            conn.commit()
    return jsonify({"message": "Note deleted successfully"}), 200


if __name__ == "__main__":
    app.run(debug=True)
