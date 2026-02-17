import React, { useState, useEffect } from 'react';
import {
  Container,
  Grid,
  Paper,
  Typography,
  Box,
  CircularProgress,
  Alert,
  Card,
  CardContent,
  Chip,
  Button,
  List,
  ListItem,
  ListItemText,
  Divider,
} from '@mui/material';
import {
  Schedule,
  CheckCircle,
  Warning,
  Email,
} from '@mui/icons-material';
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8005';

interface DeliveryStats {
  total_scheduled: number;
  delivered_today: number;
  delivered_this_week: number;
  delivered_this_month: number;
  upcoming_24h: number;
  upcoming_week: number;
  overdue_count: number;
}

interface Message {
  id: number;
  title: string;
  scheduled_for: string;
  delivered_at?: string;
  read_at?: string;
  category?: string;
}

interface Performance {
  total_delivered: number;
  total_read: number;
  read_rate: number;
  avg_time_to_read_hours: number;
}

const Delivery: React.FC = () => {
  const [stats, setStats] = useState<DeliveryStats | null>(null);
  const [upcoming, setUpcoming] = useState<Message[]>([]);
  const [overdue, setOverdue] = useState<Message[]>([]);
  const [performance, setPerformance] = useState<Performance | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchDeliveryData();
  }, []);

  const fetchDeliveryData = async () => {
    try {
      const token = localStorage.getItem('token');
      const headers = { Authorization: `Bearer ${token}` };

      const [statsRes, upcomingRes, overdueRes, perfRes] = await Promise.all([
        axios.get(`${API_URL}/api/delivery/stats`, { headers }),
        axios.get(`${API_URL}/api/delivery/upcoming`, { headers }),
        axios.get(`${API_URL}/api/delivery/overdue`, { headers }),
        axios.get(`${API_URL}/api/delivery/performance`, { headers }),
      ]);

      setStats(statsRes.data);
      setUpcoming(upcomingRes.data);
      setOverdue(overdueRes.data);
      setPerformance(perfRes.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load delivery data');
    } finally {
      setLoading(false);
    }
  };

  const markAsRead = async (messageId: number) => {
    try {
      const token = localStorage.getItem('token');
      await axios.post(
        `${API_URL}/api/delivery/mark-read/${messageId}`,
        {},
        { headers: { Authorization: `Bearer ${token}` } }
      );
      fetchDeliveryData();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to mark as read');
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = date.getTime() - now.getTime();
    const diffDays = Math.ceil(diffMs / (1000 * 60 * 60 * 24));

    if (diffDays === 0) return 'Today';
    if (diffDays === 1) return 'Tomorrow';
    if (diffDays < 7) return `In ${diffDays} days`;
    return date.toLocaleDateString();
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="80vh">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4 }}>
        <Alert severity="error">{error}</Alert>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      {/* Header */}
      <Box 
        sx={{ 
          mb: 4,
          p: 4,
          borderRadius: 3,
          background: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
          color: 'white',
          textAlign: 'center'
        }}
      >
        <Typography variant="h3" fontWeight="bold" gutterBottom>
          📬 Delivery Dashboard
        </Typography>
        <Typography variant="h6" sx={{ opacity: 0.95 }}>
          Track your message deliveries and performance
        </Typography>
      </Box>

      {/* Stats Cards */}
      {stats && (
        <Grid container spacing={3} sx={{ mb: 4 }}>
          <Grid item xs={12} sm={6} md={3}>
            <Card sx={{ 
              borderRadius: 3,
              border: '2px solid #e0e0e0',
              transition: 'all 0.3s',
              '&:hover': {
                transform: 'translateY(-4px)',
                boxShadow: '0 8px 16px rgba(79, 172, 254, 0.3)',
                borderColor: '#4facfe'
              }
            }}>
              <CardContent sx={{ textAlign: 'center', p: 3 }}>
                <Schedule sx={{ fontSize: 48, color: '#4facfe', mb: 1 }} />
                <Typography variant="h3" fontWeight="bold">{stats.total_scheduled}</Typography>
                <Typography variant="body2" color="text.secondary">
                  Total Scheduled
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} sm={6} md={3}>
            <Card sx={{ 
              borderRadius: 3,
              border: '2px solid #e0e0e0',
              transition: 'all 0.3s',
              '&:hover': {
                transform: 'translateY(-4px)',
                boxShadow: '0 8px 16px rgba(76, 175, 80, 0.3)',
                borderColor: '#4caf50'
              }
            }}>
              <CardContent sx={{ textAlign: 'center', p: 3 }}>
                <CheckCircle sx={{ fontSize: 48, color: '#4caf50', mb: 1 }} />
                <Typography variant="h3" fontWeight="bold">{stats.delivered_this_week}</Typography>
                <Typography variant="body2" color="text.secondary">
                  Delivered This Week
                </Typography>
                <Chip 
                  label={`${stats.delivered_today} today`} 
                  size="small" 
                  sx={{ mt: 1, bgcolor: '#4caf5020', color: '#4caf50' }}
                />
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} sm={6} md={3}>
            <Card sx={{ 
              borderRadius: 3,
              border: '2px solid #e0e0e0',
              transition: 'all 0.3s',
              '&:hover': {
                transform: 'translateY(-4px)',
                boxShadow: '0 8px 16px rgba(33, 150, 243, 0.3)',
                borderColor: '#2196f3'
              }
            }}>
              <CardContent sx={{ textAlign: 'center', p: 3 }}>
                <Email sx={{ fontSize: 48, color: '#2196f3', mb: 1 }} />
                <Typography variant="h3" fontWeight="bold">{stats.upcoming_24h}</Typography>
                <Typography variant="body2" color="text.secondary">
                  Coming in 24h
                </Typography>
                <Chip 
                  label={`${stats.upcoming_week} this week`} 
                  size="small" 
                  sx={{ mt: 1, bgcolor: '#2196f320', color: '#2196f3' }}
                />
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} sm={6} md={3}>
            <Card sx={{ 
              borderRadius: 3,
              border: '2px solid #e0e0e0',
              transition: 'all 0.3s',
              '&:hover': {
                transform: 'translateY(-4px)',
                boxShadow: '0 8px 16px rgba(255, 152, 0, 0.3)',
                borderColor: '#ff9800'
              }
            }}>
              <CardContent sx={{ textAlign: 'center', p: 3 }}>
                <Warning sx={{ fontSize: 48, color: '#ff9800', mb: 1 }} />
                <Typography variant="h3" fontWeight="bold">{stats.overdue_count}</Typography>
                <Typography variant="body2" color="text.secondary">
                  Overdue
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}

      {/* Performance Metrics */}
      {performance && (
        <Paper sx={{ p: 4, mb: 4, borderRadius: 3 }}>
          <Typography variant="h5" fontWeight="bold" gutterBottom sx={{ mb: 3 }}>
            📊 Performance Metrics
          </Typography>
          <Grid container spacing={3}>
            <Grid item xs={6} sm={3}>
              <Box textAlign="center">
                <Typography variant="h3" fontWeight="bold" color="primary">
                  {performance.total_delivered || 0}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Delivered
                </Typography>
              </Box>
            </Grid>
            <Grid item xs={6} sm={3}>
              <Box textAlign="center">
                <Typography variant="h3" fontWeight="bold" color="success.main">
                  {performance.total_read || 0}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Read
                </Typography>
              </Box>
            </Grid>
            <Grid item xs={6} sm={3}>
              <Box textAlign="center">
                <Typography variant="h3" fontWeight="bold" color="info.main">
                  {(performance.read_rate || 0).toFixed(0)}%
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Read Rate
                </Typography>
              </Box>
            </Grid>
            <Grid item xs={6} sm={3}>
              <Box textAlign="center">
                <Typography variant="h3" fontWeight="bold" color="warning.main">
                  {(performance.avg_time_to_read_hours || 0).toFixed(0)}h
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Avg Time to Read
                </Typography>
              </Box>
            </Grid>
          </Grid>
        </Paper>
      )}

      <Grid container spacing={3}>
        {/* Upcoming Deliveries */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3, borderRadius: 3, minHeight: 300 }}>
            <Typography variant="h6" fontWeight="bold" gutterBottom>
              📅 Upcoming Deliveries
            </Typography>
            {upcoming.length === 0 ? (
              <Box sx={{ textAlign: 'center', py: 4 }}>
                <Typography variant="body2" color="text.secondary">
                  No upcoming deliveries
                </Typography>
              </Box>
            ) : (
              <List>
                {upcoming.map((msg, index) => (
                  <React.Fragment key={msg.id}>
                    {index > 0 && <Divider />}
                    <ListItem sx={{ py: 2 }}>
                      <ListItemText
                        primary={
                          <Typography variant="body1" fontWeight="500">
                            {msg.title}
                          </Typography>
                        }
                        secondary={
                          <Box sx={{ mt: 1 }}>
                            <Chip 
                              label={formatDate(msg.scheduled_for)} 
                              size="small"
                              sx={{ bgcolor: '#4facfe20', color: '#4facfe', mr: 1 }}
                            />
                            {msg.category && (
                              <Chip
                                label={msg.category}
                                size="small"
                                sx={{ bgcolor: '#f093fb20', color: '#f093fb' }}
                              />
                            )}
                          </Box>
                        }
                      />
                    </ListItem>
                  </React.Fragment>
                ))}
              </List>
            )}
          </Paper>
        </Grid>

        {/* Overdue Messages */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3, borderRadius: 3, minHeight: 300 }}>
            <Typography variant="h6" fontWeight="bold" gutterBottom>
              ⚠️ Overdue Messages
            </Typography>
            {overdue.length === 0 ? (
              <Box sx={{ textAlign: 'center', py: 4 }}>
                <CheckCircle sx={{ fontSize: 48, color: '#4caf50', mb: 2 }} />
                <Typography variant="body2" color="text.secondary">
                  All caught up! No overdue messages
                </Typography>
              </Box>
            ) : (
              <List>
                {overdue.map((msg, index) => (
                  <React.Fragment key={msg.id}>
                    {index > 0 && <Divider />}
                    <ListItem sx={{ py: 2 }}>
                      <ListItemText
                        primary={
                          <Typography variant="body1" fontWeight="500">
                            {msg.title}
                          </Typography>
                        }
                        secondary={
                          <Box sx={{ mt: 1 }}>
                            <Typography variant="caption" color="error" display="block">
                              Scheduled: {new Date(msg.scheduled_for).toLocaleDateString()}
                            </Typography>
                            {msg.delivered_at && !msg.read_at && (
                              <Button
                                size="small"
                                variant="outlined"
                                onClick={() => markAsRead(msg.id)}
                                sx={{ mt: 1 }}
                              >
                                Mark as Read
                              </Button>
                            )}
                          </Box>
                        }
                      />
                    </ListItem>
                  </React.Fragment>
                ))}
              </List>
            )}
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default Delivery;
