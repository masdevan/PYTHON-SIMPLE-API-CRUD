from flask import Flask, request, jsonify
import mysql.connector
from config import mysql_config
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def connect_to_mysql():
    try:
        connection = mysql.connector.connect(
            host=mysql_config['host'],
            user=mysql_config['user'],
            password=mysql_config['password'],
            database=mysql_config['database']
        )
        if connection.is_connected():
            return connection
    except mysql.connector.Error as e:
        print(f"Failed to connect to MySQL Database: {e}")
        return None

@app.route('/hobi', methods=['GET'])
def get_hobi():
    connection = connect_to_mysql()
    cursor = connection.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM hobi")
    result = cursor.fetchall()
    return jsonify(result)

@app.route('/hobi', methods=['POST'])
def create_hobi():
    connection = connect_to_mysql()
    cursor = connection.cursor(dictionary=True)
    
    # Mengambil data dari form HTML
    nama = request.form['nama']
    
    cursor.execute("INSERT INTO hobi (nama) VALUES (%s)", (nama,))
    connection.commit()
    return jsonify({'message': 'Hobi created successfully'})

@app.route('/hobi/<int:id>', methods=['GET'])
def get_hobi_detail(id):
    connection = connect_to_mysql()
    cursor = connection.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM hobi WHERE id = %s", (id,))
    result = cursor.fetchone()
    return jsonify(result)

@app.route('/hobi/<int:id>', methods=['PUT'])
def update_hobi(id):
    connection = connect_to_mysql()
    cursor = connection.cursor(dictionary=True)
    
    data = request.json
    nama = data['nama']
    cursor.execute("UPDATE hobi SET nama = %s WHERE id = %s", (nama, id))
    connection.commit()
    return jsonify({'message': 'Hobi updated successfully'})

@app.route('/hobi/<int:id>', methods=['DELETE'])
def delete_hobi(id):
    connection = connect_to_mysql()
    cursor = connection.cursor(dictionary=True)
    
    cursor.execute("DELETE FROM hobi WHERE id = %s", (id,))
    connection.commit()
    return jsonify({'message': 'Hobi deleted successfully'})

@app.route('/anggota', methods=['GET'])
def get_anggota():
    connection = connect_to_mysql()
    cursor = connection.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM anggota")
    result = cursor.fetchall()
    return jsonify(result)

@app.route('/anggota', methods=['POST'])
def create_anggota():
    connection = connect_to_mysql()
    cursor = connection.cursor(dictionary=True)
    
    # Mengambil data dari form HTML
    nama = request.form['nama']
    usia = request.form['usia']
    email = request.form['email']
    deskripsi = request.form['deskripsi']
    tanggal_lahir = request.form['tanggal_lahir']
    gender = request.form['gender']
    status = request.form['status']
    
    cursor.execute("INSERT INTO anggota (nama, usia, email, deskripsi, tanggal_lahir, gender, status) VALUES (%s, %s, %s, %s, %s, %s, %s)", (nama, usia, email, deskripsi, tanggal_lahir, gender, status))
    connection.commit()
    return jsonify({'message': 'Anggota created successfully'})

@app.route('/anggota/<int:id>', methods=['GET'])
def get_anggota_detail(id):
    connection = connect_to_mysql()
    cursor = connection.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM anggota WHERE id = %s", (id,))
    result = cursor.fetchone()
    return jsonify(result)

@app.route('/anggota/<int:id>', methods=['PUT'])
def update_anggota(id):
    connection = connect_to_mysql()
    cursor = connection.cursor(dictionary=True)
    
    # Mengambil data dari form HTML
    nama = request.form['nama']
    usia = request.form['usia']
    email = request.form['email']
    deskripsi = request.form['deskripsi']
    tanggal_lahir = request.form['tanggal_lahir']
    gender = request.form['gender']
    status = request.form['status']
    
    cursor.execute("UPDATE anggota SET nama = %s, usia = %s, email = %s, deskripsi = %s, tanggal_lahir = %s, gender = %s, status = %s WHERE id = %s", (nama, usia, email, deskripsi, tanggal_lahir, gender, status, id))
    connection.commit()
    return jsonify({'message': 'Anggota updated successfully'})

@app.route('/anggota/<int:id>', methods=['DELETE'])
def delete_anggota(id):
    connection = connect_to_mysql()
    cursor = connection.cursor(dictionary=True)
    
    cursor.execute("DELETE FROM anggota WHERE id = %s", (id,))
    connection.commit()
    return jsonify({'message': 'Anggota deleted successfully'})

@app.route('/hobi_anggota', methods=['GET'])
def get_hobi_anggota():
    connection = connect_to_mysql()
    cursor = connection.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM hobi_anggota")
    result = cursor.fetchall()
    return jsonify(result)

@app.route('/hobi_anggota', methods=['POST'])
def create_hobi_anggota():
    connection = connect_to_mysql()
    cursor = connection.cursor(dictionary=True)
    
    # Mengambil data dari form HTML
    anggota_id = request.form['anggota_id']
    hobi_id = request.form['hobi_id']
    
    cursor.execute("INSERT INTO hobi_anggota (anggota_id, hobi_id) VALUES (%s, %s)", (anggota_id, hobi_id))
    connection.commit()
    return jsonify({'message': 'Hobi-anggota relationship created successfully'})

@app.route('/hobi_anggota/<int:anggota_id>/<int:hobi_id>', methods=['DELETE'])
def delete_hobi_anggota(anggota_id, hobi_id):
    connection = connect_to_mysql()
    cursor = connection.cursor(dictionary=True)
    
    cursor.execute("DELETE FROM hobi_anggota WHERE anggota_id = %s AND hobi_id = %s", (anggota_id, hobi_id))
    connection.commit()
    return jsonify({'message': 'Hobi-anggota relationship deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)