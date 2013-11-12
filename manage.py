#!/usr/bin/env python
import os
import sys
import time,sched
from kthread import *
def run_auth():
	def on9_check():
		import subprocess
		subprocess.call("check_users.py", shell=True)
		time.sleep(15)
		on9_check()
	on9_check()

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
	
	