#!/usr/bin/env python
import os
import sys
import time,sched
from kthread import *
import urllib,time

if __name__ == "__main__":
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chatdatabase.settings")
	

	from django.core.management import execute_from_command_line
	
	execute_from_command_line(sys.argv)
	
	
	
