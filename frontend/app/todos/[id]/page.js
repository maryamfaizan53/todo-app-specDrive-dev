/**
 * Edit task page
 */
"use client";

import { useState, useEffect } from "react";
import { useRouter, useParams } from "next/navigation";
import { getUser, isAuthenticated } from "../../../../.specify/lib/auth.js";
import { tasksAPI } from "../../../.specify/lib/api.js";
import Navbar from "../../../components/Navbar";
import TodoForm from "../../../components/TodoForm";

export default function EditTaskPage() {
  const router = useRouter();
  const params = useParams();
  const taskId = params.id;

  const [user, setUser] = useState(null);
  const [task, setTask] = useState(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    if (!isAuthenticated()) {
      router.push("/login");
      return;
    }

    const currentUser = getUser();
    setUser(currentUser);
  }, [router]);

  useEffect(() => {
    if (user && taskId) {
      fetchTask();
    }
  }, [user, taskId]);

  const fetchTask = async () => {
    setLoading(true);
    try {
      const data = await tasksAPI.get(user.id, taskId);
      setTask(data);
    } catch (error) {
      console.error("Failed to fetch task:", error);
      alert("Task not found");
      router.push("/todos");
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (data) => {
    setSubmitting(true);
    try {
      await tasksAPI.update(user.id, taskId, data);
      router.push("/todos");
    } catch (error) {
      console.error("Failed to update task:", error);
      throw error;
    } finally {
      setSubmitting(false);
    }
  };

  const handleCancel = () => {
    router.push("/todos");
  };

  if (!user || loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (!task) {
    return null;
  }

  return (
    <div className="min-h-screen">
      <Navbar user={user} />

      <main className="container mx-auto px-4 py-8">
        <div className="max-w-2xl mx-auto">
          <h1 className="text-3xl font-bold text-gray-900 mb-6">Edit Task</h1>
          <TodoForm
            task={task}
            onSubmit={handleSubmit}
            onCancel={handleCancel}
            loading={submitting}
          />
        </div>
      </main>
    </div>
  );
}
