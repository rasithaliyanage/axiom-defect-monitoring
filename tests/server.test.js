import test from 'node:test';
import assert from 'node:assert/strict';
import { createAppHandler } from '../server.js';
import { getDefects, getSummary } from '../src/defectData.js';

function toResponseText(response) {
  return new Promise((resolve, reject) => {
    let body = '';
    response.on('data', (chunk) => {
      body += chunk.toString();
    });
    response.on('end', () => resolve(body));
    response.on('error', reject);
  });
}

test('getDefects filters by status and severity', () => {
  const filtered = getDefects({ status: 'open', severity: 'critical' });
  assert.deepEqual(filtered.map((item) => item.id), ['AX-1007', 'AX-1001']);
});

test('getSummary counts active and critical defects', () => {
  const summary = getSummary(getDefects({ status: 'open' }));
  assert.equal(summary.total, 2);
  assert.equal(summary.open, 2);
  assert.equal(summary.critical, 2);
});

test('API exposes health and defect list endpoints', async () => {
  const handler = createAppHandler();

  const healthResponse = {
    writeHead: (statusCode, headers) => {
      healthResponse.statusCode = statusCode;
      healthResponse.headers = headers;
    },
    end: (payload) => {
      healthResponse.body = payload;
    }
  };

  await handler({ url: '/api/health' }, healthResponse);
  assert.equal(healthResponse.statusCode, 200);
  assert.match(healthResponse.body, /"status":"ok"/);

  const defectsResponse = {
    writeHead: (statusCode, headers) => {
      defectsResponse.statusCode = statusCode;
      defectsResponse.headers = headers;
    },
    end: (payload) => {
      defectsResponse.body = payload;
    }
  };

  await handler({ url: '/api/defects?status=open&severity=critical' }, defectsResponse);
  assert.equal(defectsResponse.statusCode, 200);
  const defectPayload = JSON.parse(defectsResponse.body);
  assert.equal(defectPayload.defects.length, 2);
  assert.deepEqual(defectPayload.summary.open, 2);
});

test('API serves the dashboard index page', async () => {
  const handler = createAppHandler();
  const response = {
    writeHead: (statusCode, headers) => {
      response.statusCode = statusCode;
      response.headers = headers;
    },
    end: (payload) => {
      response.body = payload;
    }
  };

  await handler({ url: '/' }, response);
  assert.equal(response.statusCode, 200);
  assert.match(String(response.body), /Defect Monitoring Dashboard/);
});
