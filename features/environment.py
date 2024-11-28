import os
from multiprocessing import Process
import threading
import string
import random
from flask_socketio import SocketIO, socketio
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from wsgiref import simple_server
from wsgiref.simple_server import WSGIRequestHandler
import app
import time

def start_server():
	flask_app = app.create_app()
	SocketIO(flask_app).run(flask_app, allow_unsafe_werkzeug=True)

def before_all(context):
	if "FLASK_CHILD" in os.environ: # Spawning a process causes behave to run them both as test runners, leading to port conflicts and dangling processes
		start_server()              # So this is a workaround - parent sets a flag, child never exits the before_all hook
	
	os.environ["FLASK_CHILD"] = "1"
	context.server_process = Process(target=start_server)
	context.server_process.start()

	context.browser = webdriver.Firefox()
	context.browser.set_page_load_timeout(time_to_wait=2000)

	context.randomly_generated_user = randomword(16)
	time.sleep(1)


def after_all(context):
	context.browser.quit()
	context.server_process.terminate()
	context.server_process.join()


def randomword(length):
	letters = string.ascii_lowercase
	return ''.join(random.choice(letters) for i in range(length))