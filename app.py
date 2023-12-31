from flask import Flask, render_template, request, send_file, jsonify
import mysql.connector
from io import BytesIO

app = Flask(__name__, static_folder='static')

# Database configuration
db_config = {
    'host': 'group5project.czptxhzjxjrt.us-east-1.rds.amazonaws.com',
    'user': 'admin',
    'password': 'JayPatel',
    'database': 'project',
}

# Connect to the RDS database
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

app.static_folder = 'assets'

# Routes
@app.route("/")
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/addservice')
def addservice():
    return render_template('addservice.html')

@app.route('/Iaas')
def Iaas():
    return render_template('Iaas.html')

@app.route('/Paas')
def Paas():
    return render_template('Paas.html')

@app.route('/Saas')
def Saas():
    return render_template('Saas.html')

@app.route('/Saas1')
def Saas1():
    return render_template('Saas1.html')

@app.route('/Saas2')
def Saas2():
    return render_template('Saas2.html')


    
# GET method
@app.route('/get_service_details/<main_service>', methods=['GET'])
def get_service(main_service):
	cursor.execute('SELECT service_name,description,main_service FROM service_details WHERE main_service = %s', (main_service,))
	services = cursor.fetchall()
	
	return render_template('get_pass_services.html', services=services)

# Updated route definition in your Flask app
@app.route('/image/<service_name>/<main_service>')
def get_image(service_name, main_service):
    # Your existing code here
    cursor.execute('SELECT image_data FROM service_details WHERE service_name = %s AND main_service = %s', (service_name, main_service))
    image_data = cursor.fetchone()[0]

    # Create an in-memory file-like object and return the image
    return send_file(BytesIO(image_data), mimetype='image/jpeg')

# POST methods
@app.route('/insert_data', methods=['POST'])
def insert_data():
    try:
        data = request.get_json()
        query = "INSERT INTO user_info (email, name, subject, message) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (data.get('email'), data.get('name'),data.get('subject'),data.get('message')))
        conn.commit()
        
        response = "Data submitted successfully!"
        return jsonify(response)
    
    except Exception as e:
        # Handle any exceptions and return an error message
        error_message = f"Error submitting the form: {str(e)}"
        return jsonify(error_message), 500

@app.route('/upload', methods=['POST'])
def upload():
    
    # Create a table to store images if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS service_details (
            id INT AUTO_INCREMENT PRIMARY KEY,
            image_data MEDIUMBLOB,
            description MEDIUMTEXT,
            service_name VARCHAR(255),
            main_service VARCHAR(255)
        )
    ''')
    conn.commit()
   
    description = request.form.get('description')
    service_name = request.form.get('service_name')
    main_service = request.form.get('main_service')

    # Get the uploaded image from the form
    image = request.files['image']
    image_data = image.read()

    # Insert data into the database
    cursor.execute('''
        INSERT INTO service_details (image_data, description, service_name, main_service)
        VALUES (%s, %s, %s, %s)
    ''', (image_data, description, service_name, main_service))
    conn.commit()

    return 'Image uploaded successfully!'
    
if __name__ == '__main__':
    app.run(debug=True)