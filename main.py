from typing import Dict

import jsonpickle as jsonpickle
import pydriller

from cache import TestIndex
from commit import CustomCommit
from project import Project
from method import Method
import re


def main():
    projects: Dict[str, Project] = {
        'commons-lang': Project.custom_import('commons-lang'),
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
            for method in list_methods(last_commit, test_file_name):
                if re.match('(?:[a-zA-Z0-9.]::){1,2}(?:setUp|tearDown)', method.name) is not None:
                    continue
                method_modifying_commits = set()
                for c in commits:
                    for m in c.modifications:
                        if method.filename == m.filename:
                            if method.start_line in [idx for idx, diff in m.diff_parsed['added']]:
                                method_modifying_commits.add(CustomCommit(c))
                                print(f'name: {method.name}')
                                print(f'author: {c.author}')
                                print(f'first line: {method.start_line}')
                                print(f'commit: {c.hash}')
                            # if method in m.methods and method not in m.methods_before:
                            #     method_modifying_commits.add(CustomCommit(c))
                            if method in m.changed_methods:
                                method_modifying_commits.add(CustomCommit(c))
                contributors = [c.author for c in method_modifying_commits]
                Method.from_pydriller_method(test_file, method, len(method_modifying_commits), contributors, project)
    with open('resources/projects.json', 'w') as f:
        f.write(jsonpickle.encode(projects))


def list_methods(commit, filename, prefix=""):
    for mod in commit.modifications:
        if mod.filename == filename:
            for method in mod.methods:
                if f"::{prefix}" in method.name:
                    yield method


def file_modifying_commits(relative_path, name):
    repo = pydriller.RepositoryMining(f"./projects/{name}", filepath=relative_path)
    return list(repo.traverse_commits())


if __name__ == '__main__':
    main()
