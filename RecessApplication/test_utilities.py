from .models import CustomUser

class TestLogger:
    def info(self, *args, **kwargs):
        return

class MockRequest:
    data = {}
    user = CustomUser()

class MockResponse:
    content = b'{}'
    status_code = 0