import { neon } from '@neondatabase/serverless';

const sql = neon(process.env.DATABASE_URL);

export default async function handler(req, res) {
  // Configurar CORS
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

  try {
    if (req.method === 'GET') {
      // Obtener todas las transacciones
      const { limit = 10, offset = 0 } = req.query;
      
      const rows = await sql`
        SELECT * FROM transactions 
        ORDER BY created_at DESC 
        LIMIT ${limit} OFFSET ${offset}
      `;
      
      return res.status(200).json({
        data: rows,
        count: rows.length,
      });
    }

    if (req.method === 'POST') {
      // Crear nueva transacción
      const {
        items = [],
        subtotal = 0,
        tax = 0,
        total = 0,
        payment_method = 'card',
      } = req.body;

      // Calcular IVA correctamente (por línea)
      const processedItems = items.map(item => ({
        ...item,
        line_tax: (item.quantity * item.price * 0.21), // 21% IVA
        line_total: (item.quantity * item.price) + (item.quantity * item.price * 0.21),
      }));

      // Recalcular totales
      const calculated_subtotal = processedItems.reduce((sum, item) => sum + (item.quantity * item.price), 0);
      const calculated_tax = processedItems.reduce((sum, item) => sum + item.line_tax, 0);
      const calculated_total = calculated_subtotal + calculated_tax;

      const rows = await sql`
        INSERT INTO transactions (
          items, 
          subtotal, 
          tax, 
          total, 
          payment_method, 
          status,
          created_at
        ) VALUES (
          ${JSON.stringify(processedItems)},
          ${calculated_subtotal},
          ${calculated_tax},
          ${calculated_total},
          ${payment_method},
          'completed',
          NOW()
        )
        RETURNING *
      `;

      return res.status(201).json({
        message: 'Transaction created successfully',
        data: rows[0],
        calculation: {
          subtotal: calculated_subtotal,
          tax: calculated_tax,
          total: calculated_total,
        },
      });
    }

    return res.status(405).json({ error: 'Method not allowed' });
  } catch (error) {
    console.error('TPV API error:', error);
    res.status(500).json({
      error: 'Internal server error',
      message: error.message,
    });
  }
}
