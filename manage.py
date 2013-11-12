#!/usr/bin/env python
import os
import sys
import time
from kthread import *
def run_auth():
	import subprocess
	subprocess.call("check_users.py", shell=True)


if __name__ == "__main__":
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chatdatabase.settings")
	try:
		A = KThread(target=run_auth)
		A.start()
	except:
		print "Error: unable to start thread"

	from django.core.management import execute_from_command_line
	
	execute_from_command_line(sys.argv)
	A.kill()
	
	