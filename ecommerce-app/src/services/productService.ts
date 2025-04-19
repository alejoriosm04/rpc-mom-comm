import { ProductsResponse } from '@/types/product';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';
const API_KEY = process.env.NEXT_PUBLIC_API_KEY || '';

export const productService = {
  async getProducts(page: number = 1, limit: number = 12, client_id?: string): Promise<ProductsResponse> {
    const query = new URLSearchParams({ page: String(page), limit: String(limit) });
    if (client_id) query.append('client_id', client_id);

    const res = await fetch(`${API_URL}/products/?${query.toString()}`, {
      headers: { 'x-api-key': API_KEY },
    });

    if (!res.ok) throw new Error('Failed to fetch products');

    return res.json();
  },
};