import json

def application(environ, start_response):
    status = '200 OK'
    headers = [('Content-Type', 'application/json')]
    response = {
        "status": "success", 
        "message": "Service is running"
    }
    start_response(status, headers)
    return [json.dumps(response).encode('utf-8')]