import abc

class UnitOfWork(abc.ABC):
    def __init__(self, seen=None):
        self.events = []
        self.seen = seen or set()
        
    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.rollback()

    @abc.abstractmethod
    def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError
    
    def add_event(self, event):
        self.events.append(event)
    
    def pull_events(self):
        while len(self.events) > 0:
            yield self.events.pop(0)
        while len(self.seen):
            obj = self.seen.pop()
            while len(obj.events) > 0:
                yield obj.events.pop(0)