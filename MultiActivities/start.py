#! /usr/bin/env python

import ConfigParser
import time
import boto.swf.layer2 as swf

cf = ConfigParser.ConfigParser()
cf.read('swf.conf')
domain = cf.get('SWF', 'DOMAIN')
workflow = cf.get('SWF', 'WORKFLOW')

workflows = swf.Domain(name=domain).workflows(name=workflow)
input_data = '%s init_data' % time.ctime()
execution = workflows[0].start(task_list='default_tasks', input=input_data)
