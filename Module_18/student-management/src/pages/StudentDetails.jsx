import { useParams, Link } from 'react-router-dom';
import { useStudents } from '../context/StudentContext';

function StudentDetails() {
  const { id } = useParams();
  const { students } = useStudents();

  const student = students.find((s) => s.id === Number(id));

  if (!student) {
    return (
      <div style={{ padding: '20px' }}>
        <h2>Student not found</h2>
        <Link to="/students">Back to list</Link>
      </div>
    );
  }

  return (
    <div style={{ padding: '20px' }}>
      <h1>Student Details</h1>
      <div style={styles.card}>
        <p><strong>Name:</strong> {student.name}</p>
        <p><strong>Email:</strong> {student.email}</p>
        <p><strong>Course:</strong> {student.course}</p>
        <p><strong>Age:</strong> {student.age}</p>
        <p><strong>Status:</strong> {student.isActive ? 'Active' : 'Inactive'}</p>
      </div>
      <Link to="/students" style={styles.back}>← Back to Students</Link>
    </div>
  );
}

const styles = {
  card: {
    backgroundColor: '#f8fafc',
    padding: '24px',
    borderRadius: '8px',
    maxWidth: '500px',
    marginTop: '20px',
  },
  back: { display: 'inline-block', marginTop: '20px', color: '#1e3a8a' },
};

export default StudentDetails;