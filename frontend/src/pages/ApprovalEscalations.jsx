/**
 * Phase 9 - Approval Escalations Screen
 * Manager/Admin can escalate delayed approvals
 */

import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

import api from '../api/axios';
import { useAuth } from '../context/AuthContext';

import {
  StatusBadge,
  DataTable,
  FilterBar,
  ConfirmModal,
  ErrorMessage,
  PageHeader,
  LoadingSpinner,
  EmptyState,
} from '../components/UIComponents';

export default function ApprovalEscalations() {
  const { user } = useAuth();
  const navigate = useNavigate();

  const [escalations, setEscalations] = useState([]);
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const [showForm, setShowForm] = useState(false);
  const [showConfirm, setShowConfirm] = useState(null);

  const [filters, setFilters] = useState({
    status: '',
    level: '',
  });

  const [formData, setFormData] = useState({
    approval_id: '',
    escalated_to: '',
    reason: '',
    escalation_level: 1,
  });

  // FETCH DATA
  useEffect(() => {
    fetchData();
  }, []);

  async function fetchData() {

  try {

    setLoading(true);

    setError('');

    // =====================================
    // FETCH ESCALATIONS
    // =====================================

    const escRes =
      await api.get(
        '/approval-escalations/'
      );

    setEscalations(
      escRes.data || []
    );

    // =====================================
    // FETCH USERS
    // =====================================

    try {

      const usersRes =
        await api.get('/approval-escalations/users');

      setUsers(
        usersRes.data || []
      );

    } catch (userErr) {

      console.log(
        'Users API failed:',
        userErr
      );

      // keep page working
      setUsers([]);

    }

  } catch (err) {

    console.log(
      'Escalation fetch failed:',
      err
    );

    setError(
      err.response?.data?.detail ||
      'Failed to load escalations'
    );

  } finally {

    setLoading(false);

  }
}

  // FILTERS
  const filtered = escalations.filter((e) => {
    if (filters.status && e.status !== filters.status) return false;

    if (
      filters.level &&
      e.escalation_level !== parseInt(filters.level)
    )
      return false;

    return true;
  });

  // CREATE ESCALATION
  async function handleSubmit(e) {
    e.preventDefault();

    if (
      !formData.approval_id ||
      !formData.escalated_to ||
      !formData.reason.trim()
    ) {
      setError('All fields are required');
      return;
    }

    try {
      await api.post('/approval-escalations', formData);

      setShowForm(false);

      setFormData({
        approval_id: '',
        escalated_to: '',
        reason: '',
        escalation_level: 1,
      });

      fetchData();
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          'Failed to escalate approval'
      );
    }
  }

  // RESOLVE
  async function handleResolve(id) {
    try {
      await api.put(`/approval-escalations/${id}/resolve`);
      fetchData();
    } catch (err) {
      setError('Failed to resolve escalation');
    }
  }

  // CANCEL
  async function handleCancel(id) {
    try {
      await api.put(`/approval-escalations/${id}/cancel`);
      fetchData();
    } catch (err) {
      setError('Failed to cancel escalation');
    }
  }

  // ACCESS CONTROL
  if (!user || (user.role !== 'admin' && user.role !== 'manager')) {
    return (
      <div
        style={{
          textAlign: 'center',
          padding: '80px 20px',
        }}
      >
        <h2>Access Denied</h2>
        <p>
          Only managers and admins can access this page.
        </p>
      </div>
    );
  }

  // TABLE
  const tableColumns = [
    { key: 'id', label: 'ID' },
    { key: 'approval_id', label: 'Approval' },
    { key: 'escalated_from', label: 'From' },
    { key: 'escalated_to', label: 'To' },
    { key: 'reason', label: 'Reason' },
    { key: 'status', label: 'Status' },
    { key: 'escalated_at', label: 'Date' },
  ];

  const tableRows = filtered.map((e) => ({

  id: e.id || '—',

  approval_id:
    e.approval_id
      ? `#${e.approval_id}`
      : '—',

  escalated_from:
    e.escalated_from
      ? `User #${e.escalated_from}`
      : '—',

  escalated_to:
    e.escalated_to
      ? `User #${e.escalated_to}`
      : '—',

  reason:
    e.reason || '—',

  status: (
    <StatusBadge
      status={e.status || 'pending'}
    />
  ),

  escalated_at:
    e.escalated_at
      ? new Date(
          e.escalated_at
        ).toLocaleString()
      : '—',

  _raw: e,
}));

  return (
    <div
      style={{
        minHeight: '100vh',
        background: '#f3f4f6',
        padding: '30px',
      }}
    >
      {/* HEADER */}
      <div
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          marginBottom: '28px',
          gap: '20px',
          flexWrap: 'wrap',
        }}
      >
        {/* LEFT */}
        <PageHeader
          title="⚡ Approval Escalations"
          subtitle="Manage escalated approvals and reassignments"
          action={
            <button
              onClick={() => setShowForm(!showForm)}
              style={{
                background: '#4f46e5',
                color: '#fff',
                border: 'none',
                padding: '12px 22px',
                borderRadius: '10px',
                fontWeight: '600',
                cursor: 'pointer',
                fontSize: '14px',
                boxShadow:
                  '0 4px 12px rgba(79,70,229,0.25)',
                transition: '0.2s ease',
              }}
            >
              + Escalate Approval
            </button>
          }
        />

        {/* RIGHT */}
        <button
          onClick={() => navigate(-1)}
          style={{
            background: '#111827',
            color: '#fff',
            border: 'none',
            padding: '12px 22px',
            borderRadius: '10px',
            fontWeight: '600',
            cursor: 'pointer',
            fontSize: '14px',
            minWidth: '120px',
            boxShadow:
              '0 4px 12px rgba(0,0,0,0.18)',
          }}
        >
          ← Back
        </button>
      </div>

      <div
        style={{
          maxWidth: '1200px',
          margin: '0 auto',
        }}
      >
        {error && (
          <ErrorMessage
            message={error}
            onClose={() => setError('')}
          />
        )}

        {/* FORM */}
        {showForm && (
          <form
            onSubmit={handleSubmit}
            style={{
              background: '#fff',
              padding: '28px',
              borderRadius: '16px',
              marginBottom: '28px',
              boxShadow:
                '0 4px 20px rgba(0,0,0,0.06)',
            }}
          >
            <h3
              style={{
                marginBottom: '20px',
                fontSize: '20px',
                fontWeight: '700',
                color: '#111827',
              }}
            >
              Create New Escalation
            </h3>

            <div
              style={{
                display: 'grid',
                gridTemplateColumns:
                  'repeat(auto-fit, minmax(250px, 1fr))',
                gap: '18px',
                marginBottom: '20px',
              }}
            >
              {/* APPROVAL ID */}
              <div>
                <label
                  style={{
                    display: 'block',
                    marginBottom: '6px',
                    fontWeight: '600',
                  }}
                >
                  Approval ID *
                </label>

                <input
                  type="number"
                  value={formData.approval_id}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      approval_id: e.target.value,
                    })
                  }
                  placeholder="Enter approval ID"
                  style={{
                    width: '100%',
                    padding: '12px',
                    border: '1px solid #ddd',
                    borderRadius: '8px',
                  }}
                />
              </div>

              {/* USER */}
              <div>
                <label
                  style={{
                    display: 'block',
                    marginBottom: '6px',
                    fontWeight: '600',
                  }}
                >
                  Escalate To *
                </label>

                <select
                  value={formData.escalated_to}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      escalated_to: e.target.value,
                    })
                  }
                  style={{
                    width: '100%',
                    padding: '12px',
                    border: '1px solid #ddd',
                    borderRadius: '8px',
                  }}
                >
                  <option value="">
                    Select user
                  </option>

                  {users
                    .filter(
                      (u) =>
                        u.role === 'admin' ||
                        u.role === 'manager'
                    )
                    .map((u) => (
                      <option
                        key={u.id}
                        value={u.id}
                      >
                        {u.name} ({u.role})
                      </option>
                    ))}
                </select>
              </div>

              {/* LEVEL */}
              <div>
                <label
                  style={{
                    display: 'block',
                    marginBottom: '6px',
                    fontWeight: '600',
                  }}
                >
                  Escalation Level
                </label>

                <select
                  value={formData.escalation_level}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      escalation_level: parseInt(
                        e.target.value
                      ),
                    })
                  }
                  style={{
                    width: '100%',
                    padding: '12px',
                    border: '1px solid #ddd',
                    borderRadius: '8px',
                  }}
                >
                  <option value="1">
                    Level 1
                  </option>
                  <option value="2">
                    Level 2
                  </option>
                  <option value="3">
                    Level 3
                  </option>
                </select>
              </div>
            </div>

            {/* REASON */}
            <div style={{ marginBottom: '20px' }}>
              <label
                style={{
                  display: 'block',
                  marginBottom: '6px',
                  fontWeight: '600',
                }}
              >
                Reason *
              </label>

              <textarea
                value={formData.reason}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    reason: e.target.value,
                  })
                }
                placeholder="Explain why this approval is being escalated..."
                style={{
                  width: '100%',
                  padding: '12px',
                  border: '1px solid #ddd',
                  borderRadius: '8px',
                  minHeight: '100px',
                }}
              />
            </div>

            {/* BUTTONS */}
            <div
              style={{
                display: 'flex',
                gap: '12px',
              }}
            >
              <button
                type="submit"
                style={{
                  background: '#4f46e5',
                  color: '#fff',
                  border: 'none',
                  padding: '12px 20px',
                  borderRadius: '8px',
                  fontWeight: '600',
                  cursor: 'pointer',
                }}
              >
                Create Escalation
              </button>

              <button
                type="button"
                onClick={() =>
                  setShowForm(false)
                }
                style={{
                  background: '#e5e7eb',
                  border: 'none',
                  padding: '12px 20px',
                  borderRadius: '8px',
                  fontWeight: '600',
                  cursor: 'pointer',
                }}
              >
                Cancel
              </button>
            </div>
          </form>
        )}

        {/* FILTER */}
        <FilterBar
          filters={[
            {
              key: 'status',
              label: 'Status',
              type: 'select',
              value: filters.status,
              options: [
                {
                  label: 'Pending',
                  value: 'pending',
                },
                {
                  label: 'Resolved',
                  value: 'resolved',
                },
                {
                  label: 'Cancelled',
                  value: 'cancelled',
                },
              ],
            },
            {
              key: 'level',
              label: 'Escalation Level',
              type: 'select',
              value: filters.level,
              options: [
                {
                  label: 'Level 1',
                  value: '1',
                },
                {
                  label: 'Level 2',
                  value: '2',
                },
                {
                  label: 'Level 3',
                  value: '3',
                },
              ],
            },
          ]}
          onFilterChange={(key, value) =>
            setFilters({
              ...filters,
              [key]: value,
            })
          }
          onReset={() =>
            setFilters({
              status: '',
              level: '',
            })
          }
        />

        {/* TABLE */}
        {loading ? (
          <LoadingSpinner />
        ) : filtered.length === 0 ? (
          <EmptyState
            icon="📭"
            title="No Escalations"
            description="No approval escalations found."
          />
        ) : (
          <DataTable
            columns={tableColumns}
            rows={tableRows}
            loading={false}
            actions={(row) => (
              <div
                style={{
                  display: 'flex',
                  gap: '8px',
                  justifyContent: 'center',
                }}
              >
                {row._raw.status ===
                  'pending' && (
                  <>
                    <button
                      onClick={() =>
                        setShowConfirm({
                          action: 'resolve',
                          id: row.id,
                        })
                      }
                      style={{
                        background: '#dcfce7',
                        color: '#166534',
                        border: 'none',
                        padding: '8px 12px',
                        borderRadius: '6px',
                        cursor: 'pointer',
                        fontWeight: '600',
                      }}
                    >
                      Resolve
                    </button>

                    <button
                      onClick={() =>
                        setShowConfirm({
                          action: 'cancel',
                          id: row.id,
                        })
                      }
                      style={{
                        background: '#fee2e2',
                        color: '#991b1b',
                        border: 'none',
                        padding: '8px 12px',
                        borderRadius: '6px',
                        cursor: 'pointer',
                        fontWeight: '600',
                      }}
                    >
                      Cancel
                    </button>
                  </>
                )}
              </div>
            )}
          />
        )}

        {/* CONFIRM */}
        {showConfirm && (
          <ConfirmModal
            title={
              showConfirm.action ===
              'resolve'
                ? 'Resolve Escalation'
                : 'Cancel Escalation'
            }
            message={
              showConfirm.action ===
              'resolve'
                ? 'Mark this escalation as resolved?'
                : 'Cancel this escalation?'
            }
            danger={
              showConfirm.action === 'cancel'
            }
            onConfirm={() => {
              if (
                showConfirm.action ===
                'resolve'
              ) {
                handleResolve(showConfirm.id);
              } else {
                handleCancel(showConfirm.id);
              }

              setShowConfirm(null);
            }}
            onCancel={() =>
              setShowConfirm(null)
            }
          />
        )}
      </div>
    </div>
  );
}