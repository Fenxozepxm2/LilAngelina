import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../api';

const MyOrders = () => {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchOrders = async () => {
      try {
        const response = await api.get('/api/orders');
        // Убедимся, что response.data – это массив
        if (Array.isArray(response.data)) {
          setOrders(response.data);
        } else {
          console.error('Ответ сервера не массив:', response.data);
          setOrders([]);
          setError('Неверный формат данных от сервера');
        }
      } catch (err) {
        console.error(err);
        setError('Не удалось загрузить заказы');
        setOrders([]);
      } finally {
        setLoading(false);
      }
    };
    fetchOrders();
  }, []);

  if (loading) return <div>Загрузка...</div>;
  if (error) return <div className="error">{error}</div>;
  if (!orders.length) return <div>У вас пока нет заказов.</div>;

  return (
    <div className="orders-list">
      <h2>Мои заказы</h2>
      {orders.map(order => (
        <div key={order.id} className="order-card">
          <Link to={`/orders/${order.id}`}>
            <div>
              <strong>Заказ №{order.id}</strong> — {order.status}
            </div>
            <div>Сумма: {order.amount} ₽</div>
            <div>Дата: {order.created_at ? new Date(order.created_at).toLocaleDateString() : '—'}</div>
          </Link>
        </div>
      ))}
    </div>
  );
};

export default MyOrders;