import { useEffect, useState } from "react";
import axios from "axios";
import { Link } from "react-router-dom";   // ← добавить
import './App.css';
import { useCart } from "./contexts/CartContext";

export default function App() {
  const [posters, setPosters] = useState([]);
  const [loading, setLoading] = useState(true);
  const { addToCart, cartItems } = useCart();   // ← добавить cartItems

  useEffect(() => {
    fetchPosters();
  }, []);

  const fetchPosters = async () => {
    try {
      const res = await axios.get("/api/posters");
      setPosters(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="loading">Loading...</div>;

  const handleAddPosterToCart = (poster) => {
    addToCart({
      id: `poster-${poster.id}`,
      item_type: "poster",
      item_id: poster.id,
      name: poster.name,
      price: poster.price,
      image_url: poster.poster_url,
    });
    alert(`Постер "${poster.name}" добавлен в корзину`);
  };

  const featuredPosters = posters.slice(0, 4);
  const allPosters = posters.slice(0);
  const cartCount = cartItems.reduce((sum, item) => sum + item.quantity, 0);

  return (
    <div className="container">
      {/* HEADER с ссылкой на корзину */}
      <div className="header">
        <span className="logo">f*ck style</span>
        <div className="icons">
          <Link to="/cart" style={{ textDecoration: 'none', color: 'inherit' }}>
            🛒 Корзина {cartCount > 0 && `(${cartCount})`}
          </Link>
          <span className="icon">⌂</span>
          <span className="icon">★</span>
        </div>
      </div>

      <div className="featured-grid">
        {featuredPosters.map((item) => (
          <div key={item.id} className="poster-card">
            <img src={item.poster_url} alt="" className="poster-image" />
          </div>
        ))}
      </div>

      <h2 className="title">assortment</h2>

      <div className="grid">
        {allPosters.map((item) => (
          <div key={item.id} className="card">
            <img src={item.poster_url} alt={item.name} className="image" />
            <button className="buy-btn" onClick={() => handleAddPosterToCart(item)}>
              BUY
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}