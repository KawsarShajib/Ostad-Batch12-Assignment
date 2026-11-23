import { Link } from 'react-router-dom';

function Navbar() {
  return (
    <nav style={styles.navbar}>
      <h2 style={{ margin: 0 }}>Student Management System</h2>
      <div style={styles.links}>
        <Link to="/" style={styles.link}>Dashboard</Link>
        <Link to="/students" style={styles.link}>Students (Local)</Link>
        <Link to="/add-student" style={styles.link}>Add Student</Link>
        <Link to="/api-students" style={styles.link}>Students (API)</Link>
        <Link to="/about" style={styles.link}>About</Link>
      </div>
    </nav>
  );
}

const styles = {
  navbar: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    backgroundColor: '#1e3a8a',
    color: 'white',
    padding: '12px 24px',
  },
  links: { display: 'flex', gap: '20px' },
  link: { color: 'white', textDecoration: 'none', fontWeight: '500' },
};

export default Navbar;