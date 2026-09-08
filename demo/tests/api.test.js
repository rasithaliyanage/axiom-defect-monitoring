import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { createApp } from '../server/index.js';

test('Persistent inspection workflow, access checks and conflict protection', async () => {
  const folder = mkdtempSync(join(tmpdir(), 'axion-test-'));
  const filename = join(folder, 'test.sqlite');
  const { app, db } = createApp(filename);
  const server = app.listen(0, '127.0.0.1');
  await new Promise(resolve => server.once('listening', resolve));
  const base = `http://127.0.0.1:${server.address().port}/api`;
  let cookie = '';
  const request = (url, body, headers = {}) => fetch(base + url, { method: body ? 'POST' : 'GET', headers: { 'Content-Type': 'application/json', cookie, ...headers }, ...(body ? { body: JSON.stringify(body) } : {}) });
  try {
    assert.equal((await request('/workspace')).status, 401);
    assert.equal((await request('/login', { email:'inspector@axion.demo', password:'wrong' })).status, 401);
    const login = await request('/login', { email:'inspector@axion.demo', password:'Demo@123' });
    assert.equal(login.status, 200); cookie = login.headers.get('set-cookie').split(';')[0];
    assert.match(login.headers.get('set-cookie'), /HttpOnly/);
    const workspace = await (await request('/workspace')).json();
    assert.equal(workspace.lines.length, 4); assert.equal(workspace.inspections.length, 181);
    const board = workspace.inspections.find(i=>i.status==='REVIEW');
    const initial = await (await request(`/inspections/${board.id}`)).json();
    assert.ok(initial.defects.length >= 2);
    assert.equal((await request(`/inspections/${board.id}/review`,{decision:'PASS',reason:'short',version:1})).status,400);
    assert.equal((await request(`/inspections/${board.id}/review`,{decision:'PASS',reason:'Manual visual verification completed.',version:1},{Origin:'https://other.example'})).status,403);
    const saved = await request(`/inspections/${board.id}/review`,{decision:'FAIL',reason:'Confirmed bridge between the power controller pins.',version:initial.version});
    assert.equal(saved.status,200);
    assert.equal((await request(`/inspections/${board.id}/review`,{decision:'PASS',reason:'Stale review must not overwrite.',version:initial.version})).status,409);
    const after = await (await request(`/inspections/${board.id}`)).json();
    assert.equal(after.status,'FAIL'); assert.equal(after.initial_status,'REVIEW'); assert.equal(after.reviews.length,1); assert.equal(after.audit.length,2);
    const unavailable=workspace.inspections.find(i=>i.status==='UNAVAILABLE');
    assert.equal((await request(`/inspections/${unavailable.id}/review`,{decision:'PASS',reason:'Cannot pass unavailable evidence.',version:1})).status,400);
    assert.equal((await request('/simulate',{})).status,201);
    assert.equal((await (await request('/workspace')).json()).inspections.length,182);
    assert.equal((await request('/inspections/missing')).status,404);
    await request('/logout',{}); assert.equal((await request('/workspace')).status,401);
    await new Promise(resolve=>server.close(resolve)); db.close();
    const reopened=createApp(filename);
    assert.equal(reopened.db.prepare('SELECT status FROM inspections WHERE id=?').get(board.id).status,'FAIL');
    assert.equal(reopened.db.prepare('SELECT COUNT(*) AS n FROM inspections').get().n,182);
    reopened.db.close();
  } finally {
    if (server.listening) await new Promise(resolve=>server.close(resolve));
    try { db.close(); } catch {}
    rmSync(folder, { recursive:true, force:true });
  }
});
