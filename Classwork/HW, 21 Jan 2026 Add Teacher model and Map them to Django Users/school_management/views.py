from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>School Management System</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 50px; text-align: center; }
                .container { max-width: 600px; margin: auto; }
                .card { background: #f4f4f4; padding: 20px; margin: 10px; border-radius: 5px; }
                a { text-decoration: none; color: #007bff; }
                a:hover { text-decoration: underline; }
                .credentials { text-align: left; background: #e9ecef; padding: 15px; border-radius: 5px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🏫 School Management System</h1>
                <div class="card">
                    <h2>Welcome to the System</h2>
                    <p>Please use one of the following links:</p>
                    <p>
                        <a href="/admin/">🔐 Admin Panel</a> | 
                        <a href="/teachers/dashboard/">👨‍🏫 Teacher Dashboard</a>
                    </p>
                </div>
                <div class="credentials">
                    <h3>Teacher Login Credentials:</h3>
                    <ul>
                        <li><strong>Principal:</strong> principal / principal123</li>
                        <li><strong>Class Teacher:</strong> classteacher / teacher123</li>
                        <li><strong>Subject Teacher:</strong> subjectteacher / teacher123</li>
                    </ul>
                </div>
            </div>
        </body>
        </html>
    ''')
