from pydriller import Commit


class CustomCommit(Commit):
    def __hash__(self):
        return hash(self.hash)

    def __eq__(self, other):
        return self is other or self.__dict__ == other.__dict__
