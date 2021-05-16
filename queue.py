import os
import sys
import json

sys.path.append('.')

class Queue:
    def __init__(self):
        self.queue = []
        
    def enQueue(self, element):
        self.queue.append(element)
        
    def deQueue(self):
        if self.queue:
            a = self.queue[0]
            self.queue.remove(a)
            return a
        else:
            print('Queue is empty')
        
    def isEmpty(self):
        return self.queue == []