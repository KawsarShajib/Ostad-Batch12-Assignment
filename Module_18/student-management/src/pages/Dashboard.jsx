import { useStudents } from '../context/StudentContext';
import { Link } from 'react-router-dom';

function Dashboard() {
  const { students } = useStudents();

  const totalStudents = students.length;
  const activeStudents = students.filter((s) => s.isActive).length;

  return (
    <div style={{ padding: '20px' }}>
      <h1>Dashboard</h1>
      <div style={styles.stats}>
        <div style={styles.card}>
          <h3>Total Students</h3>
          <p style={styles.number}>{totalStudents}</p>
        </div>
        <div style={styles.card}>
          <h3>Active Students</h3>
          <p style={styles.number}>{activeStudents}</p>
        </div>
      </div>

      <Link to="/students" style={styles.button}>
        View All Students
      </Link>
    </div>
  );
}

const styles = {
  stats: { display: 'flex', gap: '20px', margin: '20px 0' },
  card: {
    backgroundColor: '#eff6ff',
    padding: '20px',
    borderRadius: '8px',
    minWidth: '180px',
    textAlign: 'center',
  },
  number: { fontSize: '2rem', fontWeight: 'bold', color: '#1e3a8a' },
  button: {
    display: 'inline-block',
    marginTop: '20px',
    backgroundColor: '#1e3a8a',
    color: 'white',
    padding: '10px 20px',
    borderRadius: '6px',
    textDecoration: 'none',
  },
};

export default Dashboard;