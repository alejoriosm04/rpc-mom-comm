// src/hooks/useSocket.ts
import { useState, useEffect, useRef, useCallback } from 'react';
import { Product } from '../types/product';
import { v4 as uuidv4 } from 'uuid';

export type OrderStatus = {
  product_id: number;
  quantity: number;
  status: string;
  message: string;
};

export const useSocket = (
  wsUrl: string,
  onProducts: (products: Product[]) => void,
  onOrderStatus: (status: OrderStatus) => void
): string => {
  const [clientId, setClientId] = useState<string>('');
  const socketRef = useRef<WebSocket | null>(null);
  const retryRef  = useRef<number | null>(null);

  useEffect(() => {
    let cid = localStorage.getItem('client_id');
    if (!cid) {
      cid = uuidv4();
      localStorage.setItem('client_id', cid);
    }
    setClientId(cid);
  }, []);

  const connect = useCallback(() => {
    if (!clientId) return;
    const ws = new WebSocket(`${wsUrl}/${clientId}`);
    socketRef.current = ws;

    ws.onopen = () => {
      console.log(`[WS] Connected as ${clientId}`);
    };

    ws.onmessage = e => {
      try {
        const msg = JSON.parse(e.data);
        if (msg.products) onProducts(msg.products as Product[]);
        if (msg.type === 'order_status') onOrderStatus(msg as OrderStatus);
      } catch (err) {
        console.error('[WS] parse error', err);
      }
    };

    ws.onclose = () => {
      console.warn('[WS] Disconnected — retry in 2s');
      retryRef.current = window.setTimeout(connect, 2000);
    };

    ws.onerror = err => {
      console.error('[WS] error', err);
      ws.close();
    };
  }, [wsUrl, clientId, onProducts, onOrderStatus]);

  useEffect(() => {
    connect();
    return () => {
      if (retryRef.current !== null) clearTimeout(retryRef.current);
      socketRef.current?.close();
    };
  }, [connect]);

  return clientId;
};
