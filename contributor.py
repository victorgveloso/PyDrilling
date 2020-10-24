from pydriller.domain.developer import Developer

from project import Project
import pydriller


class Contributor:
    contributors = {}

    @staticmethod
    def measure_experience(project: Project, author) -> float:
        author_contributions = 0
        for c in pydriller.RepositoryMining(f"./projects/{project.name}", only_authors=[author]).traverse_commits():
            author_contributions += sum([m.added + m.removed for m in c.modifications])
        return author_contributions / project.total_contributions

    @classmethod
    def from_pydriller_method(cls, contributor: Developer, project: Project):
        if contributor.email not in cls.contributors:
            cls.contributors[contributor.email] = cls(contributor.name, contributor.email,
                                                      experience=cls.measure_experience(project, contributor.name))
        return cls.contributors[contributor.email]

    def __init__(self, name: str, email: str, experience: float):
        self.name = name
        self.email = email
        self.experience = experience

    def __str__(self):
        return f"{self.name}<{self.email}>: XP={self.experience}"

    def __repr__(self):
        return f"{self.name}<{self.email}>: XP={self.experience}"

    def __hash__(self):
        return hash(self.name + self.email)

    def __eq__(self, other):
        return self.name == other.name and self.email == other.email
