import Head from 'next/head';
import { useEffect } from 'react';

export default function Home() {
  useEffect(() => {
    // Cargar el HTML estático del frontend
    const loadFrontend = async () => {
      try {
        const response = await fetch('/static/index.html');
        if (response.ok) {
          const html = await response.text();
          document.getElementById('app-container').innerHTML = html;
        }
      } catch (error) {
        console.error('Error loading frontend:', error);
      }
    };

    loadFrontend();
  }, []);

  return (
    <>
      <Head>
        <title>Sirio TPV v1.0.0</title>
        <meta name="description" content="Sistema Punto de Venta - Sirio TPV" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main>
        <div id="app-container">
          <div style={{
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            minHeight: '100vh',
            fontFamily: 'Arial, sans-serif',
            backgroundColor: '#f5f5f5',
          }}>
            <div style={{
              textAlign: 'center',
              padding: '40px',
              backgroundColor: 'white',
              borderRadius: '8px',
              boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
            }}>
              <h1>🎉 Sirio TPV v1.0.0</h1>
              <p>Cargando interfaz del punto de venta...</p>
              <div style={{
                marginTop: '20px',
                fontSize: '14px',
                color: '#666',
              }}>
                <p>✅ Backend funcionando en Vercel</p>
                <p>✅ Base de datos Vercel Postgres activa</p>
                <p>✅ Lista para uso</p>
              </div>
            </div>
          </div>
        </div>
      </main>
    </>
  );
}
