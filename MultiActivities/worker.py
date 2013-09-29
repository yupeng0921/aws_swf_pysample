#! /usr/bin/env python

import ConfigParser
import sys
import time
import logging
import boto.swf.layer2 as swf

class  Worker(swf.ActivityWorker):
    cf = ConfigParser.ConfigParser()
    cf.read('swf.conf')
    domain = cf.get('SWF', 'DOMAIN')
    version = cf.get('SWF', 'VERSION')
    task_list = None

    def __init__(self, task_list=None):
        swf.ActivityWorker.__init__(self)
        self.task_list = task_list
        LOG_FILENAME="swf.log"
        logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO)

    def run(self):
        activity_task = self.poll()
        print activity_task
        if 'activityId' in activity_task:
            try:
                input_data = activity_task.get('input')
                log = "%s %s %s" % (time.ctime(), activity_task['activityType']['name'], input_data)
                logging.info(log)
                self.complete(result=log)
            except Exception, error:
                self.fail(reason=str(error))
                raise error
            return True

if __name__ == '__main__':
    task_list = sys.argv[1] + 'TaskList'
    worker = Worker(task_list)
    while True:
        try:
            worker.run()
        except Exception, e:
            print e
