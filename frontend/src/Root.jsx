import { Routes, Route } from 'react-router-dom'
import App from './App'
import Cart from './pages/cart'

export default function Root() {
  return (
    <Routes>
      <Route path="/" element={<App />} />
      <Route path="/cart" element={<Cart />} />
    </Routes>
  )
}