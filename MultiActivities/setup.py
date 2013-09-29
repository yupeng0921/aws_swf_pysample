#! /usr/bin/env python

import ConfigParser
import boto.swf.layer2 as swf

cf = ConfigParser.ConfigParser()
cf.read('swf.conf')
domain = cf.get('SWF', 'DOMAIN')
activities = cf.get('SWF', 'ACTIVITIES').split(',')
version = cf.get('SWF', 'VERSION')
workflow = cf.get('SWF', 'WORKFLOW')

swf.Domain(name=domain).register()
for activity in activities:
    activity = activity.strip()
    task_list = activity+'TaskList'
    swf.ActivityType(domain=domain, name=activity, version=version,task_list=task_list).register()

swf.WorkflowType(domain=domain, name=workflow, version=version, task_list='default_tasks').register()
