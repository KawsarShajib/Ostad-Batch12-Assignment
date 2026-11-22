import { createContext, useContext, useState, useEffect } from 'react';

const StudentContext = createContext();

export function StudentProvider({ children }) {
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Load initial data (will be replaced by React Query later)
  useEffect(() => {
    // This will be enhanced with React Query in Task 5
    const initialStudents = [
      { id: 1, name: 'Kawsar Ahmed', email: 'kawsar@gmail.com', course: 'Computer Science', age: 40, isActive: true },
      { id: 2, name: 'Sidratul Muntaha', email: 'arin@yahoo.com', course: 'Mathematics', age: 22, isActive: true },
      { id: 3, name: 'Safwan Ahmed', email: 'safwan@hotmail.com', course: 'Physics', age: 21, isActive: false },
    ];
    setStudents(initialStudents);
    setLoading(false);
  }, []);

  // Add student (immutability)
  const addStudent = (newStudent) => {
    setStudents((prev) => [...prev, { ...newStudent, id: Date.now() }]);
  };

  // Delete student (immutability)
  const deleteStudent = (id) => {
    setStudents((prev) => prev.filter((s) => s.id !== id));
  };

  // Update student (immutability)
  const updateStudent = (updatedStudent) => {
    setStudents((prev) =>
      prev.map((s) => (s.id === updatedStudent.id ? updatedStudent : s))
    );
  };

  return (
    <StudentContext.Provider
      value={{
        students,
        loading,
        error,
        addStudent,
        deleteStudent,
        updateStudent,
        setStudents,
      }}
    >
      {children}
    </StudentContext.Provider>
  );
}

export function useStudents() {
  const context = useContext(StudentContext);
  if (!context) {
    throw new Error('useStudents must be used within StudentProvider');
  }
  return context;
}