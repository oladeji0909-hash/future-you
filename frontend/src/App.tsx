import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider, createTheme, CssBaseline } from '@mui/material';
import Login from './pages/Login';
import Signup from './pages/Signup';
import Dashboard from './pages/Dashboard';
import Messages from './pages/Messages';
import Companion from './pages/Companion';
import Pricing from './pages/Pricing';
import Analytics from './pages/Analytics';
import Delivery from './pages/Delivery';
import Settings from './pages/Settings';
import Landing from './pages/Landing';
import Navigation from './components/Navigation';
import { useAppSelector } from './hooks';

const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#6366f1',
    },
    secondary: {
      main: '#ec4899',
    },
  },
});

const PrivateRoute: React.FC<{ children: React.ReactElement }> = ({ children }) => {
  const isAuthenticated = useAppSelector(state => state.auth.isAuthenticated);
  return isAuthenticated ? <Navigation>{children}</Navigation> : <Navigate to="/login" />;
};

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/pricing" element={<Pricing />} />
        <Route path="/" element={<Landing />} />
        <Route path="/analytics" element={<PrivateRoute><Analytics /></PrivateRoute>} />
        <Route path="/delivery" element={<PrivateRoute><Delivery /></PrivateRoute>} />
        <Route path="/settings" element={<PrivateRoute><Settings /></PrivateRoute>} />
        <Route path="/dashboard" element={<PrivateRoute><Dashboard /></PrivateRoute>} />
        <Route path="/messages" element={<PrivateRoute><Messages /></PrivateRoute>} />
        <Route path="/companion" element={<PrivateRoute><Companion /></PrivateRoute>} />
      </Routes>
    </ThemeProvider>
  );
}

export default App;
