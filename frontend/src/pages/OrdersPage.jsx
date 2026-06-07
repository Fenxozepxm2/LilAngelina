import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../api';
import './orderPage.css'
import Header from '../header';


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
    <Header/> 
    <div className="orders-layout">

      <div className="orders-list">
        <h2>МОИ ЗАКАЗЫ</h2>

        {orders.map(order => (
          <div className="order-card" key={order.id}>
            
           
            <div 
              className="order-bg"
              style={{ backgroundImage: `url(${order.items[0]?.image_url})` }}
            />

            <div className="order-inner">
              
              {/* ЛЕВО — ГЛАВНЫЙ ПОСТЕР */}
              <div className="order-poster">
                <img src={order.items[0]?.image_url} alt="" />
              </div>

              {/* ПРАВО — ИНФА */}
              <div className="order-info">
                <h3>Заказ №{order.id}</h3>

                <span className="status">{order.status}</span>

                <p className="amount">Сумма: {order.amount} ₽</p>

                <div className="items-preview">
                  {order.items.slice(1, 4).map(item => (
                    <img key={item.id} src={item.image_url} />
                  ))}
                </div>

              </div>

            </div>
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