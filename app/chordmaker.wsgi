# vim: se ft=python:
import logging
import sys
# presuming you put this into /opt/webapps/PROJECTNAME
sys.path.insert(0, '/opt/webapps')
logging.basicConfig(stream=sys.stderr)

# from PROJECTNAME.main import...
from chordmaker.main import app as application
