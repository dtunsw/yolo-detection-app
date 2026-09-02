import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Route, Routes } from 'react-router-dom'
import './index.css'
import App from './App.jsx'
import Health from './pages/health.jsx'
import ImageUpload from './components/ImageUpload.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<App />} />
        <Route path="/health" element={<Health />} />
        <Route path="/upload" element={<ImageUpload />} />
      </Routes>
    </BrowserRouter>
  </StrictMode>,
)

