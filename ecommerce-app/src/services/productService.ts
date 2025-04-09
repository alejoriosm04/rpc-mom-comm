import { ProductsResponse } from '../types/product';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'https://api.escuelajs.co/api/v1';

export const productService = {
  async getProducts(page: number = 1, limit: number = 12, client_id?: string): Promise<ProductsResponse> {
    try {
      const offset = (page - 1) * limit;
      const query = `offset=${offset}&limit=${limit}` + (client_id ? `&client_id=${client_id}` : '');
      const response = await fetch(`${API_URL}/products/?${query}`);
      if (!response.ok) throw new Error('Failed to fetch products');
  
      // ✅ Esta línea fue cambiada
      const data = await response.json(); // data es { products, total, page, limit }
  
      return {
        products: data.products, // aseguras que products es un array
        total: data.total,
        page: data.page,
        limit: data.limit
      };
    } catch (error) {
      console.error('Error fetching products:', error);
      throw error;
    }
  }
}; 