#! /usr/bin/env python

import ConfigParser
import time
import boto.swf.layer2 as swf

class Decider(swf.Decider):
    cf = ConfigParser.ConfigParser()
    cf.read('swf.conf')
    domain = cf.get('SWF', 'DOMAIN')
    task_list = 'default_tasks'
    version = cf.get('SWF', 'VERSION')
    activities = cf.get('SWF', 'ACTIVITIES').split(',')

    def run(self):
        history = self.poll()
        # Print history to familiarize yourself with its format.
        print history
        print ""
        if 'events' in history:
            # Get a list of non-decision events to see what event came in last.
            workflow_events = [e for e in history['events']
                               if not e['eventType'].startswith('Decision')]
            decisions = swf.Layer1Decisions()
            # Record latest non-decision event.
            last_event = workflow_events[-1]
            last_event_type = last_event['eventType']
            if last_event_type == 'WorkflowExecutionStarted':
                # At the start, get the worker to fetch the first assignment.
                activity = self.activities[0].strip()
                task_list = activity + 'TaskList'
                input_data = last_event['workflowExecutionStartedEventAttributes']['input']
                decisions.schedule_activity_task('%s-%s' % (activity, time.ctime()),
                                                 activity, self.version, task_list=task_list, input=input_data)
            elif last_event_type == 'ActivityTaskCompleted':
                # Take decision based on the name of activity that has just completed.
                # Get activity's event id.
                last_event_attrs = last_event['activityTaskCompletedEventAttributes']
                completed_activity_id = last_event_attrs['scheduledEventId'] - 1
                # Extract its name.
                activity_data = history['events'][completed_activity_id]
                activity_attrs = activity_data['activityTaskScheduledEventAttributes']
                activity_name = activity_attrs['activityType']['name']
                # Get the result from the activity.
                result = last_event['activityTaskCompletedEventAttributes'].get('result')

                # Take the decision.
                activities_number = len(self.activities)
                for i in range(0, activities_number):
                    activity = self.activities[i].strip()
                    if activity_name == activity:
                        if i < activities_number - 1:
                            next_activity = self.activities[i+1].strip()
                            next_task_list = next_activity + 'TaskList'
                            decisions.schedule_activity_task('%s-%s' % (next_activity, time.ctime()),
                                                             next_activity, self.version, task_list=next_task_list, input=result)
                        else:
                            # the last activity, we're done.
                            decisions.complete_workflow_execution()
                        break

            self.complete(decisions=decisions)
            return True

if __name__ == '__main__':
    decider = Decider()
    while True:
        try:
            decider.run()
        except Exception, e:
            print e
