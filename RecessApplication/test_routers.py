from .router import OptionalSlashRouter

# All test files should start with 'test_'
# Standard convention is test_<name of thing being tested>

# All test classes should start with 'Test'
class TestRouters:

    def mock_router(self):
        router = OptionalSlashRouter()
        return router

    # All tests should start with 'test_'

    def test_has_trailing_slash(self):
        router = self.mock_router()
        assert router.trailing_slash == '/?'

