import { useEffect, useState } from 'react';

interface OrderStatus {
  product_id: number;
  quantity: number;
  status: string;
  message: string;
}

export const useOrderStatus = (clientId: string) => {
  const [orderStatus, setOrderStatus] = useState<OrderStatus | null>(null);

  useEffect(() => {
    if (!clientId) return;

    const socket = new WebSocket(`${process.env.NEXT_PUBLIC_WS_URL}/${clientId}`);

    socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.type === 'order_status') {
          setOrderStatus({
            product_id: data.product_id,
            quantity: data.quantity,
            status: data.status,
            message: data.message,
          });
        }
      } catch (err) {
        console.error('[useOrderStatus] WebSocket parse error:', err);
      }
    };

    return () => socket.close();
  }, [clientId]);

  const clearStatus = () => setOrderStatus(null);

  return { orderStatus, clearStatus };
};