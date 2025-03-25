# E-Commerce Application

A modern e-commerce application built with Next.js, TypeScript, and Tailwind CSS. This project demonstrates a clean architecture approach to building a scalable e-commerce platform.

## 🚀 Quick Start

### Prerequisites

- Node.js (v18 or higher)
- npm or yarn
- Git

### Installation

1. Clone the repository:
```bash
git clone <your-repository-url>
cd ecommerce-app
```

2. Install dependencies:
```bash
npm install
# or
yarn install
```

3. Create a `.env.local` file in the root directory:
```env
NEXT_PUBLIC_API_URL=https://api.escuelajs.co/api/v1
```

4. Start the development server:
```bash
npm run dev
# or
yarn dev
```

The application will be available at `http://localhost:3000`

## 🏗️ Project Structure

```
src/
├── app/                    # Next.js app directory
│   ├── products/          # Product-related pages
│   │   ├── [slug]/       # Product detail page
│   │   └── page.tsx      # Products listing page
│   ├── layout.tsx        # Root layout
│   └── page.tsx          # Home page
├── components/            # Reusable UI components
│   ├── Layout/           # Layout components
│   │   └── Navbar.tsx    # Navigation component
│   └── ProductCard.tsx   # Product card component
├── hooks/                # Custom React hooks
│   └── useProducts.ts    # Products data fetching hook
├── services/             # API services
│   └── productService.ts # Product-related API calls
├── types/                # TypeScript type definitions
│   └── product.ts        # Product-related types
├── utils/                # Utility functions
├── constants/            # Constants and configuration
└── styles/              # Global styles
```

## 🔌 API Structure

The application uses the Platzi Fake Store API. Here are the main endpoints:

### Products Endpoint
```typescript
GET /products
Response:
{
  id: number;
  title: string;
  price: number;
  description: string;
  category: {
    id: number;
    name: string;
    image: string;
    slug: string;
  };
  images: string[];
}
```

### API Integration
- `productService.ts` handles all API calls
- Pagination is implemented with offset/limit parameters
- Images are served from various domains (configured in next.config.ts)

## 🎯 Features

### Home Page
- Hero section with featured products
- Category showcase
- Newsletter subscription
- Responsive design

### Products Page
- Product grid layout
- Pagination
- Loading states
- Error handling

### Product Detail Page
- Image gallery with thumbnails
- Product information
- Add to cart functionality
- Category labeling

## 🛠️ Technical Details

### Built With
- Next.js 14
- TypeScript
- Tailwind CSS
- React Hooks

### Key Components

#### ProductCard
```typescript
interface ProductCardProps {
  product: Product;
}
```
Displays individual product information in a grid layout.

#### useProducts Hook
```typescript
const useProducts = (initialPage: number = 1, initialLimit: number = 12) => {
  // Returns: { products, loading, error, page, total, setPage }
}
```
Manages product fetching and pagination state.

### Styling
- Utilizes Tailwind CSS for responsive design
- Custom color scheme:
  - Primary: Purple (600-800)
  - Text: Gray (700-900)
  - Backgrounds: White, Gray (50-100)

## 🔒 Environment Variables

Required environment variables:
```env
NEXT_PUBLIC_API_URL=https://api.escuelajs.co/api/v1
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
