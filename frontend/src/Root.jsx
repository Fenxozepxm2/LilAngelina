import { Routes, Route } from 'react-router-dom';
import App from './App';
import Cart from './pages/cart';
import Login from './pages/login';
import Register from './pages/register';
import OrderPage from './pages/makeOrderPage';
import MyOrders from './pages/OrdersPage';
import OrderDetails from './pages/orderDetail';

export default function Root() {
  return (
    <Routes>
      <Route path="/" element={<App />} />
      <Route path="/cart" element={<Cart />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/order" element={<OrderPage />} />
      <Route path="/myOrders" element={<MyOrders />} />
      <Route path="/orders/:id" element={<OrderDetails />} />
    </Routes>
  );
}