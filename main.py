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
            commits = modifying_commits(project.module_name + test_file, name)
            contributors = [c.author for c in commits]
            last_commit = commits[-1]
            test_file_name = test_file.rsplit('/', maxsplit=1)[-1]
            for method in list_methods(last_commit, test_file_name):
                Method.from_pydriller_method(test_file, method, len(commits), contributors, project)
    with open('projects.json', 'w') as f:
        f.write(jsonpickle.encode(projects))


def list_methods(commit, filename, prefix=""):
    for mod in commit.modifications:
        if mod.filename == filename:
            for method in mod.methods:
                if f"::{prefix}" in method.name:
                    yield method


def modifying_commits(relative_path, name):
    repo = pydriller.RepositoryMining(f"./projects/{name}", filepath=relative_path)
    return list(repo.traverse_commits())


if __name__ == '__main__':
    main()
