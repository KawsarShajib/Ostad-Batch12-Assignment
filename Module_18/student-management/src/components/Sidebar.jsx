import { Link } from 'react-router-dom';

function Sidebar() {
  return (
    <aside style={styles.sidebar}>
      <h3>Menu</h3>
      <ul style={styles.list}>
        <li><Link to="/" style={styles.link}>Dashboard</Link></li>
        <li><Link to="/students" style={styles.link}>Students (Local)</Link></li>
        <li><Link to="/add-student" style={styles.link}>Add New Student</Link></li>
        <li><Link to="/api-students" style={styles.link}>Students (API)</Link></li>
        <li><Link to="/about" style={styles.link}>About</Link></li>
      </ul>
    </aside>
  );
}

const styles = {
  sidebar: {
    width: '220px',
    backgroundColor: '#f1f5f9',
    padding: '20px',
    minHeight: 'calc(100vh - 60px)',
  },
  list: { listStyle: 'none', padding: 0 },
  link: { textDecoration: 'none', color: '#1e3a8a', display: 'block', padding: '8px 0' },
};

export default Sidebar;