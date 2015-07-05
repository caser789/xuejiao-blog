import os
COV = None
if os.environ.get('BLOG_COVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()

from app import create_app, db
from app.models import User, Role, Permission, Post, Follow, Comment
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand

app = create_app(os.getenv('XUEJIAO-BLOG-CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Permission=Permission,
            Post=Post, Follow=Follow, Comment=Comment)
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

@manager.command
# to add a Boolean option to test cmd, just add a Boolean argument to test
# function
def test(coverage=False):
    """Run the unit tests."""
    if coverage and not os.environ.get('BLOG_COVERAGE'):
        import sys
        # set environment argument
        os.environ['BLOG_COVERAGE'] = '1'
        # restart script
        os.execvp(sys.executable, [sys.executable] + sys.argv)
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        # write report to console
        print('Coverage Summary:')
        COV.report()
        # write report to disk
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        # erase cov
        COV.erase()

if __name__ == '__main__':
    manager.run()
