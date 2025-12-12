# UI Components Specification

## Overview

All components use:
- **Framework**: Next.js 14+ with JavaScript (no TypeScript)
- **Styling**: Tailwind CSS utility classes
- **State Management**: React hooks (useState, useEffect)
- **API**: Custom API client from `lib/api.js`

## Design Principles

1. **Mobile-First**: Design for mobile, enhance for desktop
2. **Accessibility**: Use semantic HTML and ARIA labels
3. **Responsive**: Adapt to all screen sizes
4. **Loading States**: Show feedback for async operations
5. **Error Handling**: Display user-friendly error messages

---

## Component: Navbar

### Purpose
Top navigation bar with app branding, user info, and logout button.

### Location
`frontend/components/Navbar.js`

### Props
```javascript
{
  user: {
    id: string,
    email: string,
    name: string?
  }
}
```

### UI Elements
- App logo/title (left side)
- User email or name (right side)
- Logout button (right side)
- Mobile: Hamburger menu

### Layout
```
┌─────────────────────────────────────────────────┐
│  Todo App            user@email.com   [Logout]  │
└─────────────────────────────────────────────────┘
```

### Tailwind Classes
```javascript
<nav className="bg-blue-600 text-white shadow-lg">
  <div className="container mx-auto px-4 py-3 flex justify-between items-center">
    <h1 className="text-2xl font-bold">Todo App</h1>
    <div className="flex items-center gap-4">
      <span className="text-sm">{user.email}</span>
      <button className="bg-white text-blue-600 px-4 py-2 rounded hover:bg-blue-50">
        Logout
      </button>
    </div>
  </div>
</nav>
```

### Behavior
- Click "Logout": Call Better Auth logout, redirect to login page
- Always visible at top of page
- Sticky position on scroll (optional)

---

## Component: TodoList

### Purpose
Display list of tasks with filters applied.

### Location
`frontend/components/TodoList.js`

### Props
```javascript
{
  tasks: Array<Task>,
  onToggleComplete: (taskId: string, completed: boolean) => Promise<void>,
  onDelete: (taskId: string) => Promise<void>,
  onEdit: (taskId: string) => void,
  loading: boolean
}
```

### UI Elements
- Empty state message if no tasks
- Loading spinner while fetching
- List of TodoItem components
- Responsive grid or list layout

### Layout
```
┌──────────────────────────────┐
│  □ Task 1 Title              │
│    Description preview...     │
│    [Edit] [Delete]           │
├──────────────────────────────┤
│  ✓ Task 2 Title (completed)  │
│    Description preview...     │
│    [Edit] [Delete]           │
├──────────────────────────────┤
│  ... more tasks              │
└──────────────────────────────┘
```

### Tailwind Classes
```javascript
<div className="space-y-4">
  {loading && (
    <div className="text-center py-8">
      <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
    </div>
  )}

  {!loading && tasks.length === 0 && (
    <div className="text-center py-12 text-gray-500">
      <p className="text-lg">No tasks yet!</p>
      <p className="text-sm">Create your first task to get started.</p>
    </div>
  )}

  {!loading && tasks.map(task => (
    <TodoItem
      key={task.id}
      task={task}
      onToggleComplete={onToggleComplete}
      onDelete={onDelete}
      onEdit={onEdit}
    />
  ))}
</div>
```

### Behavior
- Render each task as TodoItem
- Pass callbacks down to TodoItem
- Show loading state while fetching
- Show empty state when no tasks

---

## Component: TodoItem

### Purpose
Display single task with actions (complete, edit, delete).

### Location
`frontend/components/TodoItem.js`

### Props
```javascript
{
  task: {
    id: string,
    title: string,
    description: string?,
    completed: boolean,
    created_at: string,
    updated_at: string
  },
  onToggleComplete: (taskId: string, completed: boolean) => Promise<void>,
  onDelete: (taskId: string) => Promise<void>,
  onEdit: (taskId: string) => void
}
```

### UI Elements
- Checkbox for completion toggle
- Task title (strike-through if completed)
- Task description (truncated if long)
- Edit button
- Delete button
- Timestamps (created/updated)

### Layout
```
┌─────────────────────────────────────────────────┐
│ □  Buy groceries                                 │
│    Milk, eggs, bread                             │
│    Created: Dec 12, 10:30 AM                     │
│    [Edit] [Delete]                               │
└─────────────────────────────────────────────────┘
```

### Tailwind Classes
```javascript
<div className="bg-white border rounded-lg p-4 shadow hover:shadow-md transition">
  <div className="flex items-start gap-3">
    <input
      type="checkbox"
      checked={task.completed}
      onChange={(e) => onToggleComplete(task.id, e.target.checked)}
      className="mt-1 h-5 w-5 text-blue-600 rounded focus:ring-2 focus:ring-blue-500"
    />
    <div className="flex-1">
      <h3 className={`text-lg font-semibold ${task.completed ? 'line-through text-gray-500' : 'text-gray-900'}`}>
        {task.title}
      </h3>
      {task.description && (
        <p className="text-sm text-gray-600 mt-1">{task.description}</p>
      )}
      <p className="text-xs text-gray-400 mt-2">
        Created: {new Date(task.created_at).toLocaleString()}
      </p>
    </div>
  </div>
  <div className="flex gap-2 mt-3">
    <button
      onClick={() => onEdit(task.id)}
      className="px-3 py-1 text-sm bg-blue-100 text-blue-700 rounded hover:bg-blue-200"
    >
      Edit
    </button>
    <button
      onClick={() => {
        if (confirm('Delete this task?')) {
          onDelete(task.id);
        }
      }}
      className="px-3 py-1 text-sm bg-red-100 text-red-700 rounded hover:bg-red-200"
    >
      Delete
    </button>
  </div>
</div>
```

### Behavior
- Click checkbox: Toggle completion via API
- Click "Edit": Navigate to edit page
- Click "Delete": Confirm, then delete via API
- Show loading state during operations

---

## Component: TodoForm

### Purpose
Form for creating or editing a task.

### Location
`frontend/components/TodoForm.js`

### Props
```javascript
{
  task?: {
    id: string,
    title: string,
    description: string?
  },
  onSubmit: (data: { title: string, description: string? }) => Promise<void>,
  onCancel: () => void,
  loading: boolean
}
```

### UI Elements
- Title input field (required)
- Description textarea (optional)
- Submit button
- Cancel button
- Validation error messages

### Layout
```
┌─────────────────────────────────────┐
│  Title *                             │
│  ┌───────────────────────────────┐  │
│  │ Buy groceries                 │  │
│  └───────────────────────────────┘  │
│                                      │
│  Description                         │
│  ┌───────────────────────────────┐  │
│  │ Milk, eggs, bread             │  │
│  │                               │  │
│  └───────────────────────────────┘  │
│                                      │
│  [Cancel]    [Save Task]            │
└─────────────────────────────────────┘
```

### Tailwind Classes
```javascript
<form onSubmit={handleSubmit} className="bg-white rounded-lg shadow p-6 space-y-4">
  <div>
    <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-1">
      Title <span className="text-red-500">*</span>
    </label>
    <input
      id="title"
      type="text"
      value={title}
      onChange={(e) => setTitle(e.target.value)}
      className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
      required
    />
    {error && <p className="text-red-500 text-sm mt-1">{error}</p>}
  </div>

  <div>
    <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
      Description
    </label>
    <textarea
      id="description"
      value={description}
      onChange={(e) => setDescription(e.target.value)}
      rows={4}
      className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
    />
  </div>

  <div className="flex gap-3">
    <button
      type="button"
      onClick={onCancel}
      className="px-4 py-2 bg-gray-200 text-gray-700 rounded hover:bg-gray-300"
    >
      Cancel
    </button>
    <button
      type="submit"
      disabled={loading}
      className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
    >
      {loading ? 'Saving...' : 'Save Task'}
    </button>
  </div>
</form>
```

### Behavior
- Validate title is not empty
- Submit: Call onSubmit with form data
- Cancel: Call onCancel (navigate back)
- Disable submit while loading
- Pre-fill fields if editing existing task

---

## Component: TodoFilters

### Purpose
Filter and search controls for task list.

### Location
`frontend/components/TodoFilters.js`

### Props
```javascript
{
  filters: {
    completed: 'all' | 'true' | 'false',
    search: string,
    sort: 'created_at' | 'updated_at' | 'title',
    order: 'asc' | 'desc'
  },
  onFilterChange: (filters: object) => void
}
```

### UI Elements
- Search input
- Completion filter (All / Active / Completed)
- Sort dropdown
- Clear filters button

### Layout
```
┌──────────────────────────────────────────────────┐
│  ┌────────────────────┐  [All] [Active] [Done]   │
│  │ 🔍 Search tasks... │  Sort: [Created ▼]       │
│  └────────────────────┘  [Clear Filters]         │
└──────────────────────────────────────────────────┘
```

### Tailwind Classes
```javascript
<div className="bg-white rounded-lg shadow p-4 space-y-3">
  <div className="flex flex-col md:flex-row gap-3">
    <input
      type="text"
      placeholder="Search tasks..."
      value={filters.search}
      onChange={(e) => onFilterChange({ ...filters, search: e.target.value })}
      className="flex-1 px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
    />

    <div className="flex gap-2">
      <button
        onClick={() => onFilterChange({ ...filters, completed: 'all' })}
        className={`px-3 py-2 rounded ${
          filters.completed === 'all'
            ? 'bg-blue-600 text-white'
            : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
        }`}
      >
        All
      </button>
      <button
        onClick={() => onFilterChange({ ...filters, completed: 'false' })}
        className={`px-3 py-2 rounded ${
          filters.completed === 'false'
            ? 'bg-blue-600 text-white'
            : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
        }`}
      >
        Active
      </button>
      <button
        onClick={() => onFilterChange({ ...filters, completed: 'true' })}
        className={`px-3 py-2 rounded ${
          filters.completed === 'true'
            ? 'bg-blue-600 text-white'
            : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
        }`}
      >
        Done
      </button>
    </div>
  </div>

  <div className="flex justify-between items-center">
    <select
      value={filters.sort}
      onChange={(e) => onFilterChange({ ...filters, sort: e.target.value })}
      className="px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
    >
      <option value="created_at">Created Date</option>
      <option value="updated_at">Updated Date</option>
      <option value="title">Title</option>
    </select>

    <button
      onClick={() => onFilterChange({
        completed: 'all',
        search: '',
        sort: 'created_at',
        order: 'desc'
      })}
      className="px-3 py-2 text-sm text-blue-600 hover:text-blue-800"
    >
      Clear Filters
    </button>
  </div>
</div>
```

### Behavior
- Update filters on change
- Debounce search input (300ms)
- Persist filters in URL query params (optional)
- Clear all filters resets to defaults

---

## Responsive Design Guidelines

### Breakpoints (Tailwind)
- **sm**: 640px (mobile landscape)
- **md**: 768px (tablet)
- **lg**: 1024px (desktop)
- **xl**: 1280px (large desktop)

### Mobile (<640px)
- Single column layout
- Full-width buttons
- Stacked form fields
- Hidden secondary info

### Tablet (640-1024px)
- Two column layout where appropriate
- Side-by-side form fields
- Visible secondary info

### Desktop (>1024px)
- Multi-column layout
- Sidebar navigation (optional)
- Rich hover states

---

## Accessibility Guidelines

1. **Semantic HTML**: Use proper elements (`<button>`, `<input>`, `<nav>`)
2. **ARIA Labels**: Add `aria-label` for icon buttons
3. **Keyboard Navigation**: Ensure all interactive elements are focusable
4. **Focus Indicators**: Use Tailwind's `focus:ring` classes
5. **Color Contrast**: Ensure text meets WCAG AA standards
6. **Screen Readers**: Test with screen readers

---

## Error States

### Network Error
```javascript
<div className="bg-red-50 border border-red-200 rounded p-4 text-red-700">
  <p className="font-semibold">Connection Error</p>
  <p className="text-sm">Unable to reach the server. Please check your connection.</p>
</div>
```

### Validation Error
```javascript
<p className="text-red-500 text-sm mt-1">
  {error}
</p>
```

### 401/403 Error
- Redirect to login page (don't show error message)

---

## Loading States

### Button Loading
```javascript
<button disabled={loading} className="...">
  {loading ? (
    <>
      <span className="inline-block animate-spin mr-2">⟳</span>
      Loading...
    </>
  ) : (
    'Save'
  )}
</button>
```

### Page Loading
```javascript
<div className="flex justify-center items-center min-h-screen">
  <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
</div>
```

---

## Component File Structure

```
frontend/
  components/
    Navbar.js
    TodoList.js
    TodoItem.js
    TodoForm.js
    TodoFilters.js
```

Each component should:
- Export as default
- Use functional components with hooks
- Include propTypes for documentation (optional)
- Handle loading and error states
- Be reusable and composable
