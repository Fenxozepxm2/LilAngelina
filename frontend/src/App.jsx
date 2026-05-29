import { useEffect, useState } from "react";
import axios from "axios";  
import './App.css';
import { useCart } from "./contexts/CartContext";
import { Link, useNavigate } from 'react-router-dom';
import Header from "./header";


export default function App() {
  const [posters, setPosters] = useState([]);
  const [loading, setLoading] = useState(true);
  const { addToCart, cartItems } = useCart();   

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
      <Header cartCount={cartCount} />  

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