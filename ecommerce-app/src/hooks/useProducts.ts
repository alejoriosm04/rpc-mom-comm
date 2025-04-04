import { useState, useEffect } from 'react';
import { Product } from '../types/product';
import { productService } from '../services/productService';

export const useProducts = (initialPage: number = 1, initialLimit: number = 12) => {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(initialPage);
  const [total, setTotal] = useState(0);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        setLoading(true);
        const response = await productService.getProducts(page, initialLimit);
        setProducts(response.products);
        setTotal(response.total);
        setError(null);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch products');
      } finally {
        setLoading(false);
      }
    };

    fetchProducts();
  }, [page, initialLimit]);

  return {
    products,
    loading,
    error,
    page,
    total,
    setPage,
  };
}; 