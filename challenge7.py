"""
    Advent of Code Day 7
"""
from itertools import count
from common.input_file import get_transformed_input
def get_steps(step_string):
    words = step_string.split()
    return words[1], words[7]

def condense_graph(steps):
    graph = {}
    for s1, s2 in steps:
        graph[s1] = graph.get(s1, []) + [s2]
    return graph

def get_roots(steps):
    nodes = set()
    
    for s1, s2 in steps:
        
        nodes.add(s1)
        nodes.add(s2)
    dests = [s[1] for s in steps] 
    return [n for n in nodes if n not in dests]

def are_prereqs_satisfied(candidate, seq, graph):
    prereqs = [pre for pre, post in graph.items() if candidate in post]
    return all(prereq in seq for prereq in prereqs)

def topo_sort(roots, graph):
    s = ""
    next_input = sorted(roots) 
    while next_input:
        print(s, next_input)
        n = next(n for n in next_input if are_prereqs_satisfied(n, s, graph))         
        if n not in s:
            s += n
        next_input.remove(n)
        next_input = sorted(set(next_input + graph.get(n, [])))
    return s

class Worker:
    def __init__(self):
        self.working = None
        self.tick_finished = 1 


def get_time_taken(topo, graph, num_workers, delay=60):
    workers = [Worker() for _ in range( num_workers)]
    available_jobs = topo
    done = ""
    available_jobs = sorted([n for n in available_jobs if n not in done and n not in (worker.working for worker in workers) and are_prereqs_satisfied(n, done, graph)])
    for tick in count():
        for worker in (w for w in workers if w.working):
            if tick > worker.tick_finished and worker.working is not None:
                done += worker.working
                print(f"{tick}: worker done working on {worker.working}")
                available_jobs = sorted([n for n in topo if n not in done and n not in (worker.working for worker in workers) and are_prereqs_satisfied(n, done, graph)])
                print(f"Available jobs left: {available_jobs}")
                worker.working = None

        for worker in (w for w in workers if not w.working):
            if worker.working is None and available_jobs:
                worker.working, *available_jobs = available_jobs
                worker.tick_finished = tick + delay + (ord(worker.working) - ord('A'))  
                print(f"{tick}: Worker picked up {worker.working}, will finish at {worker.tick_finished}")
                print(f"Done so far: {done} Remaining jobs: {available_jobs}")
        if not available_jobs and all(worker.working is None for worker in workers):
            assert len(done) == len(topo)
            return tick 
        



STEPS = get_transformed_input("input/input7.txt", get_steps)
graph = condense_graph(STEPS)
roots = get_roots(STEPS)
TOPO = topo_sort(roots, graph)
print(get_time_taken( TOPO, graph, 5,60))