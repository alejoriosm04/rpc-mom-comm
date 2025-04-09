import { useState, useEffect } from 'react';
import { Product } from '../types/product';
import { productService } from '../services/productService';
import { v4 as uuidv4 } from 'uuid';

export const useProducts = (initialPage: number = 1, initialLimit: number = 12) => {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(initialPage);
  const [total, setTotal] = useState(0);
  const [clientId, setClientId] = useState<string | null>(null);

  useEffect(() => {
    if (typeof window !== 'undefined') {
      let cid = localStorage.getItem("client_id");
      if (!cid) {
        cid = uuidv4();
        localStorage.setItem("client_id", cid);
      }
      setClientId(cid);
    }
  }, []);

  useEffect(() => {
    if (!clientId) return;

    const socket = new WebSocket(`ws://localhost:8000/ws/${clientId}`);
    socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.products) {
          setProducts(data.products);
          setTotal(data.products.length);
          setLoading(false);
          setError(null);
        }
      } catch (err) {
        console.error("WebSocket parsing error:", err);
      }
    };
    return () => socket.close();
  }, [clientId]);

  useEffect(() => {
    if (!clientId) return;

    const fetchProducts = async () => {
      try {
        setLoading(true);
        const response = await productService.getProducts(page, initialLimit, clientId);
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
  }, [page, initialLimit, clientId]);

  return {
    products,
    loading,
    error,
    page,
    total,
    setPage,
  };
};
