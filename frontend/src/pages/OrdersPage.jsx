import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../api';
import './orderPage.css'


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
  <div className="container">   {/* ВОТ ЭТО КЛЮЧЕВОЕ */}
    
    <div className="orders-layout">

      <div className="orders-list">
        <h2>МОИ ЗАКАЗЫ</h2>

        {orders.map(order => (
          <div key={order.id} className="order-card">
            <Link to={`/orders/${order.id}`}>

              <div className="order-header">
                <strong>Заказ №{order.id}</strong>
                <span className="order-status">{order.status}</span>
              </div>

              <div>Сумма: {order.amount} ₽</div>

              <div className="order-preview">
                {order.items?.slice(0, 5).map(item => (
                  <img key={item.id} src={item.image_url} alt="" />
                ))}
              </div>

            </Link>
          </div>
        ))}

      </div>

      <div className="orders-sidebar">
        <h3>Информация</h3>
        <p>— фильтр заказов</p>
        <p>— статусы</p>
        <p>— повтор заказа</p>
      </div>

    </div>

  </div>
);
};

export default MyOrders;