/**
 * API Configuration
 * 
 * Automatically detects environment and uses appropriate backend URL:
 * - Development (localhost:5173): Uses local Flask backend at http://127.0.0.1:5000
 * - Production (Vercel): Uses deployed backend URL from environment variable
 */

export const getAPIUrl = () => {
  // Check if we're in development mode
  const isDevelopment = import.meta.env.DEV || window.location.hostname === 'localhost';
  
  if (isDevelopment) {
    // Development environment - use local Flask backend
    return 'http://127.0.0.1:5000';
  }
  
  // Production environment - use deployed backend
  // Set VITE_API_URL environment variable in Vercel
  const apiUrl = import.meta.env.VITE_API_URL;
  
  if (!apiUrl) {
    console.warn(
      'VITE_API_URL not set. Using relative URL. ' +
      'Set VITE_API_URL environment variable in Vercel for proper backend connection.'
    );
    // If no URL set, try relative path (works if backend and frontend on same domain)
    return '';
  }
  
  return apiUrl;
};

export const API_URL = getAPIUrl();

export default {
  API_URL,
  PREDICT_ENDPOINT: `${API_URL}/predict`,
  getAPIUrl
};
