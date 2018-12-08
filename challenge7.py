"""
    Advent of Code Day 7
"""
from itertools import count
from common.graph import DAG
from common.input_file import get_transformed_input

def get_steps(step_string):
    """
        Get a list of steps
    """
    words = step_string.split()
    return words[1], words[7]

def create_graph(steps):
    """
        Create a DAG from the steps
    """
    graph = DAG()
    for source, dest in steps:
        graph.add_edge(source, dest)
    return graph

def get_topologically_sorted_steps(steps):
    """
        Topologically sort the steps
    """
    graph = create_graph(steps)
    out = ""
    while graph:
        node = sorted(graph.get_roots())[0]
        out += node
        graph.remove_node(node)
    return out

class Worker:
    """
        A class of workers that can take and stop a task
    """
    def __init__(self):
        """
            Constructor
        """
        self.task = None
        self.finish_time = 1

    def is_task_finished(self, current_tick):
        """
            Is the task finished?
        """
        return current_tick > self.finish_time

    def start_task(self, task, finish_time):
        """
            Start the task and log the expected time to finish
        """
        self.task = task
        self.finish_time = finish_time

    def pop_task(self):
        """
            Stop working on a task and return it
        """
        task = self.task
        self.task = None
        return task

class WorkerPool:
    """
        A pool of workers
    """

    def __init__(self, number_of_workers):
        """
            Constructor
        """
        self.workers = [Worker() for _ in range(number_of_workers)]

    def get_active_workers(self):
        """
            get a list of all workers who currently have a task
        """
        return [worker for worker in self.workers if worker.task is not None]

    def get_idle_workers(self):
        """
            get a list of all workers who are idle (no task)
        """
        return [worker for worker in self.workers if worker.task is None]

    def get_current_tasks(self):
        """
            Get a list of all tasks being worked
        """
        return [worker.task for worker in self.get_active_workers()]

    def is_task_in_progress(self, task):
        """
            Return true if a task in progress
        """
        return task in self.get_current_tasks()

    def are_all_workers_idle(self):
        """
            Return true if all workers are idle
        """
        return len(self.get_idle_workers()) == len(self.workers)

def get_available_jobs(graph, workers):
    """
        Get a list of nodes that are roots and not currently being worked
    """
    return sorted(node for node in graph.get_roots() if not workers.is_task_in_progress(node))

def finish_jobs(tick, workers, graph):
    """
        Finish any jobs that are outstanding at this tick
    """

    finished = ""
    for worker in workers.get_active_workers():
        if worker.is_task_finished(tick):
            graph.remove_node(worker.task)
            finished += worker.pop_task()
    return finished

def start_new_jobs(tick, workers, graph, delay):
    """
        See if there are any new jobs to start
    """
    for worker in workers.get_idle_workers():
        available_jobs = get_available_jobs(graph, workers)
        if available_jobs:
            task = available_jobs[0]
            finish_time = tick + delay + (ord(task) - ord('A'))
            worker.start_task(task, finish_time)


def get_total_time_needed(sorted_input, steps, number_of_workers, delay=60):
    """
        Get the total time needed to finish all the jobs
    """
    graph = create_graph(steps)
    workers = WorkerPool(number_of_workers)
    finished = ""
    for tick in count():
        finished += finish_jobs(tick, workers, graph)
        start_new_jobs(tick, workers, graph, delay)

        if len(finished) == len(sorted_input):
            return tick
    raise RuntimeError("Unreachable Code")

STEPS = get_transformed_input("input/input7.txt", get_steps)
TOPO = get_topologically_sorted_steps(STEPS)
if __name__ == "__main__":
    print(TOPO)
    print(get_total_time_needed(TOPO, STEPS, 5))
