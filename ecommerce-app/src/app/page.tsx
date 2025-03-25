'use client';

import Link from 'next/link';

export default function Home() {
  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative h-[600px] bg-gradient-to-r from-purple-700 to-blue-700">
        <div className="absolute inset-0 bg-black/30" />
        <div className="relative container mx-auto px-6 h-full flex items-center">
          <div className="text-white max-w-2xl">
            <h1 className="text-5xl font-bold mb-6 text-white">Discover Your Style</h1>
            <p className="text-xl mb-8 text-gray-100">Shop the latest trends in fashion, electronics, and more with exclusive deals.</p>
            <Link 
              href="/products" 
              className="inline-block bg-white text-purple-700 px-8 py-3 rounded-full font-semibold hover:bg-gray-100 transition"
            >
              Shop Now
            </Link>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-100 py-12">
        <div className="container mx-auto px-6">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
              <h3 className="font-bold mb-4 text-gray-900">About Us</h3>
              <ul className="space-y-2 text-gray-700">
                <li>Our Story</li>
                <li>Careers</li>
                <li>Press</li>
              </ul>
            </div>
            <div>
              <h3 className="font-bold mb-4 text-gray-900">Customer Service</h3>
              <ul className="space-y-2 text-gray-700">
                <li>Contact Us</li>
                <li>Shipping Info</li>
                <li>Returns</li>
              </ul>
            </div>
            <div>
              <h3 className="font-bold mb-4 text-gray-900">Quick Links</h3>
              <ul className="space-y-2 text-gray-700">
                <li>FAQs</li>
                <li>Size Guide</li>
                <li>Track Order</li>
              </ul>
            </div>
            <div>
              <h3 className="font-bold mb-4 text-gray-900">Follow Us</h3>
              <ul className="space-y-2 text-gray-700">
                <li>Instagram</li>
                <li>Facebook</li>
                <li>Twitter</li>
              </ul>
            </div>
          </div>
          <div className="border-t border-gray-200 mt-12 pt-8 text-center text-gray-700">
            <p>&copy; 2025 Your E-commerce. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
