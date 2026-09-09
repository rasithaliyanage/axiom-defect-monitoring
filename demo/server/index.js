import express from 'express';
import { randomBytes, scryptSync, timingSafeEqual } from 'node:crypto';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { openDatabase, simulate } from './db.js';

export function createApp(databasePath) {
  const db = openDatabase(databasePath);
  const app = express();
  app.disable('x-powered-by');
  app.use(express.json({ limit: '24kb' }));
  app.use('/api', (req, res, next) => {
    res.set('Cache-Control', 'no-store');
    if (!['GET', 'HEAD'].includes(req.method) && req.headers.origin) {
      try { if (new URL(req.headers.origin).host !== req.headers.host) return res.status(403).json({ error: 'Request origin not permitted.' }); }
      catch { return res.status(403).json({ error: 'Invalid origin.' }); }
    }
    next();
  });
  const userView = u => ({ id: u.id, name: u.name, email: u.email, role: u.role });
  const token = req => /(?:^|;\s*)axion_session=([a-f0-9]+)/.exec(req.headers.cookie || '')?.[1];
  app.get('/api/health', (req, res) => res.json({ status: 'ok', demo: true }));
  app.post('/api/login', (req, res) => {
    const { email, password } = req.body || {};
    if (typeof email !== 'string' || typeof password !== 'string' || password.length > 200) return res.status(400).json({ error: 'Enter an email and password.' });
    const user = db.prepare('SELECT * FROM users WHERE email=?').get(email.trim().toLowerCase());
    if (!user || !timingSafeEqual(scryptSync(password, user.salt, 64), Buffer.from(user.password, 'hex'))) return res.status(401).json({ error: 'Email or password is incorrect.' });
    const session = randomBytes(32).toString('hex');
    db.prepare('DELETE FROM sessions WHERE expires < ?').run(Date.now());
    db.prepare('INSERT INTO sessions VALUES (?,?,?)').run(session, user.id, Date.now() + 8 * 3600000);
    res.cookie('axion_session', session, { httpOnly: true, sameSite: 'strict', maxAge: 8 * 3600000, path: '/' });
    res.json(userView(user));
  });
  app.use('/api', (req, res, next) => {
    req.user = db.prepare('SELECT u.* FROM sessions s JOIN users u ON u.id=s.user_id WHERE s.token=? AND s.expires>?').get(token(req) || '', Date.now());
    if (!req.user) return res.status(401).json({ error: 'Please sign in to continue.' });
    next();
  });
  app.get('/api/me', (req, res) => res.json(userView(req.user)));
  app.post('/api/logout', (req, res) => { db.prepare('DELETE FROM sessions WHERE token=?').run(token(req)); res.clearCookie('axion_session', { path: '/' }); res.json({ ok: true }); });
  app.get('/api/workspace', (req, res) => {
    const inspections = db.prepare(`SELECT i.*, l.name AS line_name, COUNT(d.id) AS defect_count FROM inspections i JOIN lines l ON i.line_id=l.id LEFT JOIN defects d ON d.inspection_id=i.id GROUP BY i.id ORDER BY i.captured_at DESC`).all();
    res.json({ inspections, lines: db.prepare('SELECT * FROM lines ORDER BY id').all(), defects: db.prepare('SELECT * FROM defects').all(), generatedAt: new Date().toISOString() });
  });
  app.get('/api/inspections/:id', (req, res) => {
    const board = db.prepare('SELECT i.*, l.name AS line_name, l.camera FROM inspections i JOIN lines l ON i.line_id=l.id WHERE i.id=?').get(req.params.id);
    if (!board) return res.status(404).json({ error: 'Inspection not found.' });
    res.json({ ...board, defects: db.prepare('SELECT * FROM defects WHERE inspection_id=?').all(board.id), reviews: db.prepare('SELECT r.*,u.name AS reviewer FROM reviews r JOIN users u ON r.user_id=u.id WHERE inspection_id=? ORDER BY r.id DESC').all(board.id), audit: db.prepare('SELECT * FROM audit WHERE inspection_id=? ORDER BY id DESC').all(board.id) });
  });
  app.post('/api/inspections/:id/review', (req, res) => {
    const { decision, reason, version } = req.body || {};
    if (!['PASS','FAIL','REVIEW'].includes(decision) || typeof reason !== 'string' || reason.trim().length < 10 || reason.length > 2000 || !Number.isInteger(version)) return res.status(400).json({ error: 'Choose a decision and provide a reason of 10–2,000 characters.' });
    db.exec('BEGIN IMMEDIATE');
    try {
      const row = db.prepare('SELECT * FROM inspections WHERE id=?').get(req.params.id);
      if (!row) { db.exec('ROLLBACK'); return res.status(404).json({ error: 'Inspection not found.' }); }
      if (row.version !== version) { db.exec('ROLLBACK'); return res.status(409).json({ error: 'This inspection changed. Reload it before submitting your decision.' }); }
      if (row.initial_status === 'UNAVAILABLE') { db.exec('ROLLBACK'); return res.status(400).json({ error: 'Incomplete inspection requires re-imaging; it cannot be released here.' }); }
      const now = new Date().toISOString();
      db.prepare('UPDATE inspections SET status=?,version=version+1,claimed_by=? WHERE id=?').run(decision, req.user.id, row.id);
      db.prepare('INSERT INTO reviews (inspection_id,user_id,decision,reason,created_at) VALUES (?,?,?,?,?)').run(row.id, req.user.id, decision, reason.trim(), now);
      db.prepare('INSERT INTO audit (inspection_id,actor,action,detail,created_at) VALUES (?,?,?,?,?)').run(row.id, req.user.name, decision === 'REVIEW' ? 'Escalated for further review' : `Human decision: ${decision}`, reason.trim(), now);
      db.exec('COMMIT'); res.json({ ok: true, version: version + 1 });
    } catch (e) { db.exec('ROLLBACK'); throw e; }
  });
  app.post('/api/simulate', (req, res) => res.status(201).json({ id: simulate(db) }));
  const dist = resolve(dirname(fileURLToPath(import.meta.url)), '../dist');
  app.use(express.static(dist));
  app.get('/{*path}', (req, res) => { if (req.path.startsWith('/api/')) return res.status(404).json({ error: 'Endpoint not found.' }); res.sendFile(resolve(dist, 'index.html')); });
  app.use((err, req, res, next) => { console.error(err.message); res.status(err.status || 500).json({ error: err.status === 400 ? 'Invalid request body.' : 'Unable to complete the request. Please try again.' }); });
  return { app, db };
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  const { app } = createApp(process.env.DB_PATH);
  const port = Number(process.env.PORT || 3001);
  app.listen(port, '127.0.0.1', () => console.log(`Axion demo: http://127.0.0.1:${port}`));
}
