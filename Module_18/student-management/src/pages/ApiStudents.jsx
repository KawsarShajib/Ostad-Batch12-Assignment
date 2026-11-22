import { useState } from 'react';
import StudentList from '../components/StudentList';
import { useStudentsQuery } from '../hooks/useStudentsQuery';

function ApiStudents() {
  const [searchTerm, setSearchTerm] = useState('');

  // React Query - fetching real data from public API
  const { data: students = [], isLoading, isError, error, refetch } = useStudentsQuery();

  // ========== LOADING STATE ==========
  if (isLoading) {
    return (
      <div style={{ padding: '40px', textAlign: 'center' }}>
        <h2>Loading students from API...</h2>
        <p>Please wait while we fetch the data.</p>
      </div>
    );
  }

  // ========== ERROR STATE ==========
  if (isError) {
    return (
      <div style={{ padding: '40px', textAlign: 'center' }}>
        <h2 style={{ color: 'red' }}>Failed to load data</h2>
        <p>{error.message}</p>
        <button
          onClick={() => refetch()}
          style={{
            marginTop: '16px',
            padding: '10px 20px',
            backgroundColor: '#1e3a8a',
            color: 'white',
            border: 'none',
            borderRadius: '6px',
            cursor: 'pointer',
          }}
        >
          Try Again
        </button>
      </div>
    );
  }

  // ========== SUCCESS STATE ==========
  return (
    <div style={{ padding: '20px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
        <h1>Students from Public API</h1>
        <button
          onClick={() => refetch()}
          style={{
            padding: '8px 16px',
            backgroundColor: '#3b82f6',
            color: 'white',
            border: 'none',
            borderRadius: '6px',
            cursor: 'pointer',
          }}
        >
          Refresh Data
        </button>
      </div>

      <p style={{ color: '#64748b', marginBottom: '20px' }}>
        Source : https://dummyjson.com/
        <br />
        This page fetches live data from DummyJSON API using React Query.
      </p>

      {/* Search */}
      <input
        type="text"
        placeholder="Search by name or email..."
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        style={{
          width: '100%',
          maxWidth: '400px',
          padding: '10px',
          marginBottom: '20px',
          borderRadius: '6px',
          border: '1px solid #ccc',
        }}
      />

      <StudentList
        students={students}
        searchTerm={searchTerm}
        // We don't pass onDelete / onEdit because this is read-only API data
        onDelete={() => alert('Delete is only available for local students')}
        onEdit={() => alert('Edit is only available for local students')}
      />
    </div>
  );
}

export default ApiStudents;