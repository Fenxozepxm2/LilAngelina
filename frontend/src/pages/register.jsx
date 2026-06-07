import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import api from '../api';

const Register = () => {
  const [form, setForm] = useState({
    username: '',
    password: '',
    phone: '',
    mail: ''
  });

  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  const handleChange = (e) =>
    setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.post('/auth/register', form);
      setMessage('Регистрация успешна');
      setTimeout(() => navigate('/login'), 1500);
    } catch (err) {
      setMessage(err.response?.data?.detail || 'Ошибка регистрации');
    }
  };

  return (
    <div className="auth-page">
      <form className="auth-box" onSubmit={handleSubmit}>
        <h2>Регистрация</h2>

        <input
          name="username"
          placeholder="Логин"
          onChange={handleChange}
          required
        />

        <input
          name="password"
          type="password"
          placeholder="Пароль"
          onChange={handleChange}
          required
        />

        <input
          name="phone"
          placeholder="Телефон"
          onChange={handleChange}
        />

        <input
          name="mail"
          placeholder="Email"
          onChange={handleChange}
        />

        <button type="submit">Создать аккаунт</button>

        {message && <p className="auth-message">{message}</p>}

        <p>
          Уже есть аккаунт? <Link to="/login">Войти</Link>
        </p>
      </form>
    </div>
  );
};

export default Register;