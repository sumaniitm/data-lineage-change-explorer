"""
This class implements the queue data structure.
The enqueue method adds an element at the rear of the queue.
The dequeue method removes an element from the front of the queue.
The is_empty method checks if a queue is empty or not.
"""

import sys

sys.path.append('.')


class Queue:
    def __init__(self):
        self.queue = []
        
    def enqueue(self, element):
        self.queue.append(element)
        
    def dequeue(self):
        if self.queue:
            a = self.queue[0]
            self.queue.remove(a)
            return a
        else:
            print('Queue is empty')
        
    def is_empty(self):
        return self.queue == []
