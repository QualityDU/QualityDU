import json
import logging
import os
import psycopg2
from dotenv import load_dotenv

def email_check(username, token):
  load_dotenv(dotenv_path='/var/www/qualitydu/api/.env')
  try:
    with psycopg2.connect(os.getenv("DB_CONN")) as conn:
      with conn.cursor() as cur:
          query = """
              SELECT email_verification_token
              FROM users
              WHERE username = %s
          """
          cur.execute(query, (username,))
          email_verification_token = cur.fetchone()
          if email_verification_token:
            if email_verification_token[0] == token:
              query = """
                UPDATE users
                SET email_verified = TRUE
                WHERE username = %s
                """
              cur.execute(query, (username,))
              conn.commit()
              #return True
            else:
              #return False
              raise Exception("Invalid email verification token.")
          else:
            #return False
            raise Exception("User not found.")
  except psycopg2.Error as e:
    logging.error(f"Database error: {e}")
    raise Exception("Failed to verify email due to a database error.") from e
  except Exception as e:
    logging.error(f"Unexpected error: {e}")
    raise Exception("An unexpected error occurred during email verification.") from e

'''
  Should do the following:
  - If the request method is GET, use token and username from the query string to verify the email and update the database.
'''
def application(environ, start_response):
  status = '200 OK'
  headers = [('Content-Type', 'application/json')]
  if environ['REQUEST_METHOD'] == 'GET':
    try:
      query = environ['QUERY_STRING']
      token = query.split('=')[1].split('&')[0]
      username = query.split('=')[2]
      email_check(username, token)
      response = {
        "status": "success", 
        "message": "Email verified."
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
      