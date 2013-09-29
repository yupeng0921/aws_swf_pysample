#! /usr/bin/env python

import boto.swf.layer2 as swf

DOMAIN = 'HelloWorld'
ACTIVITY = 'HelloWorldActivity'
VERSION = '1.0'
TASK_LIST = 'HelloWorldTaskList'
WORKFLOW = 'HelloWorldWorkflow'

swf.Domain(name=DOMAIN).deprecate()
