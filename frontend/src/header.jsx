import { useEffect, useState } from "react";
import { Link, useNavigate, useLocation } from "react-router-dom";
import { useCart } from "./contexts/CartContext";
import "./Header.css";

const Header = () => {   // ← убираем cartCount из пропсов
  const navigate = useNavigate();
  const location = useLocation();
  const { cartItems } = useCart();   // ← получаем корзину

  const isLoggedIn = !!localStorage.getItem('access_token');
  const username = localStorage.getItem('username');

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('username');
    navigate('/login');
  };

  // считаем общее количество товаров
  const cartCount = cartItems.reduce((sum, item) => sum + item.quantity, 0);
  const [scrolled, setScrolled] = useState(false);
  useEffect(() => {
  const handleScroll = () => {
    setScrolled(window.scrollY > 20);
  };

  window.addEventListener("scroll", handleScroll);
  return () => window.removeEventListener("scroll", handleScroll);
}, []);
  const isActive = (path) => location.pathname === path;

  return (
    <header className={`header-modern ${scrolled ? "scrolled" : ""}`}>
      <div className="logo">
        f*ck style<span className="logo-accent">✦</span>
      </div>

      <nav className="nav-modern">
        <Link to="/" className={isActive("/") ? "active" : ""}>
          Главная
        </Link>

        <Link to="/cart" className={isActive("/cart") ? "active" : ""}>
          Корзина
          {cartCount > 0 && (
            <span className="cart-badge">{cartCount}</span>
          )}
        </Link>

        <Link to="/myOrders" className={isActive("/myOrders") ? "active" : ""}>
          Заказы
        </Link>
      </nav>

      <div className="header-right">
        {!isLoggedIn ? (
          <>
            <Link to="/login" className="auth-link">Войти</Link>
            <Link to="/register" className="auth-btn">Регистрация</Link>
          </>
        ) : (
          <>
            <span className="username">{username}</span>
            <button onClick={handleLogout} className="logout">Выйти</button>
          </>
        )}
      </div>
    </header>
  );
};

export default Header;