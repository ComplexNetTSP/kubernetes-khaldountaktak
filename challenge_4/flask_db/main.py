import os
from flask import Flask, render_template_string, request, jsonify
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

# MongoDB configuration using environment variables
mongo_url = os.getenv('MONGO_URL', 'mongodb://localhost:27017/')  # Default to localhost for local testing
mongo_client = MongoClient(mongo_url)
db = mongo_client[os.getenv('MONGO_DB_NAME', 'flask_app_db')]  # Default to 'flask_app_db'
requests_collection = db[os.getenv('MONGO_COLLECTION_NAME', 'requests')]  # Default to 'requests'

@app.route('/')
def hello_world():
    # Variables for rendering
    my_name = "Khaldoun TAKTAK"
    project_name = "Project TEST"
    version = "V5 ROLLING UPDATE"
    hostname = "flask-web"
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Get client IP address
    client_ip = request.remote_addr

    # Record request in MongoDB
    request_record = {
        "ip_address": client_ip,
        "date": current_date
    }
    requests_collection.insert_one(request_record)

    # Fetch the last 10 records from MongoDB
    last_10_requests = list(requests_collection.find().sort("_id", -1).limit(10))

    # HTML content
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{{ project_name }} - Home</title>
    </head>
    <body>
        <h1>Welcome to {{ project_name }}!</h1>
        <p><strong>Your Name:</strong> {{ your_name }}</p>
        <p><strong>Project Name:</strong> {{ project_name }}</p>
        <p><strong>Version:</strong> {{ version }}</p>
        <p><strong>Server Hostname:</strong> {{ hostname }}</p>
        <p><strong>Current Date:</strong> {{ current_date }}</p>
        <h2>Last 10 Requests</h2>
        <table border="1">
            <tr>
                <th>#</th>
                <th>IP Address</th>
                <th>Date</th>
            </tr>
            {% for idx, request in enumerate(last_requests) %}
            <tr>
                <td>{{ idx + 1 }}</td>
                <td>{{ request['ip_address'] }}</td>
                <td>{{ request['date'] }}</td>
            </tr>
            {% endfor %}
        </table>
    </body>
    </html>
    """

    return render_template_string(
        html_content,
        your_name=my_name,
        project_name=project_name,
        version=version,
        hostname=hostname,
        current_date=current_date,
        last_requests=last_10_requests,
        enumerate=enumerate  # Pass enumerate to the template context
    )

@app.route('/health', methods=['GET'])
def health():
    try:
        # Perform a lightweight MongoDB operation to ensure connectivity
        mongo_client.admin.command('ping')
        return jsonify({"status": "healthy"}), 200
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
