import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import api from '../api';

const OrderDetails = () => {
  const { id } = useParams();
  const [order, setOrder] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchOrder = async () => {
      try {
        const res = await api.get(`/api/order/${id}`);
        setOrder(res.data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchOrder();
  }, [id]);

  if (loading) return <div>Загрузка...</div>;
  if (!order) return <div>Заказ не найден</div>;

  return (
    <div className="order-details">
      <h2>Заказ №{order.id}</h2>
      <p>Статус: {order.status}</p>
      <p>Сумма: {order.amount} ₽</p>
      <p>Получатель: {order.last_name_usr} {order.first_name_usr} {order.surname || ''}</p>
      <p>Адрес: {order.adress}</p>
      <h3>Товары:</h3>
      <ul>
        {order.items.map(item => (
          <li key={item.id}>
            {item.item_type === 'poster' ? 'Постер' : 'Диск'} (ID {item.item_id}) — 
            {item.quantity} шт. x {item.price} ₽ = {item.price * item.quantity} ₽
          </li>
        ))}
      </ul>
      <Link to="/myOrders">← Назад к заказам</Link>
    </div>
  );
};

export default OrderDetails;