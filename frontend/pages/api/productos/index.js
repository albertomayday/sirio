export default async function handler(req, res) {
  // Configurar CORS
  res.setHeader('Access-Control-Allow-Credentials', 'true');
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET,OPTIONS');
  res.setHeader(
    'Access-Control-Allow-Headers',
    'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version'
  );

  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  if (req.method === 'GET') {
    // Devolver lista de productos
    const productos = [
      { id: 1, nombre: 'Agua 1.5L', precio: 0.89, categoria: 'bebidas', badge: '' },
      { id: 2, nombre: 'Refresco Cola', precio: 1.35, categoria: 'bebidas', badge: 'OFERTA' },
      { id: 3, nombre: 'Zumo Naranja', precio: 1.20, categoria: 'bebidas', badge: '' },
      { id: 4, nombre: 'Cerveza Lata', precio: 1.10, categoria: 'bebidas', badge: '' },
      { id: 5, nombre: 'Vino Tinto', precio: 3.50, categoria: 'bebidas', badge: '' },
      { id: 6, nombre: 'Café Solo', precio: 1.20, categoria: 'bebidas', badge: '' },
      { id: 7, nombre: 'Bocadillo', precio: 2.50, categoria: 'comida', badge: '' },
      { id: 8, nombre: 'Hamburguesa', precio: 4.90, categoria: 'comida', badge: 'TOP' },
      { id: 9, nombre: 'Pizza Porción', precio: 2.80, categoria: 'comida', badge: '' },
      { id: 10, nombre: 'Ensalada', precio: 3.20, categoria: 'comida', badge: '' },
      { id: 11, nombre: 'Patatas Fritas', precio: 1.50, categoria: 'comida', badge: '' },
      { id: 12, nombre: 'Leche 1L', precio: 0.99, categoria: 'lacteos', badge: '' },
      { id: 13, nombre: 'Queso', precio: 2.30, categoria: 'lacteos', badge: '' },
      { id: 14, nombre: 'Yogur Pack', precio: 1.65, categoria: 'lacteos', badge: '' },
      { id: 15, nombre: 'Detergente', precio: 3.99, categoria: 'limpieza', badge: '' },
      { id: 16, nombre: 'Papel WC', precio: 2.45, categoria: 'limpieza', badge: 'OFERTA' },
      { id: 17, nombre: 'Bolsa', precio: 0.10, categoria: 'otros', badge: '' },
      { id: 18, nombre: 'Tabaco', precio: 5.50, categoria: 'otros', badge: '' },
      { id: 19, nombre: 'Chicles', precio: 0.80, categoria: 'otros', badge: '' },
      { id: 20, nombre: 'Periódico', precio: 1.50, categoria: 'otros', badge: '' },
    ];

    return res.status(200).json(productos);
  }

  return res.status(405).json({ error: 'Method not allowed' });
}
