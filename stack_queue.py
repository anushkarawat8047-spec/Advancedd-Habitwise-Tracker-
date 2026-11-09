# ==========================================
# stack_queue.py
# DSA Module
# Stack and Queue
# ==========================================


# ==========================================
# STACK
# ==========================================

class HabitStack:

    def __init__(self):

        self.stack = []


    # PUSH operation
    def push(self, habit):

        self.stack.append(habit)


    # POP operation
    def pop(self):

        if len(self.stack) == 0:

            return None

        return self.stack.pop()


    # Display stack
    def display(self):

        return self.stack[::-1]


# ==========================================
# QUEUE
# ==========================================

class HabitQueue:

    def __init__(self):

        self.queue = []


    # ENQUEUE operation
    def enqueue(self, habit):

        self.queue.append(habit)


    # DEQUEUE operation
    def dequeue(self):

        if len(self.queue) == 0:

            return None

        return self.queue.pop(0)


    # Display queue
    def display(self):

        return self.queue