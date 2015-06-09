#!/usr/bin/bin/env python
import os
from oga_api import create_app
from flask.ext.script import Manager, Shell, Command
from commands import TestCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)

def make_shell_context():
	return dict(app=app)

@manager.command
def test():
	import unittest
	tests = unittest.TestLoader().discover('.')
	unittest.TextTestRunner(verbosity=2).run(tests)

def main():
	manager.add_command("shell", Shell(make_context=make_shell_context))
	manager.run()

if __name__ == '__main__':
	main()
