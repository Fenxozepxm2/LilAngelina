import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import api from '../api';
import './orderDetail.css'
import Header from '../header';


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
  <div className="container">
    <Header/> 
    <div className="order-details-layout">

      {/* ЛЕВАЯ ЧАСТЬ */}
      <div className="order-items">
        <h2>СОСТАВ ЗАКАЗА</h2>

        {order.items.map(item => (
          <div className="order-item-row" key={item.id}>
            <img src={item.image_url} alt="" />

            <div className="item-info">
              <div className="item-price">
                {item.quantity} × {item.price} ₽
              </div>
            </div>

            <div className="item-total">
              {item.price * item.quantity} ₽
            </div>
          </div>
        ))}
      </div>

      {/* ПРАВАЯ ЧАСТЬ */}
      <div className="order-info">
        <h2>Заказ №{order.id}</h2>

        <div className="info-block">
          <span>Статус</span>
          <p className="status">{order.status}</p>
        </div>

        <div className="info-block">
          <span>Сумма</span>
          <p>{order.amount} ₽</p>
        </div>

        <div className="info-block">
          <span>Адрес</span>
          <p>{order.adress}</p>
        </div>

        <Link to="/myOrders" className="back-btn">
          ← Назад к заказам
        </Link>
      </div>

    </div>

  </div>
);
};

export default OrderDetails;