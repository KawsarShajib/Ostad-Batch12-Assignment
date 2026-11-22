import { useState, useRef, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useStudents } from '../context/StudentContext';

function AddStudent() {
  const { addStudent, updateStudent } = useStudents();
  const navigate = useNavigate();
  const location = useLocation();
  const nameInputRef = useRef(null); // useRef example

  const editingStudent = location.state?.student || null;

  const [formData, setFormData] = useState({
    name: '',
    email: '',
    course: '',
    age: '',
    isActive: true,
  });

  const [errors, setErrors] = useState({});

  // Focus name input on mount (useRef + useEffect)
  useEffect(() => {
    nameInputRef.current?.focus();
  }, []);

  // Pre-fill form if editing
  useEffect(() => {
    if (editingStudent) {
      setFormData(editingStudent);
    }
  }, [editingStudent]);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }));
  };

  const validate = () => {
    const newErrors = {};
    if (!formData.name.trim()) newErrors.name = 'Name is required';
    if (!formData.email.trim()) newErrors.email = 'Email is required';
    else if (!/\S+@\S+\.\S+/.test(formData.email)) newErrors.email = 'Invalid email';
    if (!formData.course.trim()) newErrors.course = 'Course is required';
    if (!formData.age || formData.age < 16) newErrors.age = 'Age must be 16 or above';
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!validate()) return;

    if (editingStudent) {
      updateStudent({ ...formData, id: editingStudent.id });
    } else {
      addStudent(formData);
    }
    navigate('/students');
  };

  return (
    <div style={{ padding: '20px', maxWidth: '500px' }}>
      <h1>{editingStudent ? 'Edit Student' : 'Add New Student'}</h1>

      <form onSubmit={handleSubmit} style={styles.form}>
        <div style={styles.field}>
          <label>Name</label>
          <input
            ref={nameInputRef}
            type="text"
            name="name"
            value={formData.name}
            onChange={handleChange}
            style={styles.input}
          />
          {errors.name && <span style={styles.error}>{errors.name}</span>}
        </div>

        <div style={styles.field}>
          <label>Email</label>
          <input
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            style={styles.input}
          />
          {errors.email && <span style={styles.error}>{errors.email}</span>}
        </div>

        <div style={styles.field}>
          <label>Course</label>
          <input
            type="text"
            name="course"
            value={formData.course}
            onChange={handleChange}
            style={styles.input}
          />
          {errors.course && <span style={styles.error}>{errors.course}</span>}
        </div>

        <div style={styles.field}>
          <label>Age</label>
          <input
            type="number"
            name="age"
            value={formData.age}
            onChange={handleChange}
            style={styles.input}
          />
          {errors.age && <span style={styles.error}>{errors.age}</span>}
        </div>

        <div style={styles.field}>
          <label>
            <input
              type="checkbox"
              name="isActive"
              checked={formData.isActive}
              onChange={handleChange}
            />{' '}
            Active Student
          </label>
        </div>

        <button type="submit" style={styles.submitBtn}>
          {editingStudent ? 'Update Student' : 'Add Student'}
        </button>
      </form>
    </div>
  );
}

const styles = {
  form: { display: 'flex', flexDirection: 'column', gap: '16px' },
  field: { display: 'flex', flexDirection: 'column', gap: '4px' },
  input: { padding: '10px', borderRadius: '6px', border: '1px solid #ccc' },
  error: { color: 'red', fontSize: '0.875rem' },
  submitBtn: {
    backgroundColor: '#1e3a8a',
    color: 'white',
    padding: '12px',
    border: 'none',
    borderRadius: '6px',
    cursor: 'pointer',
    fontWeight: 'bold',
  },
};

export default AddStudent;