import { DatabaseSync } from 'node:sqlite';
import { mkdirSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { randomBytes, scryptSync } from 'node:crypto';

export function openDatabase(filename = resolve('data/demo.sqlite')) {
  mkdirSync(dirname(filename), { recursive: true });
  const db = new DatabaseSync(filename);
  db.exec(`PRAGMA foreign_keys = ON; PRAGMA journal_mode = WAL;
    CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, email TEXT UNIQUE, name TEXT, role TEXT, salt TEXT, password TEXT);
    CREATE TABLE IF NOT EXISTS sessions (token TEXT PRIMARY KEY, user_id INTEGER REFERENCES users(id), expires INTEGER);
    CREATE TABLE IF NOT EXISTS lines (id TEXT PRIMARY KEY, name TEXT, product TEXT, status TEXT, target INTEGER, camera TEXT);
    CREATE TABLE IF NOT EXISTS inspections (id TEXT PRIMARY KEY, board_id TEXT, line_id TEXT REFERENCES lines(id), product TEXT, batch TEXT, captured_at TEXT, initial_status TEXT, status TEXT, confidence REAL, latency INTEGER, model TEXT, recipe TEXT, version INTEGER DEFAULT 1, claimed_by INTEGER REFERENCES users(id));
    CREATE TABLE IF NOT EXISTS defects (id INTEGER PRIMARY KEY, inspection_id TEXT REFERENCES inspections(id), type TEXT, severity TEXT, confidence REAL, x INTEGER, y INTEGER, width INTEGER, height INTEGER, component TEXT);
    CREATE TABLE IF NOT EXISTS reviews (id INTEGER PRIMARY KEY, inspection_id TEXT REFERENCES inspections(id), user_id INTEGER REFERENCES users(id), decision TEXT, reason TEXT, created_at TEXT);
    CREATE TABLE IF NOT EXISTS audit (id INTEGER PRIMARY KEY, inspection_id TEXT REFERENCES inspections(id), actor TEXT, action TEXT, detail TEXT, created_at TEXT);
    CREATE INDEX IF NOT EXISTS inspection_date ON inspections(captured_at);
    CREATE INDEX IF NOT EXISTS defect_inspection ON defects(inspection_id);`);
  if (!db.prepare('SELECT id FROM users LIMIT 1').get()) {
    const salt = randomBytes(16).toString('hex');
    db.prepare('INSERT INTO users VALUES (1,?,?,?,?,?)').run('inspector@axion.demo', 'Maya Chen', 'Quality inspector', salt, scryptSync('Demo@123', salt, 64).toString('hex'));
  }
  if (!db.prepare('SELECT id FROM lines LIMIT 1').get()) seed(db);
  return db;
}

function addInspection(db, index, time, forced = false) {
  const id = `INS-${String(index).padStart(5, '0')}`;
  const line = forced ? 'L2' : `L${index % 4 + 1}`;
  const status = forced ? 'REVIEW' : index % 17 === 0 ? 'UNAVAILABLE' : index % 9 === 0 ? 'FAIL' : index % 7 === 0 ? 'REVIEW' : 'PASS';
  const confidence = status === 'UNAVAILABLE' ? null : status === 'REVIEW' ? 71 + index % 15 : 94 + (index % 50) / 10;
  db.prepare('INSERT INTO inspections (id,board_id,line_id,product,batch,captured_at,initial_status,status,confidence,latency,model,recipe) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)')
    .run(id, `AX-MB-${String(index + 8400).padStart(6, '0')}`, line, line === 'L3' ? 'ATX Pro / Rev C' : 'ATX Core / Rev B', `BATCH-${line}-2409`, time, status, status, confidence, 68 + index % 43, 'Vision 2.4.1 · demo', 'QC-ATX-07 / v3');
  if (status === 'FAIL' || status === 'REVIEW') {
    const defect = db.prepare('INSERT INTO defects (inspection_id,type,severity,confidence,x,y,width,height,component) VALUES (?,?,?,?,?,?,?,?,?)');
    defect.run(id, 'Solder bridge', 'Critical', forced ? 82.4 : confidence, 424, 270, 80, 65, 'U14 · power controller');
    if (index % 2 === 0 || forced) defect.run(id, 'Missing component', 'Major', 76.8, 157, 386, 78, 56, 'C32 · capacitor');
    if (index % 3 === 0) defect.run(id, 'Misalignment', 'Major', 88.1, 454, 130, 80, 90, 'J08 · memory connector');
  }
  db.prepare('INSERT INTO audit (inspection_id,actor,action,detail,created_at) VALUES (?,?,?,?,?)').run(id, 'Inspection service', 'Inspection recorded', status === 'UNAVAILABLE' ? 'Required camera view unavailable. No PASS decision issued.' : `${status} · model Vision 2.4.1 · recipe QC-ATX-07/v3`, time);
  return id;
}

function seed(db) {
  db.exec('BEGIN');
  try {
  const insert = db.prepare('INSERT INTO lines VALUES (?,?,?,?,?,?)');
  insert.run('L1', 'Assembly line 01', 'ATX Core', 'RUNNING', 32, 'CAM-01');
  insert.run('L2', 'Assembly line 02', 'ATX Core', 'ATTENTION', 32, 'CAM-02');
  insert.run('L3', 'Assembly line 03', 'ATX Pro', 'RUNNING', 28, 'CAM-03');
  insert.run('L4', 'Assembly line 04', 'ATX Core', 'IDLE', 32, 'CAM-04');
    const now = Date.now();
    for (let i = 1; i <= 180; i++) addInspection(db, i, new Date(now - (181 - i) * 150000).toISOString());
    addInspection(db, 181, new Date(now).toISOString(), true);
    db.exec('COMMIT');
  } catch (error) { db.exec('ROLLBACK'); throw error; }
}

export function simulate(db) {
  const next = Number(db.prepare('SELECT MAX(CAST(SUBSTR(id,5) AS INTEGER)) AS n FROM inspections').get().n) + 1;
  db.exec('BEGIN');
  try { const id = addInspection(db, next, new Date().toISOString(), true); db.exec('COMMIT'); return id; }
  catch (e) { db.exec('ROLLBACK'); throw e; }
}
