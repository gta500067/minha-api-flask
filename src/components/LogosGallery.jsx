import React, { useEffect, useState } from 'react';

export default function LogosGallery() {
  const [logos, setLogos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch('https://seu-backend.onrender.com/api/logos') // Troque para a URL real da sua API
      .then((res) => {
        if (!res.ok) throw new Error('Erro ao carregar logos');
        return res.json();
      })
      .then((data) => {
        setLogos(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  if (loading) return <p>Carregando logos...</p>;
  if (error) return <p>Erro: {error}</p>;

  return (
    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '20px' }}>
      {logos.map(({ filename, url }) => (
        <div key={filename} style={{ textAlign: 'center', width: 150 }}>
          <img
            src={url}
            alt={filename}
            style={{ maxWidth: '100%', maxHeight: 100, objectFit: 'contain' }}
          />
          <p style={{ wordBreak: 'break-word' }}>{filename}</p>
        </div>
      ))}
    </div>
  );
}
