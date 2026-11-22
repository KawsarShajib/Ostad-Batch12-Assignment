# Student Management System

A complete React application built with Vite to practice modern React concepts.

## Features
- Reusable components (Navbar, Sidebar, StudentCard, StudentList, Footer)
- Props, Conditional Rendering, map()
- State Management with useState + Context API
- Form handling with validation and useRef
- React Router (Dashboard, Students, Student Details, Add Student, About)
- Search functionality
- Add / Edit / Delete students
- Ready for React Query API integration

## Project Structure

   student-management-dashboard/
   ├── public/
   ├── src/
   │   ├── components/
   │   │   ├── Navbar.jsx
   │   │   ├── Sidebar.jsx
   │   │   ├── StudentCard.jsx
   │   │   ├── StudentList.jsx
   │   │   └── Footer.jsx
   │   ├── pages/
   │   │   ├── Dashboard.jsx
   │   │   ├── Students.jsx
   │   │   ├── StudentDetails.jsx
   │   │   ├── AddStudent.jsx
   │   │   └── About.jsx
   │   ├── context/
   │   │   └── StudentContext.jsx
   │   ├── App.jsx
   │   ├── main.jsx
   │   └── index.css
   ├── index.html
   ├── package.json
   └── README.md

## Tech Stack
- React 19 + Vite
- React Router DOM
- TanStack React Query
- Context API
- Fetch API

## Getting Started

1. Clone the repository (or extract the project)
2. Install dependencies:
   ```bash
   npm install
   ```