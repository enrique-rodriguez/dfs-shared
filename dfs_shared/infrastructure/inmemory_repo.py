from dfs_shared.domain.repository import Repository


class InMemoryRepository(Repository):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.collection = set()

    def _get(self, id):
        try:
            return next(o for o in self.collection if o.id == id)
        except StopIteration:
            return None

    def get_by_spec(self, spec):
        for obj in self.collection:
            if spec.criteria(obj):
                return obj
        return None

    def _save(self, obj):
        self.collection.add(obj)

    def _delete(self, obj):
        self.collection = set(filter(lambda o: o != obj, self.collection))

    def _update(self, obj):
        pass

    def rollback(self, obj):
        pass
