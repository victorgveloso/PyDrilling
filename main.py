from typing import Dict

import jsonpickle as jsonpickle
import pydriller

from cache import TestIndex
from method import Method
from project import Project


def main():
    projects: Dict[str, Project] = {
        'okhttp': Project.custom_import('okhttp', 'okhttp'),
        'retrofit': Project.custom_import('retrofit', 'retrofit'),
        'RxJava': Project.custom_import('RxJava'),
        'zxing': Project.custom_import('zxing', 'core')
    }

    TestIndex.cache_test_files(projects)
    for name, project in projects.items():
        for test_file in TestIndex.iter_test_files(name):
            commits = file_modifying_commits(project.module_name + test_file, name)
            last_commit = commits[-1]
            test_file_name = test_file.rsplit('/', maxsplit=1)[-1]
            changed_methods = {}
            for c in commits:
                for mod in c.modifications:
                    for m in mod.changed_methods:
                        changed_methods[m] = c
            method_modifying_commits = set()
            for method in list_methods(last_commit, test_file_name):
                if method in changed_methods:
                    method_modifying_commits.add(changed_methods[method])
                contributors = [c.author for c in method_modifying_commits]
                Method.from_pydriller_method(test_file, method, len(method_modifying_commits), contributors, project)
    with open('projects.json', 'w') as f:
        f.write(jsonpickle.encode(projects))


def list_methods(commit, filename, prefix=""):
    for mod in commit.modifications:
        if mod.filename == filename:
            for method in mod.methods:
                if f"::{prefix}" in method.name:
                    yield method


def file_modifying_commits(relative_path, name):
    repo = pydriller.RepositoryMining(f"./projects/{name}", filepath=relative_path)

    def convert(commit):
        from commit import CustomCommit
        commit.__class__ = CustomCommit
        return commit

    return list(map(convert, repo.traverse_commits()))


if __name__ == '__main__':
    main()
