import StudentCard from './StudentCard';

function StudentList({ students, onDelete, onEdit, searchTerm }) {
  // Filter students (search functionality)
  const filteredStudents = students.filter((student) =>
    student.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    student.email.toLowerCase().includes(searchTerm.toLowerCase())
  );

  // Conditional rendering with if-else
  if (filteredStudents.length === 0) {
    return <p style={{ textAlign: 'center', marginTop: '40px' }}>No students found.</p>;
  }

  return (
    <div style={styles.grid}>
      {/* Render list using map() */}
      {filteredStudents.map((student) => (
        <StudentCard
          key={student.id}
          student={student}
          onDelete={onDelete}
          onEdit={onEdit}
        />
      ))}
    </div>
  );
}

const styles = {
  grid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))',
    gap: '20px',
    padding: '20px 0',
  },
};

export default StudentList;