from flask import Flask, render_template_string
import socket
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def hello_world():

    my_name = "Khaldoun TAKTAK"  
    project_name = "Project Name"  
    version = "V1"
    hostname = "flask-web" 
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  


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
    </body>
    </html>
    """

    return render_template_string(html_content, 
                                  your_name=my_name, 
                                  project_name=project_name, 
                                  version=version, 
                                  hostname=hostname, 
                                  current_date=current_date)

if __name__ == '__main__':
    app.run(debug=True)
