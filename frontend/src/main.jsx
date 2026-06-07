import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import './index.css'
import App from './App.jsx'
import Root from './Root'  
import { CartProvider } from './contexts/CartContext.jsx'
import { ToastProvider } from './contexts/ToastContext.jsx'
import "./toast.css"

createRoot(document.getElementById('root')).render(
  <ToastProvider>
    <StrictMode>
      <CartProvider>
        <BrowserRouter>
          <Root />
        </BrowserRouter>
      </CartProvider>
    </StrictMode>
  </ToastProvider>
)