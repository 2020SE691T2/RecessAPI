class TestLogger:
    def info(self, *args, **kwargs):
        return

class MockRequest:
    data = {}

class MockResponse:
    content = b'{}'
    status_code = 0