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
  const wsBaseUrl = process.env.NEXT_PUBLIC_WS_URL;

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

  // ✅ WebSocket connection
  useEffect(() => {
    if (!clientId) return;

    const socket = new WebSocket(`${wsBaseUrl}/${clientId}`);

    socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);

        // ✅ Si llegan productos en tiempo real
        if (data.products) {
          const productsWithUniqueIds = data.products.map((product: Product, index: number) => ({
            ...product,
            id: product.id ? `${product.id}-${clientId}` : `temp-${index}`
          }));
          setProducts(productsWithUniqueIds);
          setTotal(data.products.length);
          setLoading(false);
          setError(null);
        }

        // ✅ Si llega estado de orden
        if (data.type === 'order_status') {
          const { product_id, status, message, quantity } = data;

          // 🔄 Actualiza el stock localmente si la orden fue confirmada
          if (status === 'confirmed') {
            setProducts(prev =>
              prev.map(p => {
                const cleanId = p.id.toString().split('-')[0];
                if (cleanId === product_id.toString()) {
                  return { ...p, stock: Math.max(0, p.stock - quantity) };
                }
                return p;
              })
            );
          }

          // ✅ Mostrar alerta simple (puedes cambiar por toast)
          alert(`${message} (Status: ${status})`);
        }

      } catch (err) {
        console.error("WebSocket parsing error:", err);
      }
    };

    return () => socket.close();
  }, [clientId, wsBaseUrl]);

  // ✅ Carga inicial de productos
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
