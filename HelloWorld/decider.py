#! /usr/bin/env python

import time
import boto.swf.layer2 as swf

DOMAIN = 'HelloWorld'
ACTIVITY = 'HelloWorldActivity'
VERSION = '1.0'
TASK_LIST = 'HelloWorldTaskList'
WORKFLOW = 'HelloWorldWorkflow'

class Decider(swf.Decider):
    domain = DOMAIN
    task_list = 'default_tasks'
    version = VERSION

    def run(self):
        history = self.poll()
        # Print history to familiarize yourself with its format.
        print history
        if 'events' in history:
            # Get a list of non-decision events to see what event came in last.
            workflow_events = [e for e  in history['events']
                               if not e['eventType'].startswith('Decision')]
            decisions = swf.Layer1Decisions()
            # Record latest non-decision event.
            last_event = workflow_events[-1]
            last_event_type = last_event['eventType']
            if last_event_type == 'WorkflowExecutionStarted':
                # At the start, get the worker to fetch the first assignment.
                decisions.schedule_activity_task('%s-%i' % (ACTIVITY, time.time()),
                                                 ACTIVITY, VERSION, task_list=TASK_LIST)
            elif last_event_type == 'ActivityTaskCompleted':
                # Take decision based on the name of activity that has just completed.
                # 1) Get activity's event id.
                last_event_attrs = last_event['activityTaskCompletedEventAttributes']
                completed_activity_id = last_event_attrs['scheduledEventId'] - 1
                # 2) Extract its name.
                activity_data = history['events'][completed_activity_id]
                activity_attrs = activity_data['activityTaskScheduledEventAttributes']
                activity_name = activity_attrs['activityType']['name']
                # 3) Optionally, get the result from the activity.
                result = last_event['activityTaskCompletedEventAttributes'].get('result')

                # Take the decision.
                if activity_name == ACTIVITY:
                    # only one activity, we're done
                    decisions.complete_workflow_execution()

            self.complete(decisions=decisions)
            return True

if __name__ == '__main__':
    decider = Decider()
    while True:
        try:
            decider.run()
        except Exception, e:
            print e
