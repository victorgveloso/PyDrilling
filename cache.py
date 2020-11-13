class TestIndex:
    suffix = "Files.csv"

    @staticmethod
    def generate_cache_filename(name):
        return f"{name}{TestIndex.suffix}"

    @staticmethod
    def iter_test_files(name):
        with open(TestIndex.generate_cache_filename(name)) as f:
            lines = f.readlines()
        for line in lines:
            yield ''.join(line.split(',')[1:-1])

    @staticmethod
    def cache_test_files(name, project):
        with open(TestIndex.generate_cache_filename(name), 'w') as f:
            f.write('\n'.join({f"{name}," + file + "," for file in project.list_files_containing('@Test')}))
