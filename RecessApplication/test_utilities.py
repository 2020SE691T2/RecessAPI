from .models import CustomUser

class TestLogger:
    def info(self, *args, **kwargs):
        return

class MockQueryParameter:
    data = {}

    def get(self, key):
        return self.data[key]

    def set(self, data):
        self.data = data

class MockRequest:
    data = {}
    user = CustomUser()
    GET = MockQueryParameter()

class MockResponse:
    content = b'{}'
    status_code = 0