export interface Category {
  id: number;
  name: string;
  image: string;
  slug: string;
}

// En el archivo `types/product.ts`
export interface Product {
  _id: string;  // Agregar _id aquí, ya que es el identificador real
  id: string;  // Si deseas mantener la propiedad `id` para otros usos
  title: string;
  slug: string;
  price: number;
  description: string;
  category: Category;
  images: string[];
  stock: number;
}



export interface ProductsResponse { 
  products: Product[];
  total: number;
  page: number;
  limit: number;
} 