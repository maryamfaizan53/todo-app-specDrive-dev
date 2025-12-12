/**
 * Home/Landing page
 */
'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { isAuthenticated } from '../lib/auth';
import Link from 'next/link';

export default function HomePage() {
  const router = useRouter();

  useEffect(() => {
    if (isAuthenticated()) {
      router.push('/todos');
    }
  }, [router]);

  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="max-w-2xl mx-auto text-center px-4 py-16">
        <h1 className="text-5xl font-bold text-gray-900 mb-4">
          Welcome to Todo App!
        </h1>
        <p className="text-xl text-gray-600 mb-8">
          Get things done with our simple and powerful task management app.
        </p>
        <div className="flex gap-4 justify-center">
          <Link
            href="/login"
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-lg font-semibold transition"
          >
            Get Started
          </Link>
        </div>
      </div>
    </div>
  );
}
