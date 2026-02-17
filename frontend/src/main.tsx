import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import './index.css';
import './i18n';
import { AuthPage } from './features/auth/AuthPage';
import { PlantsPage } from './features/plants/PlantsPage';

function App() {
  return (
    <BrowserRouter>
      <main className="mx-auto max-w-4xl p-4">
        <Routes>
          <Route path="/" element={<AuthPage />} />
          <Route path="/plants" element={<PlantsPage />} />
        </Routes>
      </main>
    </BrowserRouter>
  );
}

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
