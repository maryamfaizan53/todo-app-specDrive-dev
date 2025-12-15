/**
 * Simplified authentication utility
 *
 * NOTE: This is a simplified implementation for demonstration.
 * In production, use Better Auth library for full authentication features.
 *
 * This module provides basic auth functions that work with JWT tokens.
 */

const AUTH_TOKEN_KEY = 'auth_token';
const AUTH_USER_KEY = 'auth_user';

/**
 * Get current authenticated user from localStorage
 * @returns {Object|null} User object or null if not authenticated
 */
export function getUser() {
  if (typeof window === 'undefined') return null;

  const userStr = localStorage.getItem(AUTH_USER_KEY);
  if (!userStr) return null;

  try {
    return JSON.parse(userStr);
  } catch {
    return null;
  }
}

/**
 * Get JWT token from localStorage
 * @returns {string|null} JWT token or null
 */
export function getToken() {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem(AUTH_TOKEN_KEY);
}

/**
 * Set user and token in localStorage
 * @param {Object} user - User object with id and email
 * @param {string} token - JWT token
 */
export function setAuth(user, token) {
  if (typeof window === 'undefined') return;

  localStorage.setItem(AUTH_USER_KEY, JSON.stringify(user));
  localStorage.setItem(AUTH_TOKEN_KEY, token);
}

/**
 * Clear authentication data
 */
export function clearAuth() {
  if (typeof window === 'undefined') return;

  localStorage.removeItem(AUTH_USER_KEY);
  localStorage.removeItem(AUTH_TOKEN_KEY);
}

/**
 * Login function (simplified - in production use Better Auth)
 * @param {string} email
 * @param {string} password
 * @returns {Promise<Object>} User object
 */
export async function login(email, password) {
  // This is a mock implementation for demonstration
  // In production, this should call Better Auth login endpoint

  // For demo, create a mock JWT token and user
  const mockUser = {
    id: 'demo-user-' + Math.random().toString(36).substr(2, 9),
    email: email,
    name: email.split('@')[0]
  };

  // Create a mock JWT token (in production, this comes from Better Auth)
  const mockToken = btoa(JSON.stringify({
    sub: mockUser.id,
    email: mockUser.email,
    iat: Date.now() / 1000,
    exp: Date.now() / 1000 + 86400 // 24 hours
  }));

  setAuth(mockUser, mockToken);
  return mockUser;
}

/**
 * Signup function (simplified - in production use Better Auth)
 * @param {string} email
 * @param {string} password
 * @param {string} name
 * @returns {Promise<Object>} User object
 */
export async function signup(email, password, name) {
  // This is a mock implementation
  // In production, this should call Better Auth signup endpoint
  return login(email, password);
}

/**
 * Logout function
 */
export function logout() {
  clearAuth();
  if (typeof window !== 'undefined') {
    window.location.href = '/';
  }
}

/**
 * Check if user is authenticated
 * @returns {boolean}
 */
export function isAuthenticated() {
  return !!getToken() && !!getUser();
}
