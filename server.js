import http from 'node:http';
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { getDefectById, getDefects, getSummary } from './src/defectData.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const publicDir = path.join(__dirname, 'public');
const PORT = Number(process.env.PORT || 3000);

function parseUrl(urlString) {
  const url = new URL(urlString, 'http://localhost');
  return {
    pathname: url.pathname,
    searchParams: url.searchParams
  };
}

function sendJson(response, statusCode, payload) {
  response.writeHead(statusCode, {
    'Content-Type': 'application/json; charset=utf-8',
    'Cache-Control': 'no-store'
  });
  response.end(JSON.stringify(payload));
}

async function serveStaticAsset(response, assetPath) {
  try {
    const resolvedPath = path.join(publicDir, assetPath);
    const normalizedPath = path.normalize(resolvedPath);

    if (!normalizedPath.startsWith(publicDir)) {
      throw new Error('Invalid path');
    }

    const file = await fs.readFile(normalizedPath);
    const extension = path.extname(normalizedPath).toLowerCase();
    const contentTypes = {
      '.html': 'text/html; charset=utf-8',
      '.css': 'text/css; charset=utf-8',
      '.js': 'application/javascript; charset=utf-8',
      '.json': 'application/json; charset=utf-8',
      '.svg': 'image/svg+xml'
    };

    response.writeHead(200, {
      'Content-Type': contentTypes[extension] || 'application/octet-stream',
      'Cache-Control': 'no-store'
    });
    response.end(file);
  } catch (error) {
    response.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
    response.end('Not found');
  }
}

export function createAppHandler() {
  return async function handler(request, response) {
    const { pathname, searchParams } = parseUrl(request.url || '/');

    if (pathname === '/api/health') {
      sendJson(response, 200, { status: 'ok', service: 'axion-defect-monitoring' });
      return;
    }

    if (pathname === '/api/defects') {
      const filters = {
        status: searchParams.get('status') || undefined,
        severity: searchParams.get('severity') || undefined,
        team: searchParams.get('team') || undefined,
        search: searchParams.get('search') || undefined
      };

      const filteredDefects = getDefects(filters);
      const summary = getSummary(filteredDefects);
      sendJson(response, 200, { summary, defects: filteredDefects });
      return;
    }

    if (pathname.startsWith('/api/defects/')) {
      const id = pathname.split('/').at(-1);
      const defect = getDefectById(id);
      if (!defect) {
        sendJson(response, 404, { error: 'Defect not found' });
        return;
      }

      sendJson(response, 200, defect);
      return;
    }

    const assetPath = pathname === '/' ? '/index.html' : pathname;
    await serveStaticAsset(response, assetPath.replace(/^\//, ''));
  };
}

const app = createAppHandler();

const server = http.createServer((request, response) => {
  app(request, response).catch((error) => {
    console.error(error);
    sendJson(response, 500, { error: 'Unexpected server error' });
  });
});

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  server.listen(PORT, () => {
    console.log(`Dashboard server is running on http://localhost:${PORT}`);
  });
}

export { server };
