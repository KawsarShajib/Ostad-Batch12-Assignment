import { useQuery } from '@tanstack/react-query';

const fetchStudents = async () => {
  const res = await fetch('https://dummyjson.com/users?limit=20');
  if (!res.ok) throw new Error('Failed to fetch students');
  const data = await res.json();
  // Map to our student shape
  return data.users.map((user) => ({
    id: user.id,
    name: `${user.firstName} ${user.lastName}`,
    email: user.email,
    course: user.university || 'General Studies',
    age: user.age,
    isActive: true,
  }));
};

export function useStudentsQuery() {
  return useQuery({
    queryKey: ['students'],
    queryFn: fetchStudents,
  });
}