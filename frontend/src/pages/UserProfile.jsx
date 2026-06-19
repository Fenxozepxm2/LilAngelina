import React, { useState, useEffect } from 'react';
import api from '../api';
import Header from '../header';
import './UserProfile.css'
import { useToast } from "../contexts/ToastContext";

const UserProfile = () => {
  const [user, setUser] = useState({
    username: '',
    phone: '',
    mail: '',
    adres: ''
  });

  const [editMode, setEditMode] = useState(false);
  const [loading, setLoading] = useState(true);

  const { addToast } = useToast();

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const res = await api.get('/profile/me');
        setUser(res.data);
      } catch (err) {
        addToast("Ошибка загрузки профиля", "error");
      } finally {
        setLoading(false);
      }
    };

    fetchProfile();
  }, []);

  const handleChange = (e) => {
    setUser({ ...user, [e.target.name]: e.target.value });
  };

  const handleSave = async () => {
    try {
      const payload = {
        phone: user.phone || null,
        mail: user.mail || null,
        adres: user.adres || null,
      };

      await api.put('/profile/me', payload);

      addToast("Профиль обновлён", "success");
      setEditMode(false);

    } catch (err) {
      addToast("Ошибка обновления", "error");
    }
  };

  if (loading) return <div className="loading">Загрузка...</div>;

  return (
    <div className="container">

        <Header/>
      <div className="profile-page">
      <div className="profile-card">

        <div className="profile-header">
          <h2>{user.username}</h2>

          {!editMode ? (
            <button onClick={() => setEditMode(true)} className="edit-btn">
              Изменить
            </button>
          ) : (
            <div className="edit-actions">
              <button onClick={handleSave} className="save-btn">
                Сохранить
              </button>
              <button onClick={() => setEditMode(false)} className="cancel-btn">
                Отмена
              </button>
            </div>
          )}
        </div>

        <div className="profile-fields">

          <div className="field">
            <label>Телефон</label>
            {editMode ? (
              <input
                name="phone"
                value={user.phone || ''}
                onChange={handleChange}
              />
            ) : (
              <span>{user.phone || "—"}</span>
            )}
          </div>

          <div className="field">
            <label>Email</label>
            {editMode ? (
              <input
                name="mail"
                value={user.mail || ''}
                onChange={handleChange}
              />
            ) : (
              <span>{user.mail || "—"}</span>
            )}
          </div>

          <div className="field">
            <label>Адрес</label>
            {editMode ? (
              <input
                name="adres"
                value={user.adres || ''}
                onChange={handleChange}
              />
            ) : (
              <span>{user.adres || "—"}</span>
            )}
          </div>

        </div>

      </div>
    </div>
    </div>

  );
};

export default UserProfile;