function StudentCard({ student, onDelete, onEdit }) {
  // Conditional rendering with ternary
  const statusBadge = student.isActive ? (
    <span style={{ color: 'green' }}>Active</span>
  ) : (
    <span style={{ color: 'red' }}>Inactive</span>
  );

  
  // Confirmation before delete
  const handleDelete = () => {
    const confirmed = window.confirm(
      `Are you sure you want to delete "${student.name}"?\nThis action cannot be undone.`
    );

    if (confirmed) {
      onDelete(student.id);
    }
  };

  
  return (
    <div style={styles.card}>
      <h3>{student.name}</h3>
      <p><strong>Email:</strong> {student.email}</p>
      <p><strong>Course:</strong> {student.course}</p>
      <p><strong>Age:</strong> {student.age}</p>
      <p><strong>Status:</strong> {statusBadge}</p>

      <div style={styles.buttons}>
        <button onClick={() => onEdit(student)} style={styles.editBtn}>
          Edit
        </button>
        <button onClick={handleDelete} style={styles.deleteBtn}>
          Delete
        </button>
      </div>
    </div>
  );
}

const styles = {
  card: {
    border: '1px solid #ddd',
    borderRadius: '8px',
    padding: '16px',
    backgroundColor: 'white',
    boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
  },
  buttons: { display: 'flex', gap: '10px', marginTop: '12px' },
  editBtn: { backgroundColor: '#3b82f6', color: 'white', border: 'none', padding: '6px 12px', borderRadius: '4px', cursor: 'pointer', fontSize: '14px', },
  deleteBtn: { backgroundColor: '#ef4444', color: 'white', border: 'none', padding: '6px 12px', borderRadius: '4px', cursor: 'pointer',fontSize: '14px', },
};

export default StudentCard;