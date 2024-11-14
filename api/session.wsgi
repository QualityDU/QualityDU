import json
import os
import psycopg2
import logging
from dotenv import load_dotenv
import bcrypt

def session_create(username, password):
  load_dotenv(dotenv_path='/var/www/qualitydu/api/.env')
  try:
    sesskey = os.urandom(16).hex()
    with psycopg2.connect(os.getenv("DB_CONN")) as conn:
      with conn.cursor() as cur:
        query = """
          SELECT passwd_hash, passwd_salt, email_verified
          FROM users
          WHERE username = %s
        """
        cur.execute(query, (username,))
        row = cur.fetchone()
        if not row:
          raise Exception("User not found.")
        passwd_hash, passwd_salt, email_verified = row
        if not passwd_hash:
          raise Exception("Unexpected error: no password hash.")
        if not passwd_salt:
          raise Exception("Unexpected error: no password salt.")
        if not email_verified:
          raise Exception("User email not verified.")
        if passwd_hash.encode('utf-8') != bcrypt.hashpw(password.encode('utf-8'), passwd_salt.encode('utf-8')):
          raise Exception("Invalid password.")
        query = """
          UPDATE users
          SET sesskey_hash = %s, sesskey_salt = %s, last_login_date = NOW()
          WHERE username = %s
        """
        sesskey_salt = bcrypt.gensalt()
        sesskey_hash = bcrypt.hashpw(sesskey.encode('utf-8'), sesskey_salt)
        cur.execute(query, (sesskey_hash.decode('utf-8'), sesskey_salt.decode('utf-8'), username))
        return sesskey
  except psycopg2.Error as e:
    logging.error(f"Database error: {e}")
    raise Exception("Failed to create session due to a database error.") from e
  except Exception as e:
    logging.error(f"Unexpected error: {e}")
    raise Exception("An unexpected error occurred during session creation.") from e

def session_delete(username, session_key):
  load_dotenv(dotenv_path='/var/www/qualitydu/api/.env')
  try:
    with psycopg2.connect(os.getenv("DB_CONN")) as conn:
      with conn.cursor() as cur:
        query = """
          SELECT sesskey_hash, sesskey_salt
          FROM users
          WHERE username = %s
        """
        cur.execute(query, (username,))
        row = cur.fetchone()
        sesskey_hash, sesskey_salt = row
        if not row:
          raise Exception("User not found.")
        if not sesskey_hash:
          raise Exception("User not authenticated.")
        if not sesskey_salt:
          raise Exception("Unexpected error: no sesskey_salt.")
        if sesskey_hash.encode('utf-8') != bcrypt.hashpw(session_key.encode('utf-8'), sesskey_salt.encode('utf-8')):
          raise Exception("Bad session key.")
        query = """
          UPDATE users
          SET sesskey_hash = NULL, sesskey_salt = NULL
          WHERE username = %s
        """
        cur.execute(query, (username,))
  except psycopg2.Error as e:
    logging.error(f"Database error: {e}")
    raise Exception("Failed to delete session due to a database error.") from e
  except Exception as e:
    logging.error(f"Unexpected error: {e}")
    raise Exception("An unexpected error occurred during session deletion.") from e

'''
  Should do the following:
  - If the request method is PUT, it should create a new session for the user with the provided username and password.
  - If the request method is DELETE, it should delete the session for the user with the provided username and session key.
'''
def application(environ, start_response):
  status = '200 OK'
  headers = [('Content-Type', 'application/json')]
  if environ['REQUEST_METHOD'] == 'PUT':
    try:
      length = int(environ.get('CONTENT_LENGTH', 0))
      body = environ['wsgi.input'].read(length)
      data = json.loads(body)
      username = data['username']
      password = data['password']
      session_key = session_create(username, password)
      response = {
        "status": "success",
        "message": "Session created successfully.",
        "session_key": session_key
      }
    except Exception as e:
      response = {
        "status": "error",
        "message": str(e)
      }
  elif environ['REQUEST_METHOD'] == 'DELETE':
    try:
      length = int(environ.get('CONTENT_LENGTH', 0))
      body = environ['wsgi.input'].read(length)
      data = json.loads(body)
      username = data['username']
      session_key = data['session_key']
      session_delete(username, session_key)
      response = {
        "status": "success",
        "message": "Session deleted successfully."
      }
    except Exception as e:
      response = {
        "status": "error",
        "message": str(e)
      }
  else:
    response = {
      "status": "error",
      "message": "Invalid request method."
    }
  start_response(status, headers)
  return [json.dumps(response).encode('utf-8')]
