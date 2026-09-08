export const defects = [
  {
    id: 'AX-1001',
    title: 'Payment gateway timeout on retry flow',
    description: 'Customers see intermittent timeout errors when retrying the payment flow after 3 failed attempts.',
    severity: 'critical',
    status: 'open',
    team: 'Payments',
    assignee: 'A. Patil',
    createdAt: '2026-08-28T10:30:00Z',
    updatedAt: '2026-09-01T07:45:00Z',
    slaHours: 8,
    resolutionHours: 16
  },
  {
    id: 'AX-1002',
    title: 'Dashboard stats lag behind nightly ETL job',
    description: 'The defects summary cards display stale values until the ETL run completes.',
    severity: 'major',
    status: 'triaged',
    team: 'Data',
    assignee: 'J. Lee',
    createdAt: '2026-08-31T13:10:00Z',
    updatedAt: '2026-09-03T09:22:00Z',
    slaHours: 24,
    resolutionHours: 9
  },
  {
    id: 'AX-1003',
    title: 'User role mapping mismatch in portal',
    description: 'Managers are being assigned customer support permissions in the admin portal.',
    severity: 'major',
    status: 'in-progress',
    team: 'Identity',
    assignee: 'R. Shaw',
    createdAt: '2026-09-03T09:35:00Z',
    updatedAt: '2026-09-05T14:10:00Z',
    slaHours: 12,
    resolutionHours: 18
  },
  {
    id: 'AX-1004',
    title: 'CSV export missing incident IDs',
    description: 'Exported CSV files from the compliance report omit the incident identifier column.',
    severity: 'moderate',
    status: 'resolved',
    team: 'Reporting',
    assignee: 'M. Chen',
    createdAt: '2026-08-15T08:45:00Z',
    updatedAt: '2026-08-17T12:00:00Z',
    slaHours: 36,
    resolutionHours: 7
  },
  {
    id: 'AX-1005',
    title: 'Edge case in validation for expired tokens',
    description: 'Expired access tokens still appear valid for 10 minutes after expiry.',
    severity: 'critical',
    status: 'blocked',
    team: 'Security',
    assignee: 'D. Moore',
    createdAt: '2026-09-01T05:20:00Z',
    updatedAt: '2026-09-06T11:30:00Z',
    slaHours: 4,
    resolutionHours: 19
  },
  {
    id: 'AX-1006',
    title: 'Search suggestions omit inactive defects',
    description: 'Users cannot find recently closed defects from the search suggestions panel.',
    severity: 'minor',
    status: 'verified',
    team: 'UX',
    assignee: 'T. Singh',
    createdAt: '2026-08-20T15:15:00Z',
    updatedAt: '2026-09-04T08:05:00Z',
    slaHours: 48,
    resolutionHours: 11
  },
  {
    id: 'AX-1007',
    title: 'Webhook retries double-submit duplicate cards',
    description: 'Duplicate defect cards are created when a webhook retries after a timeout.',
    severity: 'critical',
    status: 'open',
    team: 'Integrations',
    assignee: 'K. Gomez',
    createdAt: '2026-09-06T01:10:00Z',
    updatedAt: '2026-09-06T06:55:00Z',
    slaHours: 6,
    resolutionHours: 13
  },
  {
    id: 'AX-1008',
    title: 'Audit report filters by wrong date format',
    description: 'The audit date range filter fails for reports using ISO week format.',
    severity: 'moderate',
    status: 'in-progress',
    team: 'Audit',
    assignee: 'S. Patel',
    createdAt: '2026-09-02T19:20:00Z',
    updatedAt: '2026-09-05T10:40:00Z',
    slaHours: 18,
    resolutionHours: 22
  }
];

const severityRank = { critical: 4, major: 3, moderate: 2, minor: 1 };

export function getDefects(filters = {}) {
  const normalizedFilters = {
    status: filters.status ? String(filters.status).toLowerCase() : undefined,
    severity: filters.severity ? String(filters.severity).toLowerCase() : undefined,
    team: filters.team ? String(filters.team).toLowerCase() : undefined,
    search: filters.search ? String(filters.search).trim() : undefined
  };

  return defects
    .filter((defect) => {
      if (normalizedFilters.status && defect.status !== normalizedFilters.status) {
        return false;
      }

      if (normalizedFilters.severity && defect.severity !== normalizedFilters.severity) {
        return false;
      }

      if (normalizedFilters.team && defect.team.toLowerCase() !== normalizedFilters.team) {
        return false;
      }

      if (normalizedFilters.search) {
        const haystack = `${defect.id} ${defect.title} ${defect.description} ${defect.assignee} ${defect.team}`.toLowerCase();
        if (!haystack.includes(normalizedFilters.search.toLowerCase())) {
          return false;
        }
      }

      return true;
    })
    .sort((left, right) => {
      const severityDelta = (severityRank[right.severity] ?? 0) - (severityRank[left.severity] ?? 0);
      if (severityDelta !== 0) {
        return severityDelta;
      }

      return new Date(right.updatedAt) - new Date(left.updatedAt);
    });
}

export function getDefectById(id) {
  return defects.find((defect) => defect.id.toLowerCase() === String(id).trim().toLowerCase()) ?? null;
}

export function getSummary(allDefects = defects) {
  const total = allDefects.length;
  const open = allDefects.filter((defect) => defect.status === 'open').length;
  const critical = allDefects.filter((defect) => defect.severity === 'critical').length;
  const breached = allDefects.filter((defect) => defect.resolutionHours > defect.slaHours).length;
  const completed = allDefects.filter((defect) => defect.status === 'resolved' || defect.status === 'verified').length;

  return {
    total,
    open,
    critical,
    breached,
    completed,
    active: total - completed
  };
}
