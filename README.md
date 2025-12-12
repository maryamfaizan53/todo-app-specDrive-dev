# Todo App Frontend

Next.js 14 frontend application for the Todo Full-Stack Web Application.

## Features

- **Next.js 14 App Router**: Modern React framework with server components
- **Tailwind CSS**: Utility-first CSS framework for rapid UI development
- **Responsive Design**: Mobile-first approach with responsive layouts
- **JWT Authentication**: Secure token-based authentication (simplified demo)
- **API Integration**: Complete integration with FastAPI backend

## Prerequisites

- Node.js 18+ and npm
- Backend API running on http://localhost:8000

## Installation

1. Navigate to frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create `.env.local` file:
   ```bash
   cp .env.local.example .env.local
   ```

4. Configure environment variables in `.env.local`:
   ```
   NEXT_PUBLIC_API_URL=http://localhost:8000
   BETTER_AUTH_SECRET=your-secret-key-minimum-32-characters-long
   ```

   **Important**: Use the same `BETTER_AUTH_SECRET` as the backend!

## Running the Application

### Development Mode

```bash
npm run dev
```

The application will be available at http://localhost:3000

### Production Build

```bash
npm run build
npm start
```

## Project Structure

```
frontend/
├── app/
│   ├── layout.js          # Root layout
│   ├── page.js            # Home page
│   ├── globals.css        # Global styles
│   ├── login/
│   │   └── page.js        # Login page
│   └── todos/
│       ├── page.js        # Todo list page
│       ├── new/
│       │   └── page.js    # Create task page
│       └── [id]/
│           └── page.js    # Edit task page
├── components/
│   ├── Navbar.js          # Navigation bar
│   ├── TodoList.js        # Task list component
│   ├── TodoItem.js        # Individual task component
│   ├── TodoForm.js        # Create/edit form
│   └── TodoFilters.js     # Filter controls
├── lib/
│   ├── auth.js            # Authentication utilities
│   └── api.js             # API client
├── package.json           # Dependencies
├── tailwind.config.js     # Tailwind configuration
└── next.config.js         # Next.js configuration
```

## Pages

### `/` - Home Page
Landing page with login button. Redirects to `/todos` if already authenticated.

### `/login` - Login Page
**Demo Mode**: Enter any email and password to create a demo session.

In production, this should integrate with Better Auth for real authentication.

### `/todos` - Todo List
Main application page showing all tasks with:
- Filters (All, Active, Done)
- Search functionality
- Sort options
- Create new task button

### `/todos/new` - Create Task
Form to create a new task with title and optional description.

### `/todos/[id]` - Edit Task
Form to edit an existing task.

## Authentication

### Current Implementation (Demo Mode)

The current auth system is a simplified demo that:
- Creates mock JWT tokens client-side
- Stores user data in localStorage
- Works with the backend JWT verification

### For Production

Replace `frontend/lib/auth.js` with Better Auth integration:

1. Install Better Auth:
   ```bash
   npm install better-auth
   ```

2. Set up Better Auth provider
3. Configure JWT issuing with backend secret
4. Update API client to use Better Auth tokens

See [Better Auth Documentation](https://better-auth.com) for details.

## API Integration

All API calls go through `lib/api.js` which:
- Attaches JWT token to requests
- Handles error responses (401, 403, 404, etc.)
- Redirects to login on authentication failure

### API Client Usage

```javascript
import { tasksAPI } from '../lib/api';

// List tasks
const tasks = await tasksAPI.list(userId, {
  completed: 'false',
  search: 'groceries',
  sort: 'created_at'
});

// Create task
const task = await tasksAPI.create(userId, {
  title: 'Buy milk',
  description: 'From the grocery store'
});

// Update task
await tasksAPI.update(userId, taskId, {
  title: 'Updated title',
  description: 'Updated description'
});

// Toggle completion
await tasksAPI.toggleComplete(userId, taskId, true);

// Delete task
await tasksAPI.delete(userId, taskId);
```

## Styling with Tailwind CSS

The application uses Tailwind CSS for styling. Key patterns:

### Responsive Design
```jsx
<div className="flex flex-col md:flex-row gap-4">
  {/* Mobile: column, Desktop: row */}
</div>
```

### Button Styles
```jsx
<button className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
  Click me
</button>
```

### Form Inputs
```jsx
<input className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500" />
```

## Error Handling

### Network Errors
Displayed with toast/alert messages to the user.

### Authentication Errors (401)
Automatically redirect to login page and clear stored auth.

### Permission Errors (403)
Show error message (user trying to access another user's data).

### Not Found (404)
Show error message and redirect to todo list.

## Development Guidelines

1. **Use Client Components**: All interactive components must use `'use client'` directive
2. **Check Authentication**: Verify user is authenticated before API calls
3. **Handle Loading States**: Show spinners/loading indicators for async operations
4. **Error Feedback**: Always provide user feedback for errors
5. **Mobile First**: Design for mobile, enhance for desktop

## Testing

### Manual Testing Checklist

- [ ] Login creates session and redirects to todos
- [ ] Create task adds to list
- [ ] Edit task updates correctly
- [ ] Delete task removes from list
- [ ] Toggle completion works
- [ ] Filters (All, Active, Done) work
- [ ] Search finds tasks
- [ ] Logout clears session
- [ ] Responsive on mobile and desktop
- [ ] Error messages display correctly

### Automated Testing (Future)

Consider adding:
- Jest for unit tests
- React Testing Library for component tests
- Playwright for E2E tests

## Troubleshooting

### "Failed to fetch" errors
- Ensure backend is running on http://localhost:8000
- Check CORS is configured correctly in backend
- Verify `NEXT_PUBLIC_API_URL` in `.env.local`

### Authentication errors
- Clear localStorage and try logging in again
- Verify `BETTER_AUTH_SECRET` matches backend
- Check browser console for JWT errors

### Styling issues
- Run `npm install` to ensure Tailwind is installed
- Check `tailwind.config.js` content paths
- Verify `globals.css` includes Tailwind directives

## Deployment

### Vercel (Recommended)

1. Push code to GitHub
2. Connect repository to Vercel
3. Set environment variables in Vercel dashboard
4. Deploy

### Other Platforms

Compatible with:
- Netlify
- AWS Amplify
- Railway
- Any Node.js hosting

**Important**: Update `NEXT_PUBLIC_API_URL` to point to production backend.

## Additional Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [React Documentation](https://react.dev)
- [Better Auth Documentation](https://better-auth.com) (for production auth)
