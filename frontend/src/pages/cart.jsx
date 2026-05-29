import React from 'react';
import { useCart } from '../contexts/CartContext'; 
import { useNavigate } from 'react-router-dom';
import './cart.css'

const Cart = () => {
    const { cartItems, removeFromCart, updateQuantity, getTotal, clearCart } = useCart();
    const navigate = useNavigate();

    if (cartItems.length === 0){
        return (
          <div className="cart-empty">
            <h2>Корзина пуста</h2>
            <button onClick={() => navigate('/')}>На главную</button>
          </div>
        );
    };

    const handleCheckout = () => {
        const token = localStorage.getItem('access_token');
        if (!token){
            localStorage.setItem('redirectAfterLogin', '/cart')
            navigate('/auth/login');
            return;
        }
        navigate('/order')
    };

    return (
    <div className="cart">
      <h2 className="cart-title">Корзина</h2>

      <div className="cart-grid">
        <div className="cart-items">
          {cartItems.map(item => (
            <div key={item.id} className="cart-item">
              
              <img src={item.image_url} alt={item.name} />

              <div className="cart-item-info">
                <h4>{item.name}</h4>
                <p className="price">{item.price} ₽</p>

                <div className="controls">
                  <button onClick={() => updateQuantity(item.id, item.quantity - 1)}>-</button>
                  <span>{item.quantity}</span>
                  <button onClick={() => updateQuantity(item.id, item.quantity + 1)}>+</button>
                </div>

                <button 
                  className="remove"
                  onClick={() => removeFromCart(item.id)}
                >
                  Удалить
                </button>
              </div>

            </div>
          ))}
        </div>

        <div className="cart-summary">
          <h3>Итого</h3>
          <div className="total">{getTotal()} ₽</div>

          <button className="checkout" onClick={handleCheckout}>
            Оформить заказ
          </button>

          <button className="clear" onClick={clearCart}>
            Очистить корзину
          </button>
        </div>
      </div>
    </div>
  );
};

export default Cart;