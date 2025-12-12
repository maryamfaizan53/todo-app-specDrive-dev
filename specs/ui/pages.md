# UI Pages Specification

## Overview

All pages use Next.js 14+ App Router with JavaScript (no TypeScript). Pages are located in the `frontend/app` directory using file-based routing.

## Routing Structure

```
frontend/app/
  layout.js           # Root layout with Navbar
  page.js             # Home/landing page (/)
  login/
    page.js           # Login page (/login) - Better Auth
  signup/
    page.js           # Sign up page (/signup) - Better Auth
  todos/
    page.js           # Task list (/todos)
    new/
      page.js         # Create task (/todos/new)
    [id]/
      page.js         # Edit task (/todos/[id])
```

---

## Page: Root Layout

### Location
`frontend/app/layout.js`

### Purpose
Root layout component that wraps all pages with common elements.

### Features
- Include Better Auth provider
- Include Navbar (if user logged in)
- Set up global styles
- Configure metadata

### Implementation
```javascript
import './globals.css'
import { AuthProvider } from '@/lib/auth' // Better Auth provider
import Navbar from '@/components/Navbar'

export const metadata = {
  title: 'Todo App - Phase II',
  description: 'Full-stack todo application with Next.js and FastAPI',
}

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="bg-gray-50 min-h-screen">
        <AuthProvider>
          <Navbar />
          <main className="container mx-auto px-4 py-8">
            {children}
          </main>
        </AuthProvider>
      </body>
    </html>
  )
}
```

---

## Page: Home/Landing

### Location
`frontend/app/page.js`

### Route
`/`

### Purpose
Landing page that redirects to todos if logged in, or shows welcome message with login/signup links.

### Features
- Check authentication status
- Redirect to `/todos` if logged in
- Show welcome message if not logged in
- Links to login and sign up

### Layout
```
┌──────────────────────────────────────┐
│  Todo App                            │
├──────────────────────────────────────┤
│                                      │
│  Welcome to Todo App!                │
│                                      │
│  Get things done with our simple     │
│  and powerful task management app.   │
│                                      │
│  [Get Started]  [Login]              │
│                                      │
└──────────────────────────────────────┘
```

### Implementation
```javascript
'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/lib/auth'
import Link from 'next/link'

export default function HomePage() {
  const { user, loading } = useAuth()
  const router = useRouter()

  useEffect(() => {
    if (!loading && user) {
      router.push('/todos')
    }
  }, [user, loading, router])

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  if (user) {
    return null // Redirecting...
  }

  return (
    <div className="max-w-2xl mx-auto text-center py-16">
      <h1 className="text-5xl font-bold text-gray-900 mb-4">
        Welcome to Todo App!
      </h1>
      <p className="text-xl text-gray-600 mb-8">
        Get things done with our simple and powerful task management app.
      </p>
      <div className="flex gap-4 justify-center">
        <Link
          href="/signup"
          className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-lg font-semibold"
        >
          Get Started
        </Link>
        <Link
          href="/login"
          className="px-6 py-3 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 text-lg font-semibold"
        >
          Login
        </Link>
      </div>
    </div>
  )
}
```

---

## Page: Login

### Location
`frontend/app/login/page.js`

### Route
`/login`

### Purpose
User login form managed by Better Auth.

### Features
- Email and password inputs
- Remember me checkbox (optional)
- Login button
- Link to sign up page
- Error messages for invalid credentials

### Layout
```
┌──────────────────────────────────────┐
│  Login                               │
├──────────────────────────────────────┤
│  Email                               │
│  ┌────────────────────────────────┐ │
│  │ user@example.com               │ │
│  └────────────────────────────────┘ │
│                                      │
│  Password                            │
│  ┌────────────────────────────────┐ │
│  │ ••••••••                       │ │
│  └────────────────────────────────┘ │
│                                      │
│  [Login]                             │
│                                      │
│  Don't have an account? Sign up      │
└──────────────────────────────────────┘
```

### Implementation
```javascript
'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/lib/auth'
import Link from 'next/link'

export default function LoginPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const { login } = useAuth()
  const router = useRouter()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      await login(email, password)
      router.push('/todos')
    } catch (err) {
      setError(err.message || 'Invalid email or password')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-md mx-auto py-16">
      <div className="bg-white rounded-lg shadow-lg p-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-6 text-center">
          Login
        </h1>

        {error && (
          <div className="bg-red-50 border border-red-200 rounded p-3 mb-4 text-red-700 text-sm">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
              Email
            </label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>

          <div>
            <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">
              Password
            </label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-3 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50 font-semibold"
          >
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>

        <p className="text-center text-sm text-gray-600 mt-6">
          Don't have an account?{' '}
          <Link href="/signup" className="text-blue-600 hover:text-blue-800 font-semibold">
            Sign up
          </Link>
        </p>
      </div>
    </div>
  )
}
```

---

## Page: Sign Up

### Location
`frontend/app/signup/page.js`

### Route
`/signup`

### Purpose
New user registration form managed by Better Auth.

### Features
- Name input (optional)
- Email and password inputs
- Password confirmation
- Sign up button
- Link to login page
- Validation error messages

### Layout
```
┌──────────────────────────────────────┐
│  Sign Up                             │
├──────────────────────────────────────┤
│  Name (optional)                     │
│  ┌────────────────────────────────┐ │
│  │ John Doe                       │ │
│  └────────────────────────────────┘ │
│                                      │
│  Email                               │
│  ┌────────────────────────────────┐ │
│  │ user@example.com               │ │
│  └────────────────────────────────┘ │
│                                      │
│  Password                            │
│  ┌────────────────────────────────┐ │
│  │ ••••••••                       │ │
│  └────────────────────────────────┘ │
│                                      │
│  [Sign Up]                           │
│                                      │
│  Already have an account? Login      │
└──────────────────────────────────────┘
```

### Implementation
Similar to Login page but with sign up logic.

---

## Page: Task List

### Location
`frontend/app/todos/page.js`

### Route
`/todos`

### Purpose
Main page showing all user's tasks with filters and search.

### Features
- Protected route (require authentication)
- TodoFilters component
- TodoList component with all tasks
- Create New Task button
- Loading state
- Empty state

### Layout
```
┌──────────────────────────────────────────────────┐
│  Navbar                                          │
├──────────────────────────────────────────────────┤
│  My Tasks                         [+ New Task]   │
├──────────────────────────────────────────────────┤
│  [TodoFilters]                                   │
├──────────────────────────────────────────────────┤
│  [TodoList]                                      │
│  - Task 1                                        │
│  - Task 2                                        │
│  - Task 3                                        │
└──────────────────────────────────────────────────┘
```

### Implementation
```javascript
'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/lib/auth'
import { apiRequest } from '@/lib/api'
import TodoList from '@/components/TodoList'
import TodoFilters from '@/components/TodoFilters'
import Link from 'next/link'

export default function TodosPage() {
  const { user, loading: authLoading } = useAuth()
  const router = useRouter()
  const [tasks, setTasks] = useState([])
  const [loading, setLoading] = useState(true)
  const [filters, setFilters] = useState({
    completed: 'all',
    search: '',
    sort: 'created_at',
    order: 'desc'
  })

  useEffect(() => {
    if (!authLoading && !user) {
      router.push('/login')
    }
  }, [user, authLoading, router])

  useEffect(() => {
    if (user) {
      fetchTasks()
    }
  }, [user, filters])

  const fetchTasks = async () => {
    setLoading(true)
    try {
      const params = new URLSearchParams()
      if (filters.completed !== 'all') {
        params.append('completed', filters.completed)
      }
      if (filters.search) {
        params.append('search', filters.search)
      }
      params.append('sort', filters.sort)
      params.append('order', filters.order)

      const data = await apiRequest(`/api/${user.id}/tasks?${params}`)
      setTasks(data)
    } catch (error) {
      console.error('Failed to fetch tasks:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleToggleComplete = async (taskId, completed) => {
    try {
      await apiRequest(`/api/${user.id}/tasks/${taskId}/complete`, {
        method: 'PATCH',
        body: JSON.stringify({ completed })
      })
      fetchTasks()
    } catch (error) {
      console.error('Failed to toggle completion:', error)
    }
  }

  const handleDelete = async (taskId) => {
    try {
      await apiRequest(`/api/${user.id}/tasks/${taskId}`, {
        method: 'DELETE'
      })
      fetchTasks()
    } catch (error) {
      console.error('Failed to delete task:', error)
    }
  }

  const handleEdit = (taskId) => {
    router.push(`/todos/${taskId}`)
  }

  if (authLoading) {
    return <div>Loading...</div>
  }

  if (!user) {
    return null // Redirecting...
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-900">My Tasks</h1>
        <Link
          href="/todos/new"
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 font-semibold"
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
  )
}
```

---

## Page: Create Task

### Location
`frontend/app/todos/new/page.js`

### Route
`/todos/new`

### Purpose
Form to create a new task.

### Features
- Protected route (require authentication)
- TodoForm component
- Submit creates task and redirects to list
- Cancel returns to list

### Layout
```
┌──────────────────────────────────────┐
│  Navbar                              │
├──────────────────────────────────────┤
│  Create New Task                     │
├──────────────────────────────────────┤
│  [TodoForm]                          │
│  Title: [_______________]            │
│  Description: [_________]            │
│  [Cancel] [Create]                   │
└──────────────────────────────────────┘
```

### Implementation
```javascript
'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/lib/auth'
import { apiRequest } from '@/lib/api'
import TodoForm from '@/components/TodoForm'

export default function NewTaskPage() {
  const { user, loading: authLoading } = useAuth()
  const router = useRouter()
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    if (!authLoading && !user) {
      router.push('/login')
    }
  }, [user, authLoading, router])

  const handleSubmit = async (data) => {
    setLoading(true)
    try {
      await apiRequest(`/api/${user.id}/tasks`, {
        method: 'POST',
        body: JSON.stringify(data)
      })
      router.push('/todos')
    } catch (error) {
      console.error('Failed to create task:', error)
      alert('Failed to create task. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const handleCancel = () => {
    router.push('/todos')
  }

  if (authLoading || !user) {
    return <div>Loading...</div>
  }

  return (
    <div className="max-w-2xl mx-auto">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">Create New Task</h1>
      <TodoForm
        onSubmit={handleSubmit}
        onCancel={handleCancel}
        loading={loading}
      />
    </div>
  )
}
```

---

## Page: Edit Task

### Location
`frontend/app/todos/[id]/page.js`

### Route
`/todos/[id]`

### Purpose
Form to edit an existing task.

### Features
- Protected route (require authentication)
- Fetch task data on load
- TodoForm component pre-filled with task data
- Submit updates task and redirects to list
- Cancel returns to list
- 404 handling if task not found

### Layout
```
┌──────────────────────────────────────┐
│  Navbar                              │
├──────────────────────────────────────┤
│  Edit Task                           │
├──────────────────────────────────────┤
│  [TodoForm with existing data]       │
│  Title: [Buy groceries____]          │
│  Description: [Milk, eggs..]         │
│  [Cancel] [Update]                   │
└──────────────────────────────────────┘
```

### Implementation
```javascript
'use client'

import { useState, useEffect } from 'react'
import { useRouter, useParams } from 'next/navigation'
import { useAuth } from '@/lib/auth'
import { apiRequest } from '@/lib/api'
import TodoForm from '@/components/TodoForm'

export default function EditTaskPage() {
  const { user, loading: authLoading } = useAuth()
  const router = useRouter()
  const params = useParams()
  const taskId = params.id

  const [task, setTask] = useState(null)
  const [loading, setLoading] = useState(true)
  const [submitting, setSubmitting] = useState(false)

  useEffect(() => {
    if (!authLoading && !user) {
      router.push('/login')
    }
  }, [user, authLoading, router])

  useEffect(() => {
    if (user && taskId) {
      fetchTask()
    }
  }, [user, taskId])

  const fetchTask = async () => {
    setLoading(true)
    try {
      const data = await apiRequest(`/api/${user.id}/tasks/${taskId}`)
      setTask(data)
    } catch (error) {
      console.error('Failed to fetch task:', error)
      alert('Task not found')
      router.push('/todos')
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (data) => {
    setSubmitting(true)
    try {
      await apiRequest(`/api/${user.id}/tasks/${taskId}`, {
        method: 'PUT',
        body: JSON.stringify(data)
      })
      router.push('/todos')
    } catch (error) {
      console.error('Failed to update task:', error)
      alert('Failed to update task. Please try again.')
    } finally {
      setSubmitting(false)
    }
  }

  const handleCancel = () => {
    router.push('/todos')
  }

  if (authLoading || loading) {
    return <div>Loading...</div>
  }

  if (!user || !task) {
    return null // Redirecting...
  }

  return (
    <div className="max-w-2xl mx-auto">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">Edit Task</h1>
      <TodoForm
        task={task}
        onSubmit={handleSubmit}
        onCancel={handleCancel}
        loading={submitting}
      />
    </div>
  )
}
```

---

## Protected Routes

All pages except `/`, `/login`, and `/signup` require authentication.

### Implementation Pattern
```javascript
useEffect(() => {
  if (!authLoading && !user) {
    router.push('/login')
  }
}, [user, authLoading, router])
```

### Alternative: Middleware
Create `middleware.js` in `frontend/`:
```javascript
import { NextResponse } from 'next/server'

export function middleware(request) {
  const token = request.cookies.get('auth-token')

  if (!token && !request.nextUrl.pathname.startsWith('/login') && !request.nextUrl.pathname.startsWith('/signup') && request.nextUrl.pathname !== '/') {
    return NextResponse.redirect(new URL('/login', request.url))
  }

  return NextResponse.next()
}

export const config = {
  matcher: ['/todos/:path*']
}
```

---

## Error Pages

### 404 Not Found
`frontend/app/not-found.js`

```javascript
import Link from 'next/link'

export default function NotFound() {
  return (
    <div className="max-w-2xl mx-auto text-center py-16">
      <h1 className="text-6xl font-bold text-gray-900 mb-4">404</h1>
      <p className="text-xl text-gray-600 mb-8">Page not found</p>
      <Link
        href="/todos"
        className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
      >
        Go to Tasks
      </Link>
    </div>
  )
}
```

---

## Loading States

### Page-Level Loading
Use `loading.js` files in each route directory:

`frontend/app/todos/loading.js`:
```javascript
export default function Loading() {
  return (
    <div className="flex justify-center items-center min-h-[60vh]">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
    </div>
  )
}
```

---

## Navigation Flow

```
Home (/)
  ├─→ Sign Up (/signup) → Todos (/todos)
  └─→ Login (/login) → Todos (/todos)

Todos (/todos)
  ├─→ New Task (/todos/new) → Todos (/todos)
  ├─→ Edit Task (/todos/[id]) → Todos (/todos)
  └─→ Logout → Home (/)
```

---

## SEO and Metadata

Each page should include metadata:

```javascript
export const metadata = {
  title: 'Tasks - Todo App',
  description: 'Manage your tasks efficiently',
}
```

---

## Success Criteria

Pages are complete when:
- [ ] All routes render correctly
- [ ] Authentication protection works
- [ ] Forms submit successfully
- [ ] Navigation flows logically
- [ ] Loading states display properly
- [ ] Error handling works
- [ ] Responsive on all devices
- [ ] Accessible via keyboard
- [ ] SEO metadata present
