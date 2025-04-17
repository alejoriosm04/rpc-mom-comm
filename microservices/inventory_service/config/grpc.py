from pb import inventory_pb2_grpc, inventory_pb2
from methods.inventory import check_inventory, reduce_stock 
import grpc

class InventoryServiceServicer(inventory_pb2_grpc.InventoryServiceServicer):
    async def CheckInventory(self, request, context):
        try:
            inventory_data = await check_inventory(request.product_id, quantity=1) 
            return inventory_pb2.InventoryResponse(
                available=inventory_data["available"],
                stock=inventory_data["stock"]
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return inventory_pb2.InventoryResponse(available=False, stock=0)

    async def ReduceStock(self, request, context):
        try:
            success = await reduce_stock(request.product_id, request.quantity)
            return inventory_pb2.InventoryUpdateResponse(success=success)
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return inventory_pb2.InventoryUpdateResponse(success=False)
