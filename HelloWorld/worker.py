#! /usr/bin/env python

import boto.swf.layer2 as swf

DOMAIN = 'HelloWorld'
ACTIVITY = 'HelloWorldActivity'
VERSION = '1.0'
TASK_LIST = 'HelloWorldTaskList'
WORKFLOW = 'HelloWorldWorkflow'

class Worker(swf.ActivityWorker):

    domain = DOMAIN
    version = VERSION
    task_list = TASK_LIST

    def run(self):
        activity_task = self.poll()
        print activity_task
        if 'activityId' in activity_task:
            print 'hello world'
            self.complete()

if __name__ == '__main__':
    worker = Worker()
    while True:
        try:
            worker.run()
        except Exception, e:
            print e
