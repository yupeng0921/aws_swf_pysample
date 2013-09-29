# AWS Sample Workflow for python Samples

## Prerequisites

install boto and configure the credentials as this link:
http://boto.readthedocs.org/en/latest/getting_started.html


## The HelloWorld sample

Create domain and workflow:
    python setup.py
Run decider:
    python decider.py
Run worker:
    python worker.py
Launch a execution:
    python start.py
Every time run the start.py, decider will let trigger the worker to run, and the worker print 'hello world' to the console.

After test done, run:
    python clean.py
to deprecate the domain.

## The MultiActivities sample

Create domain and workflow:
    python setup.py
Run decider:
    python decider.py
Run three workers on three different terminals:
    python worker.py activity1
	python worker.py activity2
	python worker.py activity3
Launch a execution
    python start.py
Every time run the start.py, the decider will trigger the three workers one by one, first trigger activity1, after activity1 complete, trigger activity2, after activity2 complete, trigger activity3, after activity3 complete, the decider will complete the execution.

After test done, run:
    python clean.py
to deprecate the domain.
