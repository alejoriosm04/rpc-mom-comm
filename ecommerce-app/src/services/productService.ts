import { Product, ProductsResponse } from '../types/product';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'https://api.escuelajs.co/api/v1';

export const productService = {
  async getProducts(page: number = 1, limit: number = 12): Promise<ProductsResponse> {
    try {
      const offset = (page - 1) * limit;
      const response = await fetch(`${API_URL}/products?offset=${offset}&limit=${limit}`);
      if (!response.ok) throw new Error('Failed to fetch products');
      const products = await response.json();
      
      // Transform the response to match our ProductsResponse type
      return {
        products,
        total: 200, // API doesn't provide total, using a default value
        page,
        limit
      };
    } catch (error) {
      console.error('Error fetching products:', error);
      throw error;
    }
  },

  async getProductById(id: number): Promise<Product> {
    try {
      const response = await fetch(`${API_URL}/products/${id}`);
      if (!response.ok) throw new Error('Failed to fetch product');
      return await response.json();
    } catch (error) {
      console.error('Error fetching product:', error);
      throw error;
    }
  },

  async getProductBySlug(slug: string): Promise<Product> {
    try {
      // Since the API doesn't have a direct slug endpoint, we need to fetch all and filter
      const response = await fetch(`${API_URL}/products`);
      if (!response.ok) throw new Error('Failed to fetch products');
      const products = await response.json();
      const product = products.find((p: Product) => p.slug === slug);
      if (!product) throw new Error('Product not found');
      return product;
    } catch (error) {
      console.error('Error fetching product:', error);
      throw error;
    }
  }
}; 