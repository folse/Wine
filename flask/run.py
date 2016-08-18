#!/usr/bin/env python
import os
from wine import app
from flask.ext.script import Manager, Server, Shell
from flask.ext.migrate import MigrateCommand

manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command("run", Server(host="0.0.0.0", port=80, use_debugger=True))


if __name__ == '__main__':
	from werkzeug.contrib.fixers import ProxyFix
	app.wsgi_app = ProxyFix(app.wsgi_app)
	manager.run()
