#! /usr/bin/env python

import boto.swf.layer2 as swf

DOMAIN = 'HelloWorld'
ACTIVITY = 'HelloWorldActivity'
VERSION = '1.0'
TASK_LIST = 'HelloWorldTaskList'
WORKFLOW = 'HelloWorldWorkflow'

workflows = swf.Domain(name=DOMAIN).workflows()
execution = workflows[0].start(task_list='default_tasks')
