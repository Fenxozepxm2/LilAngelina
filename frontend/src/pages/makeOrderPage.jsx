import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useCart } from '../contexts/CartContext';
import api from '../api';
import './makeOrderPage.css'

const OrderPage = () => {
  const { cartItems, getTotal, clearCart } = useCart();
  const navigate = useNavigate();
  const [form, setForm] = useState({
    first_name: '',
    last_name: '',
    surname: '',
    adress: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  if (cartItems.length === 0) {
    return (
      <div className="checkout-empty">
        <h2>Корзина пуста</h2>
        <button onClick={() => navigate('/')}>Вернуться в каталог</button>
      </div>
    );
  }

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    const payload = {
      first_name: form.first_name,
      last_name: form.last_name,
      surname: form.surname,
      adress: form.adress,
      items: cartItems.map(item => ({
        item_type: item.item_type,
        item_id: item.item_id,
        quantity: item.quantity,
        price: item.price,
      })),
    };

    try {
      const token = localStorage.getItem('access_token');
      await api.post('/api/add_order', payload, {
        headers: { Authorization: `Bearer ${token}` }
      });
      clearCart();                    // очищаем корзину
      navigate('/myOrders');            // на страницу моих заказов
    } catch (err) {
      setError('Ошибка при оформлении заказа. Попробуйте позже.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="checkout-page">
  <h2>Оформление заказа</h2>

  <div className="checkout-layout">

    {/* ЛЕВАЯ ЧАСТЬ — ФОРМА */}
    <form onSubmit={handleSubmit} className="checkout-form">

      <div className="form-grid">
        <input
          type="text"
          name="first_name"
          placeholder="Имя"
          value={form.first_name}
          onChange={handleChange}
          required
        />

        <input
          type="text"
          name="last_name"
          placeholder="Фамилия"
          value={form.last_name}
          onChange={handleChange}
          required
        />

        <input
          type="text"
          name="surname"
          placeholder="Отчество (необязательно)"
          value={form.surname}
          onChange={handleChange}
        />

        <input
          type="text"
          name="adress"
          placeholder="Адрес доставки"
          value={form.adress}
          onChange={handleChange}
          required
        />
      </div>

      <button type="submit" disabled={loading}>
        {loading ? 'Оформляем...' : 'Подтвердить заказ'}
      </button>

      {error && <p className="error">{error}</p>}
    </form>

    {/* ПРАВАЯ ЧАСТЬ — ЗАКАЗ */}
    <div className="order-summary">

      <h3>Ваш заказ</h3>

      {cartItems.map(item => (
        <div className="order-item" key={item.id}>
          <img src={item.image_url} alt={item.name} />

          <div className="order-item-info">
            <div>{item.name}</div>
            <div>{item.quantity} x {item.price} ₽</div>
          </div>

          <div className="order-price">
            {item.price * item.quantity} ₽
          </div>
        </div>
      ))}

      <div className="order-total">
        Итого: {getTotal()} ₽
      </div>

    </div>

  </div>
</div>
  );
};

export default OrderPage;