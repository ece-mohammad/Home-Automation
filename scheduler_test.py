#!/usr/bin/env python3


import sched
import time
import threading as thread
from collections import defaultdict


class SchedulerTask(object):

    def __init__(self, task_handle, task_delay, task_priority, **task_kwargs):
        self._task_delay = task_delay
        self._priority = task_priority
        self._task_handle = task_handle
        self._kwargs = task_kwargs

    def get_priority(self):
        return self._priority

    def get_task_delay(self):
        return self._task_delay

    def get_task_handle(self):
        return self._task_handle

    def get_task_kwargs(self):
        return self._kwargs

    def set_task_handle(self, task_handle):
        self._task_handle = task_handle

    def set_priority(self, task_priority):
        self._task_delay = task_priority

    def set_task_delay(self, task_delay):
        self._task_delay = task_delay

    def set_task_kwargs(self, **kwargs):
        self._kwargs = kwargs


class CustomScheduler(sched.scheduler):

    def __init__(self, *args, **kwargs):
        sched.scheduler.__init__(self)
        self._task_queue = defaultdict(SchedulerTask)

    def add_task(self, task):

        assert isinstance(task, SchedulerTask)

        task_event = self.enter(
            task.get_task_delay(),
            task.get_priority(),
            task.get_task_handle(),
            kwargs=task.get_task_kwargs(),
        )

        self._task_queue[task] = task_event

    def clear_task_queue(self):

        for task in self._task_queue.keys():
            self.cancel(task)

    def remove_task(self, task):

        self.cancel(self._task_queue[task])
        del self._task_queue[task]

    def start_scheduler_blocking(self):
        self.run(blocking=True)

    def execute_nearest(self):

        current_tasks = len(self.queue)

        while current_tasks == len(self.queue):
            self.run(blocking=False)

    def execute_nearest_non_blocking(self):
        self.run(blocking=False)

    def __str__(self):
        return "Task"


if __name__ == '__main__':

    no_test_tasks = 5

    def foo(**kwargs):
        print("Task {} running at: {}".format(
                kwargs.get("name"),
                time.asctime(),
            )
        )

    sched_test = CustomScheduler(time.time, time.sleep)

    for i in range(no_test_tasks):

        sched_test.add_task(
            SchedulerTask(
                task_delay=i,
                task_priority=i + 1,
                task_handle=foo,
                task_kwargs={"name": "task_"+str(i)}
            )
        )

    def bar():
        while len(sched_test.queue):
            sched_test.execute_nearest_non_blocking()
            time.sleep(1)

    exec_thread = thread.Thread(target=bar, daemon=True)

    print("queue has %d tasks" % (len(sched_test.queue)))
    print("Time now:", time.asctime())

    # sched_test.start_scheduler_blocking()
    # sched_test.execute_nearest_non_blocking()
    exec_thread.start()

    for i in range(no_test_tasks):

        sched_test.add_task(
            SchedulerTask(
                task_delay=(i + 10),
                task_priority=i,
                task_handle=foo,
                task_kwargs={"name": "task_"+str(i+2)}
            )
        )
        sched_test.run()

    print("queue has %d tasks" % (len(sched_test.queue)))

    while len(sched_test.queue):
        time.sleep(1)




