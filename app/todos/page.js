/**
 * Todo list page (main page)
 */
'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { getUser, isAuthenticated } from '../../lib/auth';
import { tasksAPI } from '../../lib/api';
import Navbar from '../../components/Navbar';
import TodoList from '../../components/TodoList';
import TodoFilters from '../../components/TodoFilters';
import Link from 'next/link';

export default function TodosPage() {
  const router = useRouter();
  const [user, setUser] = useState(null);
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({
    completed: 'all',
    search: '',
    sort: 'created_at',
    order: 'desc'
  });

  useEffect(() => {
    if (!isAuthenticated()) {
      router.push('/login');
      return;
    }

    const currentUser = getUser();
    setUser(currentUser);
  }, [router]);

  useEffect(() => {
    if (user) {
      fetchTasks();
    }
  }, [user, filters]);

  const fetchTasks = async () => {
    setLoading(true);
    try {
      const data = await tasksAPI.list(user.id, filters);
      setTasks(data);
    } catch (error) {
      console.error('Failed to fetch tasks:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleToggleComplete = async (taskId, completed) => {
    try {
      await tasksAPI.toggleComplete(user.id, taskId, completed);
      fetchTasks();
    } catch (error) {
      console.error('Failed to toggle completion:', error);
      alert('Failed to update task');
    }
  };

  const handleDelete = async (taskId) => {
    try {
      await tasksAPI.delete(user.id, taskId);
      fetchTasks();
    } catch (error) {
      console.error('Failed to delete task:', error);
      alert('Failed to delete task');
    }
  };

  const handleEdit = (taskId) => {
    router.push(`/todos/${taskId}`);
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
        <div className="max-w-4xl mx-auto">
          <div className="flex justify-between items-center mb-6">
            <h1 className="text-3xl font-bold text-gray-900">My Tasks</h1>
            <Link
              href="/todos/new"
              className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 font-semibold transition"
            >
              + New Task
            </Link>
          </div>

          <div className="mb-6">
            <TodoFilters filters={filters} onFilterChange={setFilters} />
          </div>

          <TodoList
            tasks={tasks}
            onToggleComplete={handleToggleComplete}
            onDelete={handleDelete}
            onEdit={handleEdit}
            loading={loading}
          />
        </div>
      </main>
    </div>
  );
}
