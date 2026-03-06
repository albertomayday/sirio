import { sql } from '@vercel/postgres';

export default async function handler(req, res) {
  const { id } = req.query;

  try {
    if (req.method === 'GET') {
      // Obtener transacción específica
      const result = await sql`
        SELECT * FROM transactions WHERE id = ${id}
      `;

      if (result.rows.length === 0) {
        return res.status(404).json({ error: 'Transaction not found' });
      }

      return res.status(200).json({
        data: result.rows[0],
      });
    }

    if (req.method === 'PUT') {
      // Actualizar transacción
      const { status, payment_method } = req.body;

      const result = await sql`
        UPDATE transactions 
        SET status = ${status || 'updated'}, 
            payment_method = ${payment_method || 'card'},
            updated_at = NOW()
        WHERE id = ${id}
        RETURNING *
      `;

      if (result.rows.length === 0) {
        return res.status(404).json({ error: 'Transaction not found' });
      }

      return res.status(200).json({
        message: 'Transaction updated',
        data: result.rows[0],
      });
    }

    if (req.method === 'DELETE') {
      // Eliminar transacción
      const result = await sql`
        DELETE FROM transactions WHERE id = ${id}
        RETURNING id
      `;

      if (result.rows.length === 0) {
        return res.status(404).json({ error: 'Transaction not found' });
      }

      return res.status(200).json({
        message: 'Transaction deleted',
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
