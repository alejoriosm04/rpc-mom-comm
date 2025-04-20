import { useState, useEffect, useRef, useCallback } from 'react';
import { v4 as uuidv4 } from 'uuid';
import { Product } from '@/types/product';
import { productService } from '@/services/productService';

const RETRY_INTERVAL_MS = 5000;

export const useProducts = (initialPage: number = 1, initialLimit: number = 12) => {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState<number>(initialPage);
  const [total, setTotal] = useState<number>(0);
  const [clientId, setClientId] = useState<string>('');

  const wsBaseUrl = process.env.NEXT_PUBLIC_WS_URL!;
  const socketRef = useRef<WebSocket | null>(null);
  const reconnectTimeout = useRef<NodeJS.Timeout | null>(null);
  const retryTimer = useRef<NodeJS.Timeout | null>(null);

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
      const resp = await productService.getProducts(page, initialLimit, clientId);
      setProducts(resp.products.map((p) => ({ ...p, id: `${p.id}-${clientId}` })));
      setTotal(resp.total);
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

    if (retryTimer.current) clearInterval(retryTimer.current);

    if (error || (!loading && products.length === 0)) {
      retryTimer.current = setInterval(fetchProducts, RETRY_INTERVAL_MS);
    }

    return () => { if (retryTimer.current) clearInterval(retryTimer.current); };
  }, [error, products.length, loading, clientId, fetchProducts]);

  useEffect(() => {
    if (!clientId) return;

    const connect = () => {
      const socket = new WebSocket(`${wsBaseUrl}/${clientId}`);
      socketRef.current = socket;

      socket.onopen = () => console.log('[WS] Connected ✅');

      socket.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);

          if (Array.isArray(data.products)) {
            setProducts(data.products.map((p: Product) => ({ ...p, id: `${p.id}-${clientId}` })));
            setTotal(data.products.length);
            setError(null);
            setLoading(false);
            return;
          }

          if (data.type === 'order_status' && data.status === 'confirmed') {
            const { product_id, quantity } = data;
            setProducts((prev) =>
              prev.map((p) => (p.id.split('-')[0] === String(product_id) ? { ...p, stock: Math.max(0, p.stock - quantity) } : p))
            );
          }
        } catch (err) {
          console.error('[WS] Parse error', err);
        }
      };

      socket.onerror = (err) => {
        console.error('[WS] Error', err);
        socket.close();
      };

      socket.onclose = () => {
        console.warn('[WS] Closed – retrying…');
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
    setProducts((prev) => prev.map((p) => (p.id === localId ? { ...p, stock: Math.max(0, p.stock - qty) } : p)));
  }, []);

  return { products, loading, error, page, total, setPage, clientId, onOrderSuccess, refreshProducts: fetchProducts };
};