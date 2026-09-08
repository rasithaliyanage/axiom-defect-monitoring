const summaryGrid = document.getElementById('summaryGrid');
const defectTableBody = document.getElementById('defectTableBody');
const statusFilter = document.getElementById('statusFilter');
const severityFilter = document.getElementById('severityFilter');
const searchInput = document.getElementById('searchInput');
const resultCount = document.getElementById('resultCount');

const summaryConfig = [
  { key: 'total', label: 'Total defects' },
  { key: 'open', label: 'Open' },
  { key: 'critical', label: 'Critical' },
  { key: 'breached', label: 'SLA breached' },
  { key: 'completed', label: 'Closed' }
];

function formatDate(dateValue) {
  return new Intl.DateTimeFormat('en', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  }).format(new Date(dateValue));
}

function renderSummary(summary) {
  summaryGrid.innerHTML = summaryConfig
    .map((item) => {
      const value = summary[item.key] ?? 0;
      return `
        <article class="summary-card">
          <div class="label">${item.label}</div>
          <div class="value">${value}</div>
          <div class="delta">Live snapshot</div>
        </article>
      `;
    })
    .join('');
}

function renderTable(defects) {
  if (!defects.length) {
    defectTableBody.innerHTML = `
      <tr>
        <td colspan="7" class="empty-state">No defects match the current filters.</td>
      </tr>
    `;
    resultCount.textContent = '0 results';
    return;
  }

  defectTableBody.innerHTML = defects
    .map(
      (defect) => `
        <tr>
          <td><strong>${defect.id}</strong></td>
          <td>${defect.title}</td>
          <td>${defect.team}</td>
          <td><span class="severity-pill severity-${defect.severity}">${defect.severity}</span></td>
          <td><span class="status-pill status-${defect.status.replace(/\s+/g, '-')}">${defect.status}</span></td>
          <td>${defect.assignee}</td>
          <td>${formatDate(defect.updatedAt)}</td>
        </tr>
      `
    )
    .join('');

  resultCount.textContent = `${defects.length} result${defects.length === 1 ? '' : 's'}`;
}

async function loadDefects() {
  const params = new URLSearchParams();
  const status = statusFilter.value;
  const severity = severityFilter.value;
  const search = searchInput.value.trim();

  if (status) params.set('status', status);
  if (severity) params.set('severity', severity);
  if (search) params.set('search', search);

  const response = await fetch(`/api/defects?${params.toString()}`);
  const payload = await response.json();

  renderSummary(payload.summary || { total: 0, open: 0, critical: 0, breached: 0, completed: 0 });
  renderTable(payload.defects || []);
}

statusFilter.addEventListener('change', loadDefects);
severityFilter.addEventListener('change', loadDefects);
searchInput.addEventListener('input', loadDefects);

(async function initialize() {
  const response = await fetch('/api/health');
  if (!response.ok) {
    throw new Error('Dashboard API is unavailable');
  }

  await loadDefects();
})();
