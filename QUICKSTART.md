# Quick Start Guide

Get the Todo Full-Stack Application running in 5 minutes!

## Step 1: Backend Setup (2 minutes)

Open a terminal in the `backend` directory:

```bash
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Create .env file from example
cp .env.example .env
```

Edit `backend/.env` and set:
```
DATABASE_URL=sqlite:///./todo.db
BETTER_AUTH_SECRET=my-super-secret-key-that-is-at-least-32-characters-long-12345
CORS_ORIGINS=http://localhost:3000
```

Start the backend server:
```bash
uvicorn app.main:app --reload --port 8000
```

✅ Backend running at http://localhost:8000
📖 API Docs at http://localhost:8000/docs

## Step 2: Frontend Setup (2 minutes)

Open a **new terminal** in the `frontend` directory:

```bash
cd frontend

# Install Node dependencies
npm install

# Create .env.local file
cp .env.local.example .env.local
```

Edit `frontend/.env.local` and set:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=my-super-secret-key-that-is-at-least-32-characters-long-12345
```

**IMPORTANT**: Use the **same** `BETTER_AUTH_SECRET` as the backend!

Start the frontend server:
```bash
npm run dev
```

✅ Frontend running at http://localhost:3000

## Step 3: Use the App (1 minute)

1. Open http://localhost:3000 in your browser
2. Click "Get Started"
3. Enter any email and password (this is demo mode)
4. Create your first task!

## Verify Everything Works

### Test the Backend

Visit http://localhost:8000/docs to see the interactive API documentation.

Or run the tests:
```bash
cd backend
pytest
```

All tests should pass ✅

### Test the Frontend

1. Create a task
2. Mark it as complete
3. Edit the task
4. Delete the task
5. Try the filters (All, Active, Done)
6. Search for tasks

## Troubleshooting

### Backend errors?
- Check Python version: `python --version` (need 3.11+)
- Make sure .env file exists
- Check if port 8000 is already in use

### Frontend errors?
- Check Node version: `node --version` (need 18+)
- Make sure .env.local file exists
- Check if port 3000 is already in use
- Verify backend is running

### "Failed to fetch" errors?
- Ensure backend is running on http://localhost:8000
- Check that NEXT_PUBLIC_API_URL is set correctly
- Verify BETTER_AUTH_SECRET matches between frontend and backend

## Next Steps

- Read [README.md](README.md) for full documentation
- Check [specs/](specs/) for detailed specifications
- Explore [backend/README.md](backend/README.md) for backend details
- Review [frontend/README.md](frontend/README.md) for frontend details

## Need Help?

1. Check the main README.md
2. Look at the troubleshooting sections
3. Review the code comments
4. Check the specs documentation

Happy coding! 🚀
