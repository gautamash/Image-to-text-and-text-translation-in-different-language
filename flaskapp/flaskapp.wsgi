import sys
from flask import Flask, render_template, request,send_from_directory

sys.path.insert(0, '/var/www/html/flaskapp')

from app_basic import app as application