class MockCursor:
    def __init__(self, docs):
        self.docs = docs

    def __aiter__(self):
        return self

    async def __anext__(self):
        if not self.docs:
            raise StopAsyncIteration
        return self.docs.pop(0)

class MockProductsCollection:
    def __init__(self, data):
        self.data = data

    def find(self):
        return MockCursor(self.data.copy())
