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
  LinearProgress,
} from '@mui/material';
import {
  TrendingUp,
  People,
  Email,
  AttachMoney,
  CheckCircle,
  Schedule,
} from '@mui/icons-material';
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8005';

interface UserAnalytics {
  total_messages: number;
  delivered_messages: number;
  read_messages: number;
  scheduled_messages: number;
  engagement_score: number;
  avg_days_until_delivery: number;
  most_common_category: string;
}

interface PlatformAnalytics {
  total_users: number;
  active_users: number;
  total_messages: number;
  delivered_messages: number;
  current_mrr: number;
  mrr_goal: number;
  premium_users: number;
  lifetime_users: number;
  avg_engagement_score: number;
}

interface GrowthData {
  date: string;
  users: number;
  messages: number;
  mrr: number;
}

const Analytics: React.FC = () => {
  const [userAnalytics, setUserAnalytics] = useState<UserAnalytics | null>(null);
  const [platformAnalytics, setPlatformAnalytics] = useState<PlatformAnalytics | null>(null);
  const [growthData, setGrowthData] = useState<GrowthData[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchAnalytics();
  }, []);

  const fetchAnalytics = async () => {
    try {
      const token = localStorage.getItem('token');
      const headers = { Authorization: `Bearer ${token}` };

      const [userRes, platformRes, growthRes] = await Promise.all([
        axios.get(`${API_URL}/api/analytics/me`, { headers }),
        axios.get(`${API_URL}/api/analytics/platform`, { headers }),
        axios.get(`${API_URL}/api/analytics/growth`, { headers }),
      ]);

      setUserAnalytics(userRes.data);
      setPlatformAnalytics(platformRes.data);
      setGrowthData(growthRes.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load analytics');
    } finally {
      setLoading(false);
    }
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

  const mrrProgress = platformAnalytics && platformAnalytics.current_mrr && platformAnalytics.mrr_goal
    ? (platformAnalytics.current_mrr / platformAnalytics.mrr_goal) * 100
    : 0;

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" gutterBottom>
        📊 Analytics Dashboard
      </Typography>

      {/* MRR Progress */}
      {platformAnalytics && (
        <Paper sx={{ p: 3, mb: 3 }}>
          <Typography variant="h6" gutterBottom>
            💰 Monthly Recurring Revenue (MRR)
          </Typography>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
            <Typography variant="h3" sx={{ mr: 2 }}>
              ${(platformAnalytics.current_mrr || 0).toFixed(2)}
            </Typography>
            <Typography variant="body1" color="text.secondary">
              / ${(platformAnalytics.mrr_goal || 10000).toFixed(2)} goal
            </Typography>
          </Box>
          <LinearProgress
            variant="determinate"
            value={Math.min(mrrProgress, 100)}
            sx={{ height: 10, borderRadius: 5 }}
          />
          <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
            {mrrProgress.toFixed(1)}% of $10,000 MRR goal
          </Typography>
        </Paper>
      )}

      {/* Platform Metrics */}
      {platformAnalytics && (
        <Grid container spacing={3} sx={{ mb: 3 }}>
          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Box display="flex" alignItems="center" mb={1}>
                  <People color="primary" sx={{ mr: 1 }} />
                  <Typography variant="h6">{platformAnalytics.total_users || 0}</Typography>
                </Box>
                <Typography variant="body2" color="text.secondary">
                  Total Users
                </Typography>
                <Typography variant="caption" color="success.main">
                  {platformAnalytics.active_users || 0} active
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Box display="flex" alignItems="center" mb={1}>
                  <Email color="primary" sx={{ mr: 1 }} />
                  <Typography variant="h6">{platformAnalytics.total_messages || 0}</Typography>
                </Box>
                <Typography variant="body2" color="text.secondary">
                  Total Messages
                </Typography>
                <Typography variant="caption" color="success.main">
                  {platformAnalytics.delivered_messages || 0} delivered
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Box display="flex" alignItems="center" mb={1}>
                  <AttachMoney color="primary" sx={{ mr: 1 }} />
                  <Typography variant="h6">
                    {(platformAnalytics.premium_users || 0) + (platformAnalytics.lifetime_users || 0)}
                  </Typography>
                </Box>
                <Typography variant="body2" color="text.secondary">
                  Paid Users
                </Typography>
                <Typography variant="caption" color="success.main">
                  {platformAnalytics.premium_users || 0} premium, {platformAnalytics.lifetime_users || 0} lifetime
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Box display="flex" alignItems="center" mb={1}>
                  <TrendingUp color="primary" sx={{ mr: 1 }} />
                  <Typography variant="h6">
                    {(platformAnalytics.avg_engagement_score || 0).toFixed(1)}%
                  </Typography>
                </Box>
                <Typography variant="body2" color="text.secondary">
                  Avg Engagement
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}

      {/* User Analytics */}
      {userAnalytics && (
        <Paper sx={{ p: 3, mb: 3 }}>
          <Typography variant="h6" gutterBottom>
            📈 Your Activity
          </Typography>
          <Grid container spacing={2}>
            <Grid item xs={6} sm={3}>
              <Box textAlign="center">
                <Schedule fontSize="large" color="primary" />
                <Typography variant="h5">{userAnalytics.total_messages || 0}</Typography>
                <Typography variant="body2" color="text.secondary">
                  Total Messages
                </Typography>
              </Box>
            </Grid>
            <Grid item xs={6} sm={3}>
              <Box textAlign="center">
                <CheckCircle fontSize="large" color="success" />
                <Typography variant="h5">{userAnalytics.delivered_messages || 0}</Typography>
                <Typography variant="body2" color="text.secondary">
                  Delivered
                </Typography>
              </Box>
            </Grid>
            <Grid item xs={6} sm={3}>
              <Box textAlign="center">
                <Email fontSize="large" color="info" />
                <Typography variant="h5">{userAnalytics.read_messages || 0}</Typography>
                <Typography variant="body2" color="text.secondary">
                  Read
                </Typography>
              </Box>
            </Grid>
            <Grid item xs={6} sm={3}>
              <Box textAlign="center">
                <TrendingUp fontSize="large" color="warning" />
                <Typography variant="h5">{(userAnalytics.engagement_score || 0).toFixed(0)}%</Typography>
                <Typography variant="body2" color="text.secondary">
                  Engagement
                </Typography>
              </Box>
            </Grid>
          </Grid>
          <Box sx={{ mt: 2 }}>
            <Typography variant="body2" color="text.secondary">
              Avg delivery time: {(userAnalytics.avg_days_until_delivery || 0).toFixed(0)} days
            </Typography>
            {userAnalytics.most_common_category && (
              <Typography variant="body2" color="text.secondary">
                Most common: {userAnalytics.most_common_category}
              </Typography>
            )}
          </Box>
        </Paper>
      )}

      {/* Growth Chart */}
      {growthData.length > 0 && (
        <Paper sx={{ p: 3 }}>
          <Typography variant="h6" gutterBottom>
            📊 Growth Over Time (Last 30 Days)
          </Typography>
          <Box sx={{ overflowX: 'auto' }}>
            <Box sx={{ minWidth: 600, height: 200, position: 'relative' }}>
              {growthData.map((data, index) => {
                const maxMrr = Math.max(...growthData.map(d => d.mrr));
                const height = maxMrr > 0 ? (data.mrr / maxMrr) * 100 : 0;
                return (
                  <Box
                    key={index}
                    sx={{
                      display: 'inline-block',
                      width: `${100 / growthData.length}%`,
                      verticalAlign: 'bottom',
                      textAlign: 'center',
                      px: 0.5,
                    }}
                  >
                    <Box
                      sx={{
                        height: `${height}%`,
                        minHeight: data.mrr > 0 ? 20 : 5,
                        bgcolor: 'primary.main',
                        borderRadius: 1,
                        mb: 1,
                        transition: 'all 0.3s',
                        '&:hover': {
                          bgcolor: 'primary.dark',
                          transform: 'scaleY(1.1)',
                        },
                      }}
                      title={`$${data.mrr.toFixed(2)} MRR`}
                    />
                    <Typography variant="caption" color="text.secondary">
                      {new Date(data.date).getDate()}
                    </Typography>
                  </Box>
                );
              })}
            </Box>
          </Box>
          <Typography variant="caption" color="text.secondary" sx={{ mt: 2, display: 'block' }}>
            Hover over bars to see MRR values
          </Typography>
        </Paper>
      )}
    </Container>
  );
};

export default Analytics;
