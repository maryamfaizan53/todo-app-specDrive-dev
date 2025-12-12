"""
Comprehensive tests for task API endpoints.

Tests cover:
- CRUD operations (Create, Read, Update, Delete)
- JWT authentication and authorization
- User data isolation
- Input validation
- Error handling
"""
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.models import Task


class TestCreateTask:
    """Tests for POST /api/{user_id}/tasks"""

    def test_create_task_success(self, client: TestClient, test_user, auth_headers):
        """Test creating a task with valid data."""
        response = client.post(
            f"/api/{test_user['id']}/tasks",
            json={"title": "New Task", "description": "Task description"},
            headers=auth_headers
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "New Task"
        assert data["description"] == "Task description"
        assert data["completed"] is False
        assert data["user_id"] == test_user["id"]
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data

    def test_create_task_without_description(self, client: TestClient, test_user, auth_headers):
        """Test creating a task without description."""
        response = client.post(
            f"/api/{test_user['id']}/tasks",
            json={"title": "Task without description"},
            headers=auth_headers
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Task without description"
        assert data["description"] is None

    def test_create_task_missing_token(self, client: TestClient, test_user):
        """Test creating a task without JWT token."""
        response = client.post(
            f"/api/{test_user['id']}/tasks",
            json={"title": "New Task"}
        )
        assert response.status_code == 401

    def test_create_task_invalid_token(self, client: TestClient, test_user):
        """Test creating a task with invalid JWT token."""
        response = client.post(
            f"/api/{test_user['id']}/tasks",
            json={"title": "New Task"},
            headers={"Authorization": "Bearer invalid-token"}
        )
        assert response.status_code == 401

    def test_create_task_mismatched_user_id(self, client: TestClient, test_user, auth_headers):
        """Test creating a task for different user (should fail)."""
        response = client.post(
            "/api/different-user/tasks",
            json={"title": "New Task"},
            headers=auth_headers
        )
        assert response.status_code == 403
        assert "Forbidden" in response.json()["detail"]

    def test_create_task_empty_title(self, client: TestClient, test_user, auth_headers):
        """Test creating a task with empty title."""
        response = client.post(
            f"/api/{test_user['id']}/tasks",
            json={"title": ""},
            headers=auth_headers
        )
        assert response.status_code == 422


class TestListTasks:
    """Tests for GET /api/{user_id}/tasks"""

    def test_list_tasks_success(self, client: TestClient, test_user, auth_headers, sample_tasks):
        """Test listing all tasks for authenticated user."""
        response = client.get(
            f"/api/{test_user['id']}/tasks",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 3

    def test_list_tasks_empty(self, client: TestClient, test_user, auth_headers):
        """Test listing tasks when user has no tasks."""
        response = client.get(
            f"/api/{test_user['id']}/tasks",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0

    def test_list_tasks_filter_completed(self, client: TestClient, test_user, auth_headers, sample_tasks):
        """Test filtering tasks by completion status."""
        response = client.get(
            f"/api/{test_user['id']}/tasks?completed=true",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["completed"] is True

    def test_list_tasks_filter_incomplete(self, client: TestClient, test_user, auth_headers, sample_tasks):
        """Test filtering incomplete tasks."""
        response = client.get(
            f"/api/{test_user['id']}/tasks?completed=false",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert all(not task["completed"] for task in data)

    def test_list_tasks_search(self, client: TestClient, test_user, auth_headers, sample_tasks):
        """Test searching tasks by title/description."""
        response = client.get(
            f"/api/{test_user['id']}/tasks?search=First",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert "First" in data[0]["description"]

    def test_list_tasks_missing_token(self, client: TestClient, test_user):
        """Test listing tasks without JWT token."""
        response = client.get(f"/api/{test_user['id']}/tasks")
        assert response.status_code == 401

    def test_list_tasks_mismatched_user_id(self, client: TestClient, auth_headers):
        """Test listing tasks for different user (should fail)."""
        response = client.get(
            "/api/different-user/tasks",
            headers=auth_headers
        )
        assert response.status_code == 403

    def test_list_tasks_user_isolation(
        self,
        client: TestClient,
        session: Session,
        test_user,
        test_user_2,
        auth_headers,
        sample_tasks
    ):
        """Test that users can only see their own tasks."""
        # Create task for user 2
        task_user_2 = Task(
            user_id=test_user_2["id"],
            title="User 2 Task",
            completed=False
        )
        session.add(task_user_2)
        session.commit()

        # User 1 should only see their tasks (3 from sample_tasks)
        response = client.get(
            f"/api/{test_user['id']}/tasks",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        assert all(task["user_id"] == test_user["id"] for task in data)


class TestGetTask:
    """Tests for GET /api/{user_id}/tasks/{task_id}"""

    def test_get_task_success(self, client: TestClient, test_user, auth_headers, sample_task):
        """Test getting a specific task."""
        response = client.get(
            f"/api/{test_user['id']}/tasks/{sample_task.id}",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == sample_task.id
        assert data["title"] == sample_task.title

    def test_get_task_not_found(self, client: TestClient, test_user, auth_headers):
        """Test getting non-existent task."""
        response = client.get(
            f"/api/{test_user['id']}/tasks/non-existent-id",
            headers=auth_headers
        )
        assert response.status_code == 404

    def test_get_task_missing_token(self, client: TestClient, test_user, sample_task):
        """Test getting task without JWT token."""
        response = client.get(f"/api/{test_user['id']}/tasks/{sample_task.id}")
        assert response.status_code == 401

    def test_get_task_different_user(
        self,
        client: TestClient,
        session: Session,
        test_user_2,
        auth_headers_user_2,
        sample_task
    ):
        """Test getting task belonging to different user (should fail)."""
        response = client.get(
            f"/api/{test_user_2['id']}/tasks/{sample_task.id}",
            headers=auth_headers_user_2
        )
        assert response.status_code == 404


class TestUpdateTask:
    """Tests for PUT /api/{user_id}/tasks/{task_id}"""

    def test_update_task_success(self, client: TestClient, test_user, auth_headers, sample_task):
        """Test updating a task with valid data."""
        response = client.put(
            f"/api/{test_user['id']}/tasks/{sample_task.id}",
            json={"title": "Updated Title", "description": "Updated description"},
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["description"] == "Updated description"
        assert data["id"] == sample_task.id

    def test_update_task_not_found(self, client: TestClient, test_user, auth_headers):
        """Test updating non-existent task."""
        response = client.put(
            f"/api/{test_user['id']}/tasks/non-existent-id",
            json={"title": "Updated Title"},
            headers=auth_headers
        )
        assert response.status_code == 404

    def test_update_task_empty_title(self, client: TestClient, test_user, auth_headers, sample_task):
        """Test updating task with empty title."""
        response = client.put(
            f"/api/{test_user['id']}/tasks/{sample_task.id}",
            json={"title": ""},
            headers=auth_headers
        )
        assert response.status_code == 422

    def test_update_task_missing_token(self, client: TestClient, test_user, sample_task):
        """Test updating task without JWT token."""
        response = client.put(
            f"/api/{test_user['id']}/tasks/{sample_task.id}",
            json={"title": "Updated Title"}
        )
        assert response.status_code == 401

    def test_update_task_different_user(
        self,
        client: TestClient,
        test_user_2,
        auth_headers_user_2,
        sample_task
    ):
        """Test updating task belonging to different user (should fail)."""
        response = client.put(
            f"/api/{test_user_2['id']}/tasks/{sample_task.id}",
            json={"title": "Updated Title"},
            headers=auth_headers_user_2
        )
        assert response.status_code == 404


class TestDeleteTask:
    """Tests for DELETE /api/{user_id}/tasks/{task_id}"""

    def test_delete_task_success(self, client: TestClient, test_user, auth_headers, sample_task):
        """Test deleting a task."""
        response = client.delete(
            f"/api/{test_user['id']}/tasks/{sample_task.id}",
            headers=auth_headers
        )
        assert response.status_code == 204

        # Verify task is deleted
        response = client.get(
            f"/api/{test_user['id']}/tasks/{sample_task.id}",
            headers=auth_headers
        )
        assert response.status_code == 404

    def test_delete_task_not_found(self, client: TestClient, test_user, auth_headers):
        """Test deleting non-existent task."""
        response = client.delete(
            f"/api/{test_user['id']}/tasks/non-existent-id",
            headers=auth_headers
        )
        assert response.status_code == 404

    def test_delete_task_missing_token(self, client: TestClient, test_user, sample_task):
        """Test deleting task without JWT token."""
        response = client.delete(f"/api/{test_user['id']}/tasks/{sample_task.id}")
        assert response.status_code == 401

    def test_delete_task_different_user(
        self,
        client: TestClient,
        test_user_2,
        auth_headers_user_2,
        sample_task
    ):
        """Test deleting task belonging to different user (should fail)."""
        response = client.delete(
            f"/api/{test_user_2['id']}/tasks/{sample_task.id}",
            headers=auth_headers_user_2
        )
        assert response.status_code == 404


class TestToggleCompletion:
    """Tests for PATCH /api/{user_id}/tasks/{task_id}/complete"""

    def test_toggle_completion_to_true(self, client: TestClient, test_user, auth_headers, sample_task):
        """Test marking task as complete."""
        response = client.patch(
            f"/api/{test_user['id']}/tasks/{sample_task.id}/complete",
            json={"completed": True},
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["completed"] is True
        assert data["id"] == sample_task.id

    def test_toggle_completion_to_false(self, client: TestClient, test_user, auth_headers, sample_task):
        """Test marking task as incomplete."""
        # First mark as complete
        client.patch(
            f"/api/{test_user['id']}/tasks/{sample_task.id}/complete",
            json={"completed": True},
            headers=auth_headers
        )

        # Then mark as incomplete
        response = client.patch(
            f"/api/{test_user['id']}/tasks/{sample_task.id}/complete",
            json={"completed": False},
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["completed"] is False

    def test_toggle_completion_not_found(self, client: TestClient, test_user, auth_headers):
        """Test toggling completion for non-existent task."""
        response = client.patch(
            f"/api/{test_user['id']}/tasks/non-existent-id/complete",
            json={"completed": True},
            headers=auth_headers
        )
        assert response.status_code == 404

    def test_toggle_completion_missing_token(self, client: TestClient, test_user, sample_task):
        """Test toggling completion without JWT token."""
        response = client.patch(
            f"/api/{test_user['id']}/tasks/{sample_task.id}/complete",
            json={"completed": True}
        )
        assert response.status_code == 401

    def test_toggle_completion_different_user(
        self,
        client: TestClient,
        test_user_2,
        auth_headers_user_2,
        sample_task
    ):
        """Test toggling completion for task belonging to different user (should fail)."""
        response = client.patch(
            f"/api/{test_user_2['id']}/tasks/{sample_task.id}/complete",
            json={"completed": True},
            headers=auth_headers_user_2
        )
        assert response.status_code == 404


class TestHealthEndpoints:
    """Tests for health check endpoints"""

    def test_root_endpoint(self, client: TestClient):
        """Test root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data

    def test_health_check(self, client: TestClient):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
