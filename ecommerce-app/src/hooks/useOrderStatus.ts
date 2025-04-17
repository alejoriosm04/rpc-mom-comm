import { useEffect, useState } from 'react';

interface OrderStatus {
  product_id: number;
  quantity: number;
  status: string;
  message: string;
}

export const useOrderStatus = (clientId: string | null) => {
  const [orderStatus, setOrderStatus] = useState<OrderStatus | null>(null);

  useEffect(() => {
    if (!clientId) return;

    const socket = new WebSocket(`ws://localhost:8000/ws/${clientId}`);

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);

      if (data.type === 'order_status') {
        setOrderStatus({
          product_id: data.product_id,
          quantity: data.quantity,
          status: data.status,
          message: data.message,
        });
      }
    };

    return () => socket.close();
  }, [clientId]);

  const clearStatus = () => setOrderStatus(null);

  return { orderStatus, clearStatus };
};
