import Image from 'next/image';
import { Product } from '../types/product';

interface ProductCardProps {
  product: Product;
}

export const ProductCard = ({ product }: ProductCardProps) => {
  return (
    <div className="group bg-white rounded-xl shadow-sm hover:shadow-md transition p-4">
      <div className="relative aspect-square rounded-lg mb-4 overflow-hidden">
        <Image
          src={product.images[0] || 'https://placehold.co/600x400'}
          alt={product.title}
          fill
          className="object-cover group-hover:scale-105 transition"
        />
        {product.images.length > 1 && (
          <div className="absolute bottom-2 right-2 bg-white/90 px-2 py-1 rounded-full text-xs text-gray-700">
            +{product.images.length - 1} more
          </div>
        )}
      </div>
      
      <div className="space-y-3">
        <div className="flex justify-between items-start">
          <h3 className="font-semibold text-gray-900 line-clamp-2 flex-1">{product.title}</h3>
          <span className="text-sm text-gray-700 bg-gray-100 px-2 py-1 rounded-full ml-2">
            {product.category.name}
          </span>
        </div>

        <p className="text-2xl text-purple-700 font-semibold">
          ${product.price.toFixed(2)}
        </p>

        <p className="text-gray-600 text-sm line-clamp-3">
          {product.description}
        </p>

        <div className="space-y-2 pt-2 border-t border-gray-100">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <span className="text-xs text-gray-500">Category:</span>
              <span className="text-xs font-medium text-gray-700">{product.category.name}</span>
            </div>
            <span className="text-xs text-gray-500">
              ID: {product.id}
            </span>
          </div>

          <button className="w-full bg-purple-700 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-purple-800 transition">
            Add to Cart
          </button>
        </div>
      </div>
    </div>
  );
}; 