import { Link, useNavigate } from "react-router-dom";

const Header = ({ cartCount }) => {
  const navigate = useNavigate();
  const isLoggedIn = !!localStorage.getItem('access_token');
  const username = localStorage.getItem('username');

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('username');
    navigate('/login');
  };

  return (
    <header className="header">
      <div className="logo">f*ck style</div>

      <nav className="nav">
        <Link to="/">Главная</Link>
        <Link to="/cart">
          Корзина {cartCount > 0 && `(${cartCount})`}
        </Link>
      </nav>

      <div className="auth">
        {!isLoggedIn ? (
          <>
            <Link to="/login" className="auth-link">Войти</Link>
            <Link to="/register" className="auth-btn">Регистрация</Link>
          </>
        ) : (
          <>
            <span className="username">{username}</span>
            <button onClick={handleLogout} className="logout">
              Выйти
            </button>
          </>
        )}
      </div>
    </header>
  );
};

export default Header;