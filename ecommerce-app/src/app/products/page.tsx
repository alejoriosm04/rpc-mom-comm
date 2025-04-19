'use client';

import { useEffect } from 'react';
import { useProducts } from '../../hooks/useProducts';
import { useOrderStatus } from '../../hooks/useOrderStatus';
import { ProductCard } from '../../components/ProductCard';

export default function ProductsPage() {
  const {
    products,
    loading,
    error,
    page,
    total,
    setPage,
    clientId,
    onOrderSuccess,
    refreshProducts,
  } = useProducts();

  const { orderStatus, clearStatus } = useOrderStatus(clientId);

  useEffect(() => {
    if (orderStatus) {
      alert(`${orderStatus.message} (Status: ${orderStatus.status})`);
      clearStatus();
      if (orderStatus.status === 'confirmed') {
        refreshProducts(); // Refrescar productos si fue confirmada
      }
    }
  }, [orderStatus, clearStatus, refreshProducts]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin h-12 w-12 rounded-full border-t-4 border-purple-600" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-red-600 font-semibold">Error: {error}</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen py-16 bg-gray-50">
      <div className="container mx-auto px-6">
        <h1 className="text-4xl font-extrabold mb-12 text-center text-purple-700">
          Our Products
        </h1>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
          {products.map(product => (
            <ProductCard
              key={product.id}
              product={product}
              clientId={clientId}
              onOrderSuccess={qty => onOrderSuccess(product.id, qty)}
            />
          ))}
        </div>
        <div className="mt-12 flex justify-center gap-4">
          <button
            onClick={() => setPage(p => Math.max(1, p - 1))}
            disabled={page === 1}
            className="px-4 py-2 rounded-lg bg-purple-100 text-purple-700"
          >
            Previous
          </button>
          <span className="px-4 py-2">{page} / {Math.ceil(total / 12)}</span>
          <button
            onClick={() => setPage(p => p + 1)}
            disabled={page >= Math.ceil(total / 12)}
            className="px-4 py-2 rounded-lg bg-purple-100 text-purple-700"
          >
            Next
          </button>
        </div>
      </div>
    </div>
  );
}
