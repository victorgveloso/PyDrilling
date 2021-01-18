from typing import Collection

from pydriller.domain.commit import Method as PyDrillerMethod
from pydriller import Commit


class CustomCommit:
    def __init__(self, commit: Commit):
        self.commit = commit
        self._modified_methods = set()

    def __hash__(self):
        return hash(self.commit.hash)

    def __eq__(self, other):
        return self.commit is other.commit or self.commit.__dict__ == other.commit.__dict__

    @property
    def modified_methods(self) -> Collection[PyDrillerMethod]:
        return self._modified_methods

    def add_modified_method(self, method: PyDrillerMethod):
        self._modified_methods.add(method)

    @property
    def dmm_unit_interfacing(self):
        return self.commit.dmm_unit_interfacing

    @property
    def dmm_unit_complexity(self):
        return self.commit.dmm_unit_complexity

    @property
    def dmm_unit_size(self):
        return self.commit.dmm_unit_size

    @property
    def branches(self):
        return self.commit.branches

    @property
    def in_main_branch(self):
        return self.commit.in_main_branch

    @property
    def modifications(self):
        return self.commit.modifications

    @property
    def merge(self):
        return self.commit.merge

    @property
    def parents(self):
        return self.commit.parents

    @property
    def msg(self):
        return self.commit.msg

    @property
    def committer_timezone(self):
        return self.commit.committer_timezone

    @property
    def author_timezone(self):
        return self.commit.author_timezone

    @property
    def committer_date(self):
        return self.commit.committer_date

    @property
    def author_date(self):
        return self.commit.author_date

    @property
    def project_path(self):
        return self.commit.project_path

    @property
    def project_name(self):
        return self.commit.project_name

    @property
    def committer(self):
        return self.commit.committer

    @property
    def author(self):
        return self.commit.author

    @property
    def hash(self):
        return self.commit.hash
