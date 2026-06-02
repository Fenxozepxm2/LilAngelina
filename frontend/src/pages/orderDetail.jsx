import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import api from '../api';
import './orderDetail.css'


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
   <div className="order-details-layout">

  {/* ЛЕВО */}
  <div className="order-items">
    {order.items.map(item => (
      <div className="order-item-row" key={item.id}>
        <img src={item.image_url} />

        <div>
          <div>{item.quantity} x {item.price} ₽</div>
        </div>

        <div>{item.price * item.quantity} ₽</div>
      </div>
    ))}
  </div>

  {/* ПРАВО */}
  <div className="order-info">
    <h2>Заказ №{order.id}</h2>
    <p>{order.status}</p>
    <p>{order.amount} ₽</p>
    <p>{order.adress}</p>
  </div>

</div>
  );
};

export default OrderDetails;