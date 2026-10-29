"""A reusable stack backed by a Python list."""


class Stack:
    """Store items in last-in, first-out order."""

    def __init__(self):
        """Create an empty stack."""
        self._items = []

    def push(self, item):
        """Add an item to the top."""
        self._items.append(item)

    def pop(self):
        """Remove and return the top item; raise IndexError if empty."""
        if self.is_empty():
            raise IndexError("Cannot pop from an empty stack.")
        return self._items.pop()

    def peek(self):
        """Return the top item without removing it; raise IndexError if empty."""
        if self.is_empty():
            raise IndexError("Cannot peek at an empty stack.")
        return self._items[-1]

    def is_empty(self):
        """Return True when the stack has no items."""
        return len(self._items) == 0

    def size(self):
        """Return the number of items."""
        return len(self._items)


if __name__ == "__main__":
    stack = Stack()
    assert stack.is_empty()
    assert stack.size() == 0

    stack.push(10)
    assert stack.size() == 1

    stack.push(20)
    stack.push(30)
    assert stack.size() == 3
    assert stack.peek() == 30
    assert stack.size() == 3

    assert stack.pop() == 30
    assert stack.pop() == 20
    assert stack.pop() == 10
    assert stack.is_empty()
    assert stack.size() == 0

    for operation in (stack.pop, stack.peek):
        try:
            operation()
        except IndexError:
            pass
        else:
            raise AssertionError("Expected IndexError for an empty stack.")

    print("All Stack tests passed.")