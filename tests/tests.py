


import unittest

# Your module imported assuming working directory
# is root of repository. See workflow in repository
# for example running of test cases.
import entrypoint as ep

class TestSomething(unittest.TestCase) :

    def test_sometestcase(self) :
        # Unit test cases would go in these
        # test methods to test the various
        # Python functions, methods, etc.
        pass

    def test_anothertestcase(self) :
        pass
