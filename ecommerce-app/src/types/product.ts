export interface Category {
  id: number;
  name: string;
  image: string;
  slug: string;
}

export interface Product {
  id: string;
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