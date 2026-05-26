/**
 * Phase 9 - Approval Delegations Screen
 * Managers can delegate approval responsibility to another user
 */

import React, { useEffect, useState } from 'react';

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

export default function ApprovalDelegations() {
    useAuth();
  const [delegations, setDelegations] = useState([]);
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showForm, setShowForm] = useState(false);
  const [showConfirm, setShowConfirm] = useState(null);
  const [filters, setFilters] = useState({ status: '' });

  const [formData, setFormData] = useState({
    delegatee_id: '',
    start_date: '',
    end_date: '',
    reason: '',
  });

  useEffect(() => {
    fetchData();
  }, []);

  async function fetchData() {
    try {
      setLoading(true);
      const [delRes, usersRes] = await Promise.all([
        api.get('/approval-delegations/me'),
        api.get('/users/'),
      ]);
      setDelegations(delRes.data || []);
      setUsers(usersRes.data || []);
    } catch (err) {
      setError('Failed to load delegations');
    } finally {
      setLoading(false);
    }
  }

  // Filter delegations
  const filtered = delegations.filter((d) => {
    if (filters.status && d.status !== filters.status) return false;
    return true;
  });

  // Validate form
  function validateForm() {
    if (!formData.delegatee_id) {
      setError('Please select a delegatee');
      return false;
    }
    if (!formData.start_date) {
      setError('Please select a start date');
      return false;
    }
    if (!formData.end_date) {
      setError('Please select an end date');
      return false;
    }
    if (new Date(formData.end_date) <= new Date(formData.start_date)) {
      setError('End date must be after start date');
      return false;
    }
    if (!formData.reason.trim()) {
      setError('Please provide a reason');
      return false;
    }
    return true;
  }

  // Submit delegation
  async function handleSubmit(e) {
    e.preventDefault();
    if (!validateForm()) return;

    try {
      await api.post('/approval-delegations', formData);
      setShowForm(false);
      setFormData({
        delegatee_id: '',
        start_date: '',
        end_date: '',
        reason: '',
      });
      setError('');
      fetchData();
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to create delegation');
    }
  }

  // Cancel delegation
  async function handleCancel(id) {
    try {
      await api.put(`/approval-delegations/${id}/cancel`);
      fetchData();
      setShowConfirm(null);
    } catch (err) {
      setError('Failed to cancel delegation');
    }
  }

  const tableColumns = [
    { key: 'delegatee', label: 'Delegated To' },
    { key: 'start_date', label: 'Start Date' },
    { key: 'end_date', label: 'End Date' },
    { key: 'reason', label: 'Reason' },
    { key: 'status', label: 'Status' },
  ];

  const tableRows = delegations.map((d) => ({
    delegatee: `User #${d.delegatee_id}`,
    start_date: new Date(d.start_date).toLocaleDateString(),
    end_date: new Date(d.end_date).toLocaleDateString(),
    reason: d.reason,
    status: <StatusBadge status={d.status === 'Active' ? 'active' : 'cancelled'} />,
    _raw: d,
  }));

  return (
    <div style={{ minHeight: '100vh', background: '#f0f2f5', padding: '24px' }}>
      <PageHeader
        title="🔄 Approval Delegations"
        subtitle="Delegate your approval responsibility to team members"
        action={
          <button
            onClick={() => setShowForm(!showForm)}
            style={{
              background: '#4f46e5',
              color: '#fff',
              border: 'none',
              padding: '10px 20px',
              borderRadius: '8px',
              fontWeight: '600',
              cursor: 'pointer',
            }}
          >
            + New Delegation
          </button>
        }
      />

      <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
        {error && <ErrorMessage message={error} onClose={() => setError('')} />}

        {/* Delegation Form */}
        {showForm && (
          <form
            onSubmit={handleSubmit}
            style={{
              background: '#fff',
              padding: '28px',
              borderRadius: '12px',
              marginBottom: '28px',
              boxShadow: '0 2px 12px rgba(0,0,0,0.07)',
            }}
          >
            <h3 style={{ margin: '0 0 20px', fontSize: '18px', fontWeight: '700' }}>
              Create New Delegation
            </h3>

            <div
              style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
                gap: '16px',
                marginBottom: '20px',
              }}
            >
              <div>
                <label style={{ display: 'block', marginBottom: '6px', fontWeight: '600', fontSize: '13px' }}>
                  Delegatee (Manager) *
                </label>
                <select
                  value={formData.delegatee_id}
                  onChange={(e) => setFormData({ ...formData, delegatee_id: e.target.value })}
                  style={{
                    width: '100%',
                    padding: '10px 12px',
                    border: '1px solid #ddd',
                    borderRadius: '8px',
                  }}
                >
                  <option value="">Select user</option>
                  {users
                    .filter((u) => u.role === 'admin' || u.role === 'manager')
                    .map((u) => (
                      <option key={u.id} value={u.id}>
                        {u.name} ({u.role})
                      </option>
                    ))}
                </select>
              </div>

              <div>
                <label style={{ display: 'block', marginBottom: '6px', fontWeight: '600', fontSize: '13px' }}>
                  Start Date *
                </label>
                <input
                  type="date"
                  value={formData.start_date}
                  onChange={(e) => setFormData({ ...formData, start_date: e.target.value })}
                  style={{
                    width: '100%',
                    padding: '10px 12px',
                    border: '1px solid #ddd',
                    borderRadius: '8px',
                  }}
                />
              </div>

              <div>
                <label style={{ display: 'block', marginBottom: '6px', fontWeight: '600', fontSize: '13px' }}>
                  End Date *
                </label>
                <input
                  type="date"
                  value={formData.end_date}
                  onChange={(e) => setFormData({ ...formData, end_date: e.target.value })}
                  style={{
                    width: '100%',
                    padding: '10px 12px',
                    border: '1px solid #ddd',
                    borderRadius: '8px',
                  }}
                />
              </div>
            </div>

            <div style={{ marginBottom: '20px' }}>
              <label style={{ display: 'block', marginBottom: '6px', fontWeight: '600', fontSize: '13px' }}>
                Reason for Delegation *
              </label>
              <textarea
                value={formData.reason}
                onChange={(e) => setFormData({ ...formData, reason: e.target.value })}
                placeholder="e.g., On leave, temporary unavailability..."
                style={{
                  width: '100%',
                  padding: '10px 12px',
                  border: '1px solid #ddd',
                  borderRadius: '8px',
                  minHeight: '80px',
                  fontFamily: 'sans-serif',
                }}
              />
            </div>

            <div style={{ display: 'flex', gap: '12px' }}>
              <button
                type="submit"
                style={{
                  background: '#4f46e5',
                  color: '#fff',
                  border: 'none',
                  padding: '10px 20px',
                  borderRadius: '8px',
                  fontWeight: '600',
                  cursor: 'pointer',
                }}
              >
                Create Delegation
              </button>
              <button
                type="button"
                onClick={() => setShowForm(false)}
                style={{
                  background: '#f0f0f0',
                  border: 'none',
                  padding: '10px 20px',
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

        {/* Filters */}
        <FilterBar
          filters={[
            {
              key: 'status',
              label: 'Status',
              type: 'select',
              value: filters.status,
              options: [
                { label: 'Active', value: 'Active' },
                { label: 'Cancelled', value: 'Cancelled' },
              ],
            },
          ]}
          onFilterChange={(key, value) => setFilters({ ...filters, [key]: value })}
          onReset={() => setFilters({ status: '' })}
        />

        {/* Table */}
        {loading ? (
          <LoadingSpinner />
        ) : filtered.length === 0 ? (
          <EmptyState icon="🔄" title="No Delegations" description="No active delegations. Create one to delegate your approvals." />
        ) : (
          <DataTable
            columns={tableColumns}
            rows={tableRows}
            loading={false}
            actions={(row) => (
              <div style={{ display: 'flex', gap: '8px', justifyContent: 'center' }}>
                {row._raw.is_active && (
                  <button
                    onClick={() => setShowConfirm({ id: row._raw.id })}
                    style={{
                      background: '#fde8e8',
                      color: '#c0392b',
                      border: 'none',
                      padding: '6px 12px',
                      borderRadius: '6px',
                      fontSize: '12px',
                      fontWeight: '600',
                      cursor: 'pointer',
                    }}
                  >
                    Cancel
                  </button>
                )}
              </div>
            )}
          />
        )}

        {/* Confirm Modal */}
        {showConfirm && (
          <ConfirmModal
            title="Cancel Delegation"
            message="Are you sure you want to cancel this delegation? Approvals will no longer be delegated to this user."
            danger={true}
            onConfirm={() => handleCancel(showConfirm.id)}
            onCancel={() => setShowConfirm(null)}
          />
        )}
      </div>
    </div>
  );
}