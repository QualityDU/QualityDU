import json
from datetime import datetime
import psycopg2
import os
from dotenv import load_dotenv
import logging
from helpers.mail import send_email
import threading
import bcrypt

'''
The users table is defined as:
CREATE TABLE public.users (
	user_id serial4 NOT NULL,
	passwd_hash varchar NOT NULL,
	"role" varchar DEFAULT '0'::character varying NOT NULL,
	ip_addr varchar NULL,
	registration_date date NOT NULL,
	last_login_date date NULL,
	username varchar NOT NULL,
	num_contributions int4 DEFAULT 0 NOT NULL,
	num_requests int4 DEFAULT 0 NOT NULL,
	karma int4 DEFAULT 0 NOT NULL,
	email varchar NOT NULL,
	email_verified bool DEFAULT false NOT NULL,
	email_verification_token varchar NOT NULL,
	sesskey_hash varchar NULL,
	last_usr_chng_date date NULL,
	sesskey_salt varchar NULL,
	passwd_salt varchar NULL,
	CONSTRAINT users_pk PRIMARY KEY (user_id),
	CONSTRAINT users_unique UNIQUE (username),
	CONSTRAINT users_unique_1 UNIQUE (email_verification_token)
);
'''

def user_create(username, password, email, ip_addr):
	passwd_salt = bcrypt.gensalt()
	passwd_hash = bcrypt.hashpw(password, passwd_salt)
	registration_date = datetime.now()

	load_dotenv(dotenv_path='/var/www/qualitydu/api/.env')
	# conn = psycopg2.connect(os.getenv("DB_CONN"))
	# cur = conn.cursor()

	# query = "INSERT INTO users (passwd_hash, username, email, registration_date, ip_addr) VALUES (%s, %s, %s, %s, %s)"
	# cur.execute(query, (passwd_hash, username, email, registration_date, ip_addr))
	# conn.commit()
	# cur.close()
	# conn.close()	
	try:
		email_verification_token = os.urandom(16).hex()
		base_url = os.getenv("BASE_URL");
		with psycopg2.connect(os.getenv("DB_CONN")) as conn:
			with conn.cursor() as cur:
				query = """
          INSERT INTO users (passwd_hash, passwd_salt, username, email, registration_date, ip_addr, email_verification_token)
          VALUES (%s, %s, %s, %s, %s, %s, %s)
          """
				cur.execute(query, (passwd_hash, passwd_salt, username, email, registration_date, ip_addr, email_verification_token))
				# Send an email in parallel to verify the email address
				subject = "QualityDU Email Verification"
				body = f"Click <a href='{base_url}/api/email-verify?token={email_verification_token}&username={username}'>here</a> to verify your email address. <br/><hr/><br/> By proceeding, you agree to the below terms and conditions:<br><br>1. You will not use this service to post any material which is knowingly false and/or defamatory, inaccurate, abusive, vulgar, hateful, harassing, obscene, profane, sexually oriented, threatening, invasive of a person's privacy, or otherwise violative of any law.<br>2. You will not use this service to promote any illegal activities.<br>3. You will not use this service to post any copyrighted material unless the copyright is owned by you."
			  #send_email(subject, body, os.getenv("MAIL_SENDER"), [email], os.getenv("MAIL_PASSWD"))
				threading.Thread(target=send_email, args=(subject, body, os.getenv("MAIL_SENDER"), [email], os.getenv("MAIL_PASSWD"))).start()

	except psycopg2.Error as e:
		logging.error(f"Database error: {e}")
		raise Exception("Failed to create user due to a database error.") from e
	except Exception as e:
		logging.error(f"Unexpected error: {e}")
		raise Exception("An unexpected error occurred during user creation.") from e

def user_get(user_id):
	load_dotenv(dotenv_path='/var/www/qualitydu/api/.env')
	try:
		with psycopg2.connect(os.getenv("DB_CONN")) as conn:
			with conn.cursor() as cur:
				query = """
					SELECT user_id, username, registration_date, last_login_date, num_contributions, karma, email_verified
					FROM users
					WHERE user_id=%s;
					"""
				cur.execute(query, (user_id,))
				user = cur.fetchone()
				if user:
					return user
				else:
					raise Exception("User not found.")
	except psycopg2.Error as e:
		logging.error(f"Database error: {e}")
		raise Exception("Failed to get user due to a database error.") from e
	except Exception as e:
		logging.error(f"Unexpected error: {e}")
		raise Exception("An unexpected error occurred during user retrieval.") from e

def user_sesskey_check_cur(user_id, auth_sesskey, cur):
	query = """
		SELECT sesskey_hash, sesskey_salt
		FROM users
		WHERE user_id = %s
	"""
	cur.execute(query, (user_id,))
	row = cur.fetchone()
	sesskey_hash, sesskey_salt = row
	if not row:
		raise Exception("User not found.")
	if not sesskey_hash:
		raise Exception("User not authenticated.")
	if not sesskey_salt:
		raise Exception("Falsy sesskey_salt (should not happen)")
	if sesskey_hash != bcrypt.hashpw(auth_sesskey, sesskey_salt):
		raise Exception("Bad sesskey.")

def user_update(user_id, password, email, auth_sesskey):
	passwd_salt = bcrypt.gensalt()
	passwd_hash = bcrypt.hashpw(password, passwd_salt)
	chng_date = datetime.now()

	load_dotenv(dotenv_path='/var/www/qualitydu/api/.env')
	try:
		with psycopg2.connect(os.getenv("DB_CONN")) as conn:
			with conn.cursor() as cur:
				user_sesskey_check_cur(user_id, auth_sesskey, cur)
				query = """
					UPDATE users
					SET passwd_hash = %s, passwd_salt = %s, email = %s, last_usr_chng_date = %s
					WHERE user_id = %s
					"""
				cur.execute(query, (passwd_hash, passwd_salt, email, chng_date, user_id))
	except psycopg2.Error as e:
		logging.error(f"Database error: {e}")
		raise Exception("Failed to update user due to a database error.") from e
	except Exception as e:
		logging.error(f"Unexpected error: {e}")
		raise Exception("An unexpected error occurred during user update.") from e

def user_delete(user_id, auth_sesskey):
	load_dotenv(dotenv_path='/var/www/qualitydu/api/.env')
	try:
		with psycopg2.connect(os.getenv("DB_CONN")) as conn:
			with conn.cursor() as cur:
				user_sesskey_check_cur(user_id, auth_sesskey, cur)
				query = """
					DELETE FROM users
					WHERE user_id = %s
					"""
				cur.execute(query, (user_id,))
	except psycopg2.Error as e:
		logging.error(f"Database error: {e}")
		raise Exception("Failed to delete user due to a database error.") from e
	except Exception as e:
		logging.error(f"Unexpected error: {e}")
		raise Exception("An unexpected error occurred during user deletion.") from e

'''
	Should do the following:
	- If the request method is POST, it should create a new user with the provided username, password, and email.
	- If the request method is GET, it should return the user_id, username, registration_date, last_login_date, num_contributions, karma, and email_verified for the user with the provided user_id.
	- If the request method is PUT, it should update the user with the provided user_id with the provided password, and email. The operation should require an additional parameter: sesskey, which shall be used to authenticate the user.
	- If the request method is DELETE, it should delete the user with the provided user_id. The operation should require an additional parameter: sesskey, which shall be used to authenticate the user.
'''
def application(environ, start_response):
	status = '200 OK'
	headers = [('Content-Type', 'application/json')]
	if environ['REQUEST_METHOD'] == 'POST':
		try:
			length = int(environ.get('CONTENT_LENGTH', '0'))
			body = environ['wsgi.input'].read(length).decode('utf-8')
			data = json.loads(body)
			user_create(data['username'], data['password'], data['email'], environ['REMOTE_ADDR'])
			status = '201 Created'
			response = {
				"status": "success",
				"message": "User created successfully"
			}
		except Exception as e:
			status = '500 Internal Server Error'
			response = {
				"status": "error",
				"message": str(e)
			}
	elif environ['REQUEST_METHOD'] == 'GET':
		try:
			user_id = environ['QUERY_STRING'].split('=')[-1]
			user = user_get(user_id)
			status = '200 OK'			
			response = {
				"status": "success",
				"user": {
					"user_id": user[0],
					"username": user[1],
					"registration_date": user[2].isoformat(),
					"last_login_date": user[3].isoformat() if user[3] else None,
					"num_contributions": user[4],
					"karma": user[5],
					"email_verified": user[6]
				}
			}
		except Exception as e:
			status = '404 Not Found'			
			response = {
				"status": "error", 
				"message": str(e)
			}
	elif environ['REQUEST_METHOD'] == 'PUT':
		try:
			length = int(environ.get('CONTENT_LENGTH', '0'))
			body = environ['wsgi.input'].read(length).decode('utf-8')
			data = json.loads(body)
			user_update(data['user_id'], data['password'], data['email'], data['sesskey'])
			status = '200 OK'
			response = {
				"status": "success",
				"message": "User updated successfully"
			}
		except Exception as e:
			status = '500 Internal Server Error'			
			response = {
				"status": "error", 
				"message": str(e)
			}
	elif environ['REQUEST_METHOD'] == 'DELETE':
		try:
			length = int(environ.get('CONTENT_LENGTH', '0'))
			body = environ['wsgi.input'].read(length).decode('utf-8')
			data = json.loads(body)
			user_delete(data['user_id'], data['sesskey'])
			status = '200 OK'
			response = {
				"status": "success",
				"message": "User deleted successfully"
			}
		except Exception as e:
			status = '500 Internal Server Error'			
			response = {
				"status": "error", 
				"message": str(e)
			}
	else:
		status = '405 Method Not Allowed'		
		response = {
			"status": "error", 
			"message": "Method not allowed"
		}
	start_response(status, headers)
	return [json.dumps(response).encode('utf-8')]
