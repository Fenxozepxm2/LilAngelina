import { useEffect, useState } from "react";
import axios from "axios";
import './App.css';

export default function App() {
  const [posters, setPosters] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchPosters();
  },[]);  
  

  const fetchPosters = async() => {
    try{
      const res = await axios.get("/api/posters")
      console.log(res.data)
      setPosters(res.data)
    }catch(err){
      console.error(err)
    }finally{
      setLoading(false)
    }
  };
  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  const featuredPosters = posters.slice(0,4)

  const allPosters = posters.slice(0)



  return (
    <div className="container">
      {/* HEADER */}
      <div className="header">
        <span className="logo">f*ck style</span>
        <div className="icons">
          <span className="icon">⌂</span>
          <span className="icon">★</span>
        </div>
      </div>

      {/* FEATURED (верхние 4 постера) */}
      <div className="featured-grid">
        {featuredPosters.map((item) => (
          <div key={item.id} className="poster-card">
            <img src={item.poster_url} alt="" className="poster-image " />
          </div>
        ))}
      </div>

      {/* TITLE */}
      <h2 className="title">assortment</h2>

      {/* GRID */}
      <div className="grid">
        {allPosters.map((item) => (
          <div key={item.id} className="card">
            <img src={item.poster_url} alt={item.name} className="image" />
            <button className="buy-btn">BUY</button>
          </div>
        ))}
      </div>
    </div>
  );
}