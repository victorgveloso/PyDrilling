import pydriller


class Project:
    @classmethod
    def custom_import(cls, name: str, module_name='.'):
        contributions = 0
        for c in pydriller.RepositoryMining(f"./projects/{name}").traverse_commits():
            for m in c.modifications:
                contributions += m.added + m.removed
        return cls(name, f"./projects/{name}/{module_name}", contributions)

    def __init__(self, name: str, path: str, contributions: int, methods=None):
        if methods is None:
            methods = []
        self.total_contributions = contributions
        self.name = name
        self.module_path = path
        self.module_name = path.rsplit('/', maxsplit=2)[-1]
        self.methods = methods

    def __eq__(self, other):
        return self.name == other.name and self.module_path == other.module_path

    def __hash__(self):
        return hash(self.module_path + self.name)

    @staticmethod
    def _file_contains(file, pattern):
        with open(file) as f:
            return pattern in f.read()

    def list_files_containing(self, pattern):
        from glob import iglob
        import itertools
        path = self.module_path + '/**/test/**/*.'
        for file in itertools.chain(iglob(path + 'java', recursive=True), iglob(path + 'kt', recursive=True)):
            if self._file_contains(file, pattern):
                yield file[len(self.module_path):]
