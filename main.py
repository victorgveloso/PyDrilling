from typing import Dict, Set, Union, Tuple, List

import jsonpickle as jsonpickle
from pydriller.domain.commit import Method as PyDrillerMethod

from cache import TestIndex
from commit import CustomCommit
from method import Method
from project import Project


class PyDrillingController:
    def __init__(self):
        self.project_args: List[Tuple[str, str]] = [('okhttp', 'okhttp'), ('retrofit', 'retrofit'), ('RxJava', '.'),
                                                    ('zxing', 'core')]
        self.projects: Union[Dict[str, Project], None] = None

    @staticmethod
    def _import_and_cache(name, module) -> Project:
        project = Project.custom_import(name, module)
        TestIndex.cache_test_files(name, project)
        return project

    def load(self):
        from multiprocessing import Pool
        with Pool(4) as p:
            results = p.starmap(PyDrillingController._import_and_cache, self.project_args)
        self.projects = {project.name: project for project in results}

    def process(self):
        if self.projects is None:
            self.projects = {}
            for name, module in self.project_args:
                with open(f'{name}.json', 'r') as f:
                    project: Project = jsonpickle.decode(f.read())
                    self.projects[project.name] = project

        for name, project in self.projects.items():
            test_files = TestIndex.iter_test_files(name)
            test_methods: Dict[PyDrillerMethod, Set[CustomCommit]] = {}
            for commit in project.commits:
                for method in commit.modified_methods:
                    if method.filename in test_files:
                        if method in test_methods:
                            test_methods[method].add(commit)
                        else:
                            test_methods[method] = set()
            for method, commits in test_methods.items():
                contributors = {commit.author.email for commit in commits}
                new_method = Method.from_pydriller_method(method.filename, method, len(commits), contributors, project)
                project.methods.append(new_method)

    def visualize(self):
        from statistics import mean, median, stdev, StatisticsError
        with open("output.csv", "w") as f:
            f.write(
                "Project,Package,Method,SLOC,Complexity,ModifyingCommits,Contributors," +
                "MaxExperienced,MinExperienced,MeanExperience,MedianExperience,StdevExperience\n")
        for project_name, project in self.projects.items():
            for test in project.methods:
                experiences = [c.experience for c in test.contributors]
                with open("output.csv", "a") as f:
                    try:
                        stdev_xp = str(stdev(experiences))
                    except StatisticsError:
                        stdev_xp = "None"
                    f.write(','.join([project_name, test.package, test.name, str(test.nloc), str(test.complexity),
                                      str(test.n_commits), str(len(experiences)), str(max(experiences)),
                                      str(min(experiences)), str(mean(experiences)), str(median(experiences)),
                                      stdev_xp]) + '\n')


def main():
    ctrl = PyDrillingController()
    abort = False
    while not abort:
        answer = input('What do you want to do? (load,abort,process,visualize)')
        if answer == 'abort':
            abort = True
        elif answer == 'load':
            ctrl.load()
        elif answer == 'process':
            ctrl.process()
        elif answer == 'visualize':
            ctrl.visualize()
        else:
            print("Please, provide a valid answer (load,abort,process,visualize)")


if __name__ == '__main__':
    main()
