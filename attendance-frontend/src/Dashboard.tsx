import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface Student {
  id: number;
  username: string;
  email: string;
  enrolled_date: string;
  image_hash: string;
}

const Dashboard = () => {
  const [students, setStudents] = useState<Student[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showAddStudent, setShowAddStudent] = useState(false);

  useEffect(() => {
    fetchStudents();
  }, []);

  const fetchStudents = async () => {
    try {
      const response = await axios.get(`${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/students`);
      setStudents(response.data);
    } catch (err) {
      setError('Failed to fetch students');
    } finally {
      setLoading(false);
    }
  };

  const addStudent = async (username: string, email: string, imageHash: string) => {
    try {
      await axios.post(`${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/students/enroll`, {
        username,
        email,
        image_hash: imageHash,
      });
      setShowAddStudent(false);
      fetchStudents();
    } catch (err) {
      setError('Failed to enroll student');
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString();
  };

  return (
    <div style={{ padding: '40px', background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', minHeight: '100vh' }}>
      <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
        <div style={{ 
          display: 'flex', 
          justifyContent: 'space-between', 
          alignItems: 'center',
          marginBottom: '40px'
        }}>
          <h1 style={{ color: 'white' }}>🎓 Attendance Dashboard</h1>
          <button 
            className="btn btn-primary"
            onClick={() => setShowAddStudent(true)}
            style={{ background: 'white', color: '#667eea' }}
          >
            + Add Student
          </button>
        </div>

        {loading ? (
          <div style={{ textAlign: 'center', padding: '40px' }}>Loading students...</div>
        ) : (
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))',
            gap: '24px'
          }}>
            {students.length === 0 ? (
              <p style={{ color: 'white' }}>No students enrolled yet.</p>
            ) : (
              students.map((student) => (
                <div key={student.id} style={{
                  background: 'rgba(255, 255, 255, 0.95)',
                  borderRadius: '12px',
                  padding: '20px',
                  boxShadow: '0 4px 12px rgba(0, 0, 0, 0.1)',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '16px'
                }}>
                  <div style={{ 
                    width: '48px', 
                    height: '48px', 
                    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                    borderRadius: '50%',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: 'white',
                    fontWeight: 'bold',
                    fontSize: '18px'
                  }}>
                    {student.username[0].toUpperCase()}
                  </div>
                  <div style={{ flex: 1 }}>
                    <h3 style={{ color: '#333', marginBottom: '4px' }}>
                      {student.username}
                    </h3>
                    <p style={{ color: '#666', fontSize: '14px' }}>{student.email}</p>
                    <p style={{ color: '#999', fontSize: '12px' }}>
                      Enrolled: {formatDate(student.enrolled_date)}
                    </p>
                  </div>
                </div>
              ))
            )}
          </div>
        )}

        {/* Add Student Modal */}
        {showAddStudent && (
          <div style={{
            position: 'fixed',
            top: '0',
            left: '0',
            width: '100%',
            height: '100%',
            background: 'rgba(0, 0, 0, 0.5)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            zIndex: 1000
          }}>
            <div style={{
              background: 'white',
              borderRadius: '12px',
              padding: '32px',
              maxWidth: '400px',
              width: '90%',
              boxShadow: '0 12px 48px rgba(0, 0, 0, 0.2)'
            }}>
              <h2 style={{ color: '#333', marginBottom: '24px' }}>Add New Student</h2>
              <form 
                onSubmit={(e) => {
                  e.preventDefault();
                  const form = e.target as HTMLFormElement;
                  const formData = new FormData(form);
                  addStudent(
                    formData.get('username') as string,
                    formData.get('email') as string,
                    formData.get('imageHash') as string
                  );
                }}
              >
                <div style={{ marginBottom: '16px' }}>
                  <label style={{ display: 'block', marginBottom: '8px', color: '#333' }}>Username</label>
                  <input
                    type="text"
                    name="username"
                    className="input"
                    required
                  />
                </div>
                <div style={{ marginBottom: '16px' }}>
                  <label style={{ display: 'block', marginBottom: '8px', color: '#333' }}>Email</label>
                  <input
                    type="email"
                    name="email"
                    className="input"
                    required
                  />
                </div>
                <div style={{ marginBottom: '16px' }}>
                  <label style={{ display: 'block', marginBottom: '8px', color: '#333' }}>Image Hash (SHA-256)</label>
                  <input
                    type="text"
                    name="imageHash"
                    className="input"
                    placeholder="Enter SHA-256 hash of enrolled photo"
                  />
                </div>
                <div style={{ display: 'flex', gap: '16px' }}>
                  <button 
                    type="submit" 
                    className="btn btn-primary"
                    style={{ flex: 1 }}
                  >
                    Add Student
                  </button>
                  <button 
                    type="button" 
                    onClick={() => setShowAddStudent(false)}
                    className="btn btn-secondary"
                    style={{ flex: 1 }}
                  >
                    Cancel
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
