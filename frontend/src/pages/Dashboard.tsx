import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Box, Container, Typography, Grid, Card, CardContent, Button, Chip, Paper } from '@mui/material';
import { Message, Chat, Timeline, TrendingUp } from '@mui/icons-material';
import { useAppSelector } from '../hooks';

const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  const user = useAppSelector(state => state.auth.user);

  const cards = [
    {
      title: 'Messages',
      description: 'Create and manage messages to your future self',
      icon: Message,
      color: '#667eea',
      gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      path: '/messages'
    },
    {
      title: 'AI Companion',
      description: 'Chat with your AI companion for guidance',
      icon: Chat,
      color: '#f093fb',
      gradient: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
      path: '/companion'
    },
    {
      title: 'Timeline',
      description: 'View your journey and upcoming deliveries',
      icon: Timeline,
      color: '#4facfe',
      gradient: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
      path: '/delivery'
    }
  ];

  return (
    <Container maxWidth="lg">
      <Box sx={{ mt: 4, mb: 6 }}>
        {/* Hero Section */}
        <Box 
          sx={{ 
            mb: 6,
            p: 4,
            borderRadius: 3,
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            color: 'white',
            position: 'relative',
            overflow: 'hidden',
            '&::before': {
              content: '""',
              position: 'absolute',
              top: 0,
              left: 0,
              right: 0,
              bottom: 0,
              background: 'radial-gradient(circle at 80% 20%, rgba(255,255,255,0.1) 0%, transparent 50%)',
            }
          }}
        >
          <Box sx={{ position: 'relative', zIndex: 1 }}>
            <Typography variant="h3" fontWeight="bold" gutterBottom>
              Welcome back, {user?.full_name || 'there'}! 👋
            </Typography>
            <Typography variant="h6" sx={{ opacity: 0.9, mb: 2 }}>
              Ready to connect with your future self?
            </Typography>
            <Chip 
              label={`${user?.subscription_tier.toUpperCase()} Plan`}
              sx={{ 
                bgcolor: 'rgba(255,255,255,0.2)',
                color: 'white',
                fontWeight: 'bold',
                backdropFilter: 'blur(10px)'
              }}
            />
          </Box>
        </Box>

        {/* Quick Actions */}
        <Grid container spacing={3}>
          {cards.map((card, index) => (
            <Grid item xs={12} md={4} key={index}>
              <Card
                onClick={() => navigate(card.path)}
                sx={{
                  cursor: 'pointer',
                  height: '100%',
                  borderRadius: 3,
                  border: '1px solid #e0e0e0',
                  transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
                  '&:hover': {
                    transform: 'translateY(-8px)',
                    boxShadow: `0 12px 24px ${card.color}40`,
                    borderColor: card.color
                  }
                }}
              >
                <CardContent sx={{ p: 3 }}>
                  <Box
                    sx={{
                      width: 60,
                      height: 60,
                      borderRadius: 2,
                      background: card.gradient,
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      mb: 2
                    }}
                  >
                    <card.icon sx={{ fontSize: 32, color: 'white' }} />
                  </Box>
                  <Typography variant="h5" fontWeight="bold" gutterBottom>
                    {card.title}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {card.description}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>

        {/* Stats Section */}
        <Box sx={{ mt: 6 }}>
          <Typography variant="h5" fontWeight="bold" gutterBottom sx={{ mb: 3 }}>
            📊 Quick Stats
          </Typography>
          <Grid container spacing={3}>
            <Grid item xs={12} sm={6} md={3}>
              <Card sx={{ p: 3, textAlign: 'center', borderRadius: 3 }}>
                <Typography variant="h3" fontWeight="bold" color="primary">
                  0
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Total Messages
                </Typography>
              </Card>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Card sx={{ p: 3, textAlign: 'center', borderRadius: 3 }}>
                <Typography variant="h3" fontWeight="bold" color="success.main">
                  0
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Delivered
                </Typography>
              </Card>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Card sx={{ p: 3, textAlign: 'center', borderRadius: 3 }}>
                <Typography variant="h3" fontWeight="bold" color="warning.main">
                  0
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Scheduled
                </Typography>
              </Card>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Card sx={{ p: 3, textAlign: 'center', borderRadius: 3 }}>
                <Typography variant="h3" fontWeight="bold" color="info.main">
                  0%
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Engagement
                </Typography>
              </Card>
            </Grid>
          </Grid>
        </Box>

        {/* CTA */}
        <Paper 
          elevation={2}
          sx={{ 
            mt: 6, 
            p: 4, 
            borderRadius: 3,
            textAlign: 'center'
          }}
        >
          <Typography variant="h5" fontWeight="bold" gutterBottom>
            🚀 Create Your First Message
          </Typography>
          <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
            Start your journey by writing a message to your future self
          </Typography>
          <Button
            variant="contained"
            size="large"
            onClick={() => navigate('/messages')}
            sx={{
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              px: 4,
              py: 1.5,
              fontSize: '1.1rem',
              fontWeight: 'bold',
              '&:hover': {
                background: 'linear-gradient(135deg, #5568d3 0%, #6a3d8f 100%)',
                transform: 'translateY(-2px)',
                boxShadow: '0 8px 16px rgba(102, 126, 234, 0.4)'
              }
            }}
          >
            ✨ Create Message
          </Button>
        </Paper>
      </Box>
    </Container>
  );
};

export default Dashboard;
