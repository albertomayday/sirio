import Head from 'next/head';

export default function Home() {
  return (
    <>
      <Head>
        <title>Sirio TPV v1.0.0</title>
        <meta name="description" content="Sistema Punto de Venta - Sirio TPV" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <iframe 
        src="/static/index.html" 
        style={{
          width: '100vw',
          height: '100vh',
          border: 'none',
          position: 'fixed',
          top: 0,
          left: 0,
        }}
        title="Sirio TPV"
      />
    </>
  );
}
