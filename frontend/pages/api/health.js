import { sql } from '@vercel/postgres';

export default async function handler(req, res) {
  try {
    // Health check en la DB
    const result = await sql`SELECT NOW() as "currentTime"`;
    
    res.status(200).json({
      status: 'healthy',
      timestamp: result.rows[0].currentTime,
      version: '1.0.0',
      environment: process.env.NODE_ENV,
    });
  } catch (error) {
    console.error('Health check error:', error);
    res.status(503).json({
      status: 'unhealthy',
      error: error.message,
    });
  }
}
