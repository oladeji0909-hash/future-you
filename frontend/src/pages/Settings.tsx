import React, { useState } from 'react';
import {
  Container,
  Box,
  Typography,
  Paper,
  TextField,
  Button,
  Grid,
  Avatar,
  Divider,
  Alert,
  Switch,
  FormControlLabel,
} from '@mui/material';
import { Settings as SettingsIcon, Lock, Security, Person, Download } from '@mui/icons-material';
import { useAppSelector } from '../hooks';

const Settings: React.FC = () => {
  const user = useAppSelector(state => state.auth.user);
  const [fullName, setFullName] = useState(user?.full_name || '');
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [success, setSuccess] = useState('');
  const [error, setError] = useState('');

  const handleProfileUpdate = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSuccess('Profile updated successfully!');
    setTimeout(() => setSuccess(''), 3000);
  };

  const handlePasswordChange = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    
    if (newPassword !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    if (newPassword.length < 8) {
      setError('Password must be at least 8 characters');
      return;
    }

    setSuccess('Password changed successfully!');
    setCurrentPassword('');
    setNewPassword('');
    setConfirmPassword('');
    setTimeout(() => setSuccess(''), 3000);
  };

  const handleExportData = () => {
    const dataStr = JSON.stringify({ user, messages: [] }, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `future-you-data-${new Date().toISOString().split('T')[0]}.json`;
    link.click();
    setSuccess('Data exported successfully!');
    setTimeout(() => setSuccess(''), 3000);
  };

  return (
    <Container maxWidth="md">
      <Box sx={{ mt: 4, mb: 4 }}>
        <Box 
          sx={{ 
            mb: 4,
            p: 4,
            borderRadius: 3,
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            color: 'white',
            textAlign: 'center'
          }}
        >
          <SettingsIcon sx={{ fontSize: 48, mb: 2 }} />
          <Typography variant="h3" fontWeight="bold" gutterBottom>
            Settings
          </Typography>
          <Typography variant="body1" sx={{ opacity: 0.95 }}>
            Manage your account preferences
          </Typography>
        </Box>

        {error && <Alert severity="error" sx={{ mb: 3 }} onClose={() => setError('')}>{error}</Alert>}
        {success && <Alert severity="success" sx={{ mb: 3 }} onClose={() => setSuccess('')}>{success}</Alert>}

        <Paper elevation={2} sx={{ p: 4, mb: 3, borderRadius: 3 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
            <Person sx={{ mr: 2, color: 'primary.main' }} />
            <Typography variant="h5" fontWeight="bold">
              Profile Information
            </Typography>
          </Box>
          <Divider sx={{ mb: 3 }} />
          
          <Box component="form" onSubmit={handleProfileUpdate}>
            <Grid container spacing={3}>
              <Grid item xs={12} sx={{ display: 'flex', justifyContent: 'center', mb: 2 }}>
                <Avatar 
                  sx={{ 
                    width: 100, 
                    height: 100,
                    bgcolor: '#667eea',
                    fontSize: '2.5rem'
                  }}
                >
                  {user?.full_name?.charAt(0) || user?.email.charAt(0).toUpperCase()}
                </Avatar>
              </Grid>
              
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Full Name"
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                />
              </Grid>
              
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Email"
                  value={user?.email}
                  disabled
                  helperText="Email cannot be changed"
                />
              </Grid>
              
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Subscription Plan"
                  value={user?.subscription_tier.toUpperCase()}
                  disabled
                />
              </Grid>
              
              <Grid item xs={12}>
                <Button 
                  type="submit" 
                  variant="contained" 
                  size="large"
                  sx={{
                    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
                  }}
                >
                  Save Changes
                </Button>
              </Grid>
            </Grid>
          </Box>
        </Paper>

        <Paper elevation={2} sx={{ p: 4, mb: 3, borderRadius: 3 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
            <Lock sx={{ mr: 2, color: 'primary.main' }} />
            <Typography variant="h5" fontWeight="bold">
              Change Password
            </Typography>
          </Box>
          <Divider sx={{ mb: 3 }} />
          
          <Box component="form" onSubmit={handlePasswordChange}>
            <Grid container spacing={3}>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  type="password"
                  label="Current Password"
                  value={currentPassword}
                  onChange={(e) => setCurrentPassword(e.target.value)}
                  required
                />
              </Grid>
              
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  type="password"
                  label="New Password"
                  value={newPassword}
                  onChange={(e) => setNewPassword(e.target.value)}
                  required
                  helperText="Minimum 8 characters"
                />
              </Grid>
              
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  type="password"
                  label="Confirm New Password"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  required
                />
              </Grid>
              
              <Grid item xs={12}>
                <Button 
                  type="submit" 
                  variant="contained" 
                  size="large"
                  sx={{
                    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
                  }}
                >
                  Change Password
                </Button>
              </Grid>
            </Grid>
          </Box>
        </Paper>

        <Paper elevation={2} sx={{ p: 4, mb: 3, borderRadius: 3 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
            <Security sx={{ mr: 2, color: 'primary.main' }} />
            <Typography variant="h5" fontWeight="bold">
              Security
            </Typography>
          </Box>
          <Divider sx={{ mb: 3 }} />
          
          <Box>
            <FormControlLabel
              control={<Switch />}
              label="Enable Two-Factor Authentication (2FA)"
            />
            <Typography variant="body2" color="text.secondary" sx={{ ml: 4, mt: 1 }}>
              Add an extra layer of security to your account
            </Typography>
            
            <Button 
              variant="outlined" 
              sx={{ mt: 2, ml: 4 }}
            >
              Setup 2FA
            </Button>
          </Box>
        </Paper>

        <Paper elevation={2} sx={{ p: 4, borderRadius: 3 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
            <Download sx={{ mr: 2, color: 'primary.main' }} />
            <Typography variant="h5" fontWeight="bold">
              Export Data
            </Typography>
          </Box>
          <Divider sx={{ mb: 3 }} />
          
          <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
            Download all your data including messages, settings, and activity
          </Typography>
          
          <Button 
            variant="contained"
            startIcon={<Download />}
            onClick={handleExportData}
            sx={{
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
            }}
          >
            Export My Data
          </Button>
        </Paper>
      </Box>
    </Container>
  );
};

export default Settings;
