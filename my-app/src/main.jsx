import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import './index.css';
import App from './App.jsx';

/*
// code kích hoạt mock API
async function prepare() {
  if (import.meta.env.DEV) {
    const { worker } = await import('./mocks/browser.js'); 
    await worker.start({ onUnhandledRequest: 'warn' });
  }
}

prepare().finally(() => {
  createRoot(document.getElementById('root')).render(
    <StrictMode>
      <App />
    </StrictMode>
  );
});
*/

// Không dùng MSW
createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>
);
