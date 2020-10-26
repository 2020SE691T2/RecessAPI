# All test files should start with 'test_'
# Standard convention is test_<name of thing being tested>

# All test classes should start with 'Test'
class TestTest:
    def func(self, x):
        return x + 1

    # All tests should start with 'test_'
    def test_answer(self):
        assert self.func(4) == 5
