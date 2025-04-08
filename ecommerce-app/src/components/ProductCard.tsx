import Image from 'next/image';
import Link from 'next/link';
import { Product } from '../types/product';

interface ProductCardProps {
  product: Product;
}

export const ProductCard = ({ product }: ProductCardProps) => {
  return (
    <Link href={`/products/${product.slug}`} className="block">
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
        <h3 className="font-semibold mb-2 line-clamp-2 text-gray-900">{product.title}</h3>
        <div className="flex justify-between items-center">
          <p className="text-purple-700 font-semibold">${product.price.toFixed(2)}</p>
          <span className="text-sm text-gray-700 bg-gray-100 px-2 py-1 rounded-full">
            {product.category.name}
          </span>
        </div>
      </div>
    </Link>
  );
}; 