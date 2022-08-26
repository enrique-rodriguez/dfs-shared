import abc


class Repository(abc.ABC):
    def __init__(self, seen):
        self.seen = seen
        
    def save(self, obj):
        self.seen.add(obj)
        self._save(obj)

    def get(self, id):
        obj = self._get(id)
        if obj:
            self.seen.add(obj)
        return obj
    
    def delete(self, id):
        obj = self.get(id)
        if obj:
            self._delete(obj)
    
    def update(self, obj):
        self.seen.add(obj)
        self._update(obj)
    
    @abc.abstractmethod
    def get_by_spec(self, spec):
        raise NotImplementedError
    
    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError

    @abc.abstractmethod
    def _save(self, obj):
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, obj):
        raise NotImplementedError
    
    @abc.abstractmethod
    def _delete(self, obj):
        raise NotImplementedError
    
    @abc.abstractmethod
    def _update(self, obj):
        raise NotImplementedError
        

class RepositoryManager:
    repo_class = None

    def __init__(self, seen):
        self.seen = seen
        self.repositories = dict()

    def get_repo(self, entity):
        if entity not in self.repositories:
            self.repositories[entity] = self.repo_class(self.seen)
        return self.repositories[entity]
    
    def get(self, obj_class, id):
        repo = self.get_repo(obj_class)
        return repo.get(id)
    
    def get_by_spec(self, obj_class, spec):
        repo = self.get_repo(obj_class)
        return repo.get_by_spec(spec)

    def save(self, obj):
        repo = self.get_repo(type(obj))
        repo.save(obj)
    
    def update(self, obj):
        repo = self.get_repo(type(obj))
        repo.update(obj)
    
    def delete(self, obj):
        repo = self.get_repo(type(obj))
        repo._delete(obj)