/**
 * Create new task page
 */
"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { getUser, isAuthenticated } from "../../../lib/auth";
import { tasksAPI } from "../../../lib/api";
import Navbar from "../components/Navbar";
import TodoForm from "../components/TodoForm";

export default function NewTaskPage() {
  const router = useRouter();
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!isAuthenticated()) {
      router.push("/login");
      return;
    }

    const currentUser = getUser();
    setUser(currentUser);
  }, [router]);

  const handleSubmit = async (data) => {
    setLoading(true);
    try {
      await tasksAPI.create(user.id, data);
      router.push("/todos");
    } catch (error) {
      console.error("Failed to create task:", error);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = () => {
    router.push("/todos");
  };

  if (!user) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen">
      <Navbar user={user} />

      <main className="container mx-auto px-4 py-8">
        <div className="max-w-2xl mx-auto">
          <h1 className="text-3xl font-bold text-gray-900 mb-6">
            Create New Task
          </h1>
          <TodoForm
            onSubmit={handleSubmit}
            onCancel={handleCancel}
            loading={loading}
          />
        </div>
      </main>
    </div>
  );
}
