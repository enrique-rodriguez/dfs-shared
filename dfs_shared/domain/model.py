class Entity:
    def __init__(self, id):
        self.id = id
        self.events = list()

    def __eq__(self, obj):
        if type(obj) != type(self):
            return False
        return self.id == obj.id
    
    def __hash__(self):
        return hash(self.id)
    
    @classmethod
    def new(cls, *args, **kwargs):
        return cls(*args, **kwargs)


class AggregateRoot(Entity):
    pass
