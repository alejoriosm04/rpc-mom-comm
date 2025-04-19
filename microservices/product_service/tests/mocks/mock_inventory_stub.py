class MockInventoryStub:
    async def CheckInventory(self, request):
        class Response:
            stock = 99 
        return Response()
