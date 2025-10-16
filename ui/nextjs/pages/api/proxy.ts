import type { NextApiRequest, NextApiResponse } from 'next'
export default async function handler(req: NextApiRequest, res: NextApiResponse){
  const base = process.env.RETRIEVER_BASE || "http://localhost:8082";
  const r = await fetch(`${base}/ask`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ case_id: 'CASE-001', question: req.body.question, k: 6 }) });
  const data = await r.json(); res.status(200).json(data);
}