/**
 * Navigation bar component
 */
'use client';

import { logout } from '@/lib/auth';

export default function Navbar({ user }) {
  if (!user) return null;

  const handleLogout = () => {
    logout();
  };

  return (
    <nav className="bg-blue-600 text-white shadow-lg">
      <div className="container mx-auto px-4 py-3 flex justify-between items-center">
        <h1 className="text-2xl font-bold">Todo App</h1>
        <div className="flex items-center gap-4">
          <span className="text-sm hidden sm:inline">{user.email}</span>
          <button
            onClick={handleLogout}
            className="bg-white text-blue-600 px-4 py-2 rounded hover:bg-blue-50 transition font-semibold"
          >
            Logout
          </button>
        </div>
      </div>
    </nav>
  );
}
