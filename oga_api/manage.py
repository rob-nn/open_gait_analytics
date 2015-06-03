#!/usr/bin/bin/env python
import os
from oga_api import create_app

from flask.ext.script import Manager, Shell

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

def make_shell_context():
	return dict(app=app)

def main():
	manager = Manager(app)
	manager.add_command("shell", Shell(make_context=make_shell_context))
	manager.run()

if __name__ == '__main__':
	main()
