import { useState } from 'react';
import { useStudents } from '../context/StudentContext';
import StudentList from '../components/StudentList';
import { useNavigate } from 'react-router-dom';

function Students() {
  const { students, deleteStudent, updateStudent } = useStudents();
  const [searchTerm, setSearchTerm] = useState('');
  const navigate = useNavigate();

  const handleEdit = (student) => {
    // For simplicity we navigate to add page with state (or implement edit modal later)
    navigate('/add-student', { state: { student } });
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1>Student List</h1>

      {/* Search input */}
      <input
        type="text"
        placeholder="Search by name or email..."
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        style={styles.search}
      />

      <StudentList
        students={students}
        onDelete={deleteStudent}
        onEdit={handleEdit}
        searchTerm={searchTerm}
      />
    </div>
  );
}

const styles = {
  search: {
    width: '100%',
    maxWidth: '400px',
    padding: '10px',
    marginBottom: '20px',
    borderRadius: '6px',
    border: '1px solid #ccc',
  },
};

export default Students;