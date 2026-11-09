class HabitStack:

    def __init__(self):
        self.stack = []

    # PUSH
    def push(self, item):
        self.stack.append(item)

    # POP
    def pop(self):
        if self.stack:
            return self.stack.pop()

        return None

    def display(self):
        return self.stack[::-1]


class HabitQueue:

    def __init__(self):
        self.queue = []

    # ENQUEUE
    def enqueue(self, item):
        self.queue.append(item)

    # DEQUEUE
    def dequeue(self):
        if self.queue:
            return self.queue.pop(0)

        return None

    def display(self):
        return self.queue


def search_habit(habits, name):
    """
    Linear Search
    """

    for habit in habits:

        if habit[1].lower() == name.lower():
            return habit

    return None


def sort_habits(habits):
    """
    Bubble Sort
    Highest performance first.
    """

    arr = habits.copy()

    n = len(arr)

    for i in range(n):

        for j in range(0, n - i - 1):

            if arr[j][1] < arr[j + 1][1]:

                arr[j], arr[j + 1] = (
                    arr[j + 1],
                    arr[j]
                )

    return arr