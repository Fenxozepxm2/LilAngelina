import { Routes, Route } from 'react-router-dom';
import App from './App';
import Cart from './pages/cart';
import Login from './pages/login';
import Register from './pages/register';
import OrderPage from './pages/orderPage';

export default function Root() {
  return (
    <Routes>
      <Route path="/" element={<App />} />
      <Route path="/cart" element={<Cart />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/order" element={<OrderPage />} />
    </Routes>
  );
}