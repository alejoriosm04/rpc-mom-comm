const API_URL = process.env.NEXT_PUBLIC_API_URL;

export const orderService = {
  async createOrder(product_id: number, quantity: number, client_id: string) {
    const res = await fetch(`${API_URL}/orders/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': process.env.NEXT_PUBLIC_API_KEY || '',
      },
      body: JSON.stringify({ product_id, quantity, client_id }),
    });

    if (!res.ok) throw new Error('Failed to create order');
    return res.json();
  },
};