// ✅ src/hooks/useProducts.ts
import { useState, useEffect, useRef, useCallback } from 'react';
import { Product } from '../types/product';
import { productService } from '../services/productService';
import { v4 as uuidv4 } from 'uuid';

export const useProducts = (initialPage: number = 1, initialLimit: number = 12) => {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(initialPage);
  const [total, setTotal] = useState(0);
  const [clientId, setClientId] = useState<string>('');

  const wsBaseUrl = process.env.NEXT_PUBLIC_WS_URL!;
  const socketRef = useRef<WebSocket | null>(null);
  const reconnectTimeout = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    if (typeof window === 'undefined') return;
    let cid = localStorage.getItem('client_id');
    if (!cid) {
      cid = uuidv4();
      localStorage.setItem('client_id', cid);
    }
    setClientId(cid);
  }, []);

  const fetchProducts = useCallback(async () => {
    if (!clientId) return;
    try {
      setLoading(true);
      const response = await productService.getProducts(page, initialLimit, clientId);
      setProducts(response.products.map(p => ({ ...p, id: `${p.id}-${clientId}` })));
      setTotal(response.total);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error fetching products');
    } finally {
      setLoading(false);
    }
  }, [page, initialLimit, clientId]);

  useEffect(() => { if (clientId) fetchProducts(); }, [clientId, fetchProducts]);

  useEffect(() => {
    if (!clientId) return;

    const connect = () => {
      const socket = new WebSocket(`${wsBaseUrl}/${clientId}`);
      socketRef.current = socket;

      socket.onopen = () => console.log('[WS] Connected ✅');

      socket.onmessage = event => {
        try {
          const data = JSON.parse(event.data);

          if (data.products) {
            setProducts(data.products.map((p: Product, i: number) => ({
              ...p,
              id: `${p.id}-${clientId}` || `temp-${i}`,
            })));
            setTotal(data.products.length);
            setLoading(false);
            setError(null);
          }

          if (data.type === 'order_status' && data.status === 'confirmed') {
            const { product_id, quantity } = data;
            setProducts(prev => prev.map(p => {
              const cleanId = p.id.split('-')[0];
              return cleanId === product_id.toString() ? { ...p, stock: Math.max(0, p.stock - quantity) } : p;
            }));
          }
        } catch (err) {
          console.error('[WS] Parsing error:', err);
        }
      };

      socket.onerror = err => {
        console.error('[WS] Error:', err);
        socket.close();
      };

      socket.onclose = () => {
        console.warn('[WS] Disconnected. Reconnecting...');
        reconnectTimeout.current = setTimeout(connect, 2000);
      };
    };

    connect();
    return () => {
      if (reconnectTimeout.current) clearTimeout(reconnectTimeout.current);
      socketRef.current?.close();
    };
  }, [clientId, wsBaseUrl]);

  const onOrderSuccess = useCallback((localId: string, qty: number) => {
    setProducts(prev => prev.map(p => p.id === localId ? { ...p, stock: Math.max(0, p.stock - qty) } : p));
  }, []);

  return {
    products,
    loading,
    error,
    page,
    total,
    setPage,
    clientId,
    onOrderSuccess,
    refreshProducts: fetchProducts,
  };
};
