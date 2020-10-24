from typing import Collection

from pydriller.domain.developer import Developer
import pydriller.domain.commit

from contributor import Contributor
from project import Project


class Method:
    @classmethod
    def from_pydriller_method(cls, path: str, method: pydriller.domain.commit.Method, n_commits: int,
                              developers: Collection[Developer], project: Project):
        # /src/test/java/package/file.java -> .src.test.java.package.file.java
        package = path.replace('/', '.')
        # .src.test.java.package.file.java -> src.test.java.package.file.class
        package = package.lstrip('.')
        # src.test.java.package.file.class -> package.file.java
        package = package.split('.', maxsplit=3)[-1]
        # package.file.class -> package
        package = package.rsplit('.', maxsplit=2)[0]

        contributors = {Contributor.from_pydriller_method(c, project) for c in developers}

        new_method = cls(package, method.name, method.nloc, method.complexity, n_commits, contributors)

        project.methods.append(new_method)

        return new_method

    def __init__(self, package: str, name: str, nloc: int, complexity: int, n_commits: int,
                 contributors: Collection[Contributor]):
        self.package = package
        self.name = name
        self.nloc = nloc
        self.complexity = complexity
        self.n_commits = n_commits
        self.contributors = contributors

    def __hash__(self):
        return hash(self.package + self.name)

    def __repr__(self):
        return f"{self.package}.{self.name}(SLOC={self.nloc},Complexity={self.complexity})"

    def __str__(self):
        return f"{self.package}.{self.name}"

    def __eq__(self, other):
        return self.package == other.package and self.name == other.name
