'use client';

import Image from 'next/image';
import { useState } from 'react';
import { Product } from '../types/product';
import { orderService } from '../services/orderService';

interface Props {
  product: Product;
  clientId: string;
  onOrderSuccess: (qty: number) => void;
}

export const ProductCard = ({ product, clientId, onOrderSuccess }: Props) => {
  const [qty, setQty] = useState(1);
  const [message, setMessage] = useState('');
  const [statusType, setStatus] = useState<'success' | 'warning' | 'error' | null>(null);
  const [loading, setLoading] = useState(false);

  const idNum = parseInt(product.id.split('-')[0], 10);
  const out = product.stock === 0;

  const handleOrder = async () => {
    if (!clientId) return;
    if (qty < 1 || qty > product.stock) {
      setMessage('Cantidad inválida');
      setStatus('warning');
      return;
    }

    setLoading(true);
    setMessage('');
    setStatus(null);

    try {
      const res = await orderService.createOrder(idNum, qty, clientId);
      setMessage(res.message);
      setStatus(
        res.status === 'confirmed' ? 'success' :
        res.status === 'pending'  ? 'warning' : 'error'
      );

      if (res.status === 'confirmed') {
        onOrderSuccess(qty);
      }
    } catch {
      setMessage('Servicio no disponible');
      setStatus('error');
    } finally {
      setLoading(false);
      setTimeout(() => setMessage(''), 4000);
    }
  };

  return (
    <div className="group bg-white rounded-xl shadow-sm hover:shadow-md transition p-4 flex flex-col">
      <div className="relative aspect-square rounded-lg mb-4 overflow-hidden">
        <Image
          src={product.images[0] || 'https://placehold.co/600x400'}
          alt={product.title}
          fill
          className="object-cover"
        />
      </div>

      <h3 className="font-semibold text-gray-900 line-clamp-2">{product.title}</h3>
      <p className="mt-1 text-sm text-gray-500">{product.category.name}</p>
      <p className="mt-2 text-2xl font-extrabold text-purple-600">${product.price.toFixed(2)}</p>
      <p className="mt-1 text-sm font-medium text-green-600">Stock: {product.stock}</p>

      <div className="mt-4 flex items-center space-x-2">
        <input
          type="number"
          min={1}
          max={product.stock}
          value={qty}
          onChange={e => setQty(Number(e.target.value))}
          className="w-20 px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-400 transition"
        />
        <button
          disabled={loading || out}
          onClick={handleOrder}
          className={`flex-1 px-4 py-2 rounded-lg text-white font-medium transition ${
            out ? 'bg-gray-300 cursor-not-allowed' : 'bg-purple-700 hover:bg-purple-800'
          }`}
        >
          {loading ? 'Processing...' : out ? 'No stock' : 'Add to Cart'}
        </button>
      </div>

      {message && (
        <p className={`mt-2 text-center text-sm ${
          statusType === 'success' ? 'text-green-600' :
          statusType === 'warning' ? 'text-yellow-600' :
          'text-red-600'
        }`}>
          {message}
        </p>
      )}
    </div>
  );
};
