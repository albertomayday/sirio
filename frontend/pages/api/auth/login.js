export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Credentials', 'true');
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET,OPTIONS,PATCH,DELETE,POST,PUT');
  res.setHeader(
    'Access-Control-Allow-Headers',
    'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version'
  );

  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  if (req.method === 'POST') {
    const { username, password } = req.body;

    // Validación básica
    if (!username || !password) {
      return res.status(400).json({ error: 'Username and password required' });
    }

    // TODO: Implementar autenticación real con JWT
    // Por ahora, devolver token mock
    const token = Buffer.from(`${username}:${Date.now()}`).toString('base64');

    return res.status(200).json({
      message: 'Authentication successful',
      token,
      user: {
        username,
        role: 'admin',
      },
    });
  }

  if (req.method === 'GET') {
    // Validar token
    const auth = req.headers.authorization;

    if (!auth) {
      return res.status(401).json({ error: 'Authorization required' });
    }

    return res.status(200).json({
      message: 'Token is valid',
      authenticated: true,
    });
  }

  return res.status(405).json({ error: 'Method not allowed' });
}
