#! /usr/bin/env python

import boto.swf.layer2 as swf

DOMAIN = 'HelloWorld'
ACTIVITY = 'HelloWorldActivity'
VERSION = '1.0'
TASK_LIST = 'HelloWorldTaskList'
WORKFLOW = 'HelloWorldWorkflow'
swf.Domain(name=DOMAIN).register()
swf.ActivityType(domain=DOMAIN, name=ACTIVITY, version=VERSION, task_list=TASK_LIST).register()
swf.WorkflowType(domain=DOMAIN, name=WORKFLOW, version=VERSION, task_list='default_tasks').register()
