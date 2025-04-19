import { ProductsResponse } from '../types/product';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';
const API_KEY = process.env.NEXT_PUBLIC_API_KEY || '';

export const productService = {
  async getProducts(page: number = 1, limit: number = 12, client_id?: string): Promise<ProductsResponse> {
    try {
      const offset = (page - 1) * limit;
      const query = `page=${page}&limit=${limit}` + (client_id ? `&client_id=${client_id}` : '');

      const response = await fetch(`${API_URL}/products/?${query}`, {
        headers: {
          'x-api-key': API_KEY,
        },
      });

      if (!response.ok) throw new Error('Failed to fetch products');

      const data = await response.json();
      return {
        products: data.products,
        total: data.total,
        page: data.page,
        limit: data.limit,
      };
    } catch (error) {
      console.error('Error fetching products:', error);
      throw error;
    }
  },
};
