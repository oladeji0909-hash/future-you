import React from 'react';
import { Box, Container, Typography, Button, Grid, Card, CardContent, Paper } from '@mui/material';
import { AutoAwesome, Schedule, Security, TrendingUp, Chat, Email } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';

const Landing: React.FC = () => {
  const navigate = useNavigate();

  const features = [
    {
      icon: <AutoAwesome sx={{ fontSize: 48 }} />,
      title: 'AI-Powered Timing',
      description: 'Our AI determines the perfect moment to deliver your message for maximum impact'
    },
    {
      icon: <Schedule sx={{ fontSize: 48 }} />,
      title: 'Smart Scheduling',
      description: 'Schedule messages for specific dates or let AI choose the optimal time'
    },
    {
      icon: <Security sx={{ fontSize: 48 }} />,
      title: 'End-to-End Encryption',
      description: 'Your messages are encrypted and secure. Only you can read them'
    },
    {
      icon: <Chat sx={{ fontSize: 48 }} />,
      title: 'AI Companion',
      description: 'Get guidance and support from your personal AI companion'
    },
    {
      icon: <TrendingUp sx={{ fontSize: 48 }} />,
      title: 'Track Progress',
      description: 'See your growth and engagement with detailed analytics'
    },
    {
      icon: <Email sx={{ fontSize: 48 }} />,
      title: 'Email Notifications',
      description: 'Get notified when your messages are ready to be delivered'
    }
  ];

  return (
    <Box>
      {/* Hero Section */}
      <Box
        sx={{
          minHeight: '100vh',
          display: 'flex',
          alignItems: 'center',
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          position: 'relative',
          overflow: 'hidden',
          '&::before': {
            content: '""',
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            background: 'radial-gradient(circle at 20% 50%, rgba(255,255,255,0.1) 0%, transparent 50%)',
          }
        }}
      >
        <Container maxWidth="lg" sx={{ position: 'relative', zIndex: 1 }}>
          <Grid container spacing={6} alignItems="center">
            <Grid item xs={12} md={6}>
              <Typography variant="h1" fontWeight="bold" color="white" gutterBottom sx={{ fontSize: { xs: '2.5rem', md: '4rem' } }}>
                ✨ Future You
              </Typography>
              <Typography variant="h4" color="rgba(255,255,255,0.95)" gutterBottom sx={{ mb: 4 }}>
                Messages from your past, delivered at the perfect moment
              </Typography>
              <Typography variant="h6" color="rgba(255,255,255,0.9)" sx={{ mb: 4 }}>
                Write messages to your future self and let AI deliver them when you need them most
              </Typography>
              <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
                <Button
                  variant="contained"
                  size="large"
                  onClick={() => navigate('/signup')}
                  sx={{
                    bgcolor: 'white',
                    color: '#667eea',
                    px: 4,
                    py: 2,
                    fontSize: '1.2rem',
                    fontWeight: 'bold',
                    '&:hover': {
                      bgcolor: '#f5f5f5',
                      transform: 'translateY(-4px)',
                      boxShadow: '0 12px 24px rgba(0,0,0,0.2)'
                    }
                  }}
                >
                  Start Free Today
                </Button>
                <Button
                  variant="outlined"
                  size="large"
                  onClick={() => navigate('/login')}
                  sx={{
                    borderColor: 'white',
                    color: 'white',
                    px: 4,
                    py: 2,
                    fontSize: '1.2rem',
                    fontWeight: 'bold',
                    '&:hover': {
                      borderColor: 'white',
                      bgcolor: 'rgba(255,255,255,0.1)'
                    }
                  }}
                >
                  Login
                </Button>
              </Box>
            </Grid>
            <Grid item xs={12} md={6}>
              <Paper
                elevation={24}
                sx={{
                  p: 4,
                  borderRadius: 4,
                  bgcolor: 'rgba(255,255,255,0.95)',
                  backdropFilter: 'blur(10px)'
                }}
              >
                <Typography variant="h5" fontWeight="bold" gutterBottom color="primary">
                  🎯 Why Future You?
                </Typography>
                <Typography variant="body1" color="text.secondary" sx={{ mb: 2 }}>
                  • Write messages to your future self
                </Typography>
                <Typography variant="body1" color="text.secondary" sx={{ mb: 2 }}>
                  • AI determines optimal delivery time
                </Typography>
                <Typography variant="body1" color="text.secondary" sx={{ mb: 2 }}>
                  • Track your personal growth
                </Typography>
                <Typography variant="body1" color="text.secondary" sx={{ mb: 2 }}>
                  • Get support from AI companion
                </Typography>
                <Typography variant="body1" color="text.secondary">
                  • 100% secure and private
                </Typography>
              </Paper>
            </Grid>
          </Grid>
        </Container>
      </Box>

      {/* Features Section */}
      <Container maxWidth="lg" sx={{ py: 10 }}>
        <Typography variant="h2" fontWeight="bold" textAlign="center" gutterBottom>
          Powerful Features
        </Typography>
        <Typography variant="h6" color="text.secondary" textAlign="center" sx={{ mb: 6 }}>
          Everything you need to connect with your future self
        </Typography>

        <Grid container spacing={4}>
          {features.map((feature, index) => (
            <Grid item xs={12} md={4} key={index}>
              <Card
                elevation={2}
                sx={{
                  height: '100%',
                  borderRadius: 3,
                  transition: 'all 0.3s',
                  '&:hover': {
                    transform: 'translateY(-8px)',
                    boxShadow: '0 12px 24px rgba(102, 126, 234, 0.3)'
                  }
                }}
              >
                <CardContent sx={{ textAlign: 'center', p: 4 }}>
                  <Box sx={{ color: '#667eea', mb: 2 }}>
                    {feature.icon}
                  </Box>
                  <Typography variant="h5" fontWeight="bold" gutterBottom>
                    {feature.title}
                  </Typography>
                  <Typography variant="body1" color="text.secondary">
                    {feature.description}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Container>

      {/* Pricing Preview */}
      <Box sx={{ bgcolor: '#f8f9fa', py: 10 }}>
        <Container maxWidth="lg">
          <Typography variant="h2" fontWeight="bold" textAlign="center" gutterBottom>
            Simple Pricing
          </Typography>
          <Typography variant="h6" color="text.secondary" textAlign="center" sx={{ mb: 6 }}>
            Start free, upgrade when you're ready
          </Typography>

          <Grid container spacing={4} justifyContent="center">
            <Grid item xs={12} md={4}>
              <Card elevation={3} sx={{ borderRadius: 3, textAlign: 'center', p: 4 }}>
                <Typography variant="h4" fontWeight="bold" gutterBottom>
                  Free
                </Typography>
                <Typography variant="h2" fontWeight="bold" color="primary" gutterBottom>
                  $0
                </Typography>
                <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
                  5 messages per month
                </Typography>
                <Button
                  variant="outlined"
                  fullWidth
                  size="large"
                  onClick={() => navigate('/signup')}
                >
                  Get Started
                </Button>
              </Card>
            </Grid>

            <Grid item xs={12} md={4}>
              <Card
                elevation={6}
                sx={{
                  borderRadius: 3,
                  textAlign: 'center',
                  p: 4,
                  border: '3px solid #667eea',
                  transform: 'scale(1.05)'
                }}
              >
                <Typography variant="h4" fontWeight="bold" gutterBottom>
                  Premium
                </Typography>
                <Typography variant="h2" fontWeight="bold" color="primary" gutterBottom>
                  $9.99
                </Typography>
                <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
                  Unlimited messages
                </Typography>
                <Button
                  variant="contained"
                  fullWidth
                  size="large"
                  onClick={() => navigate('/signup')}
                  sx={{
                    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
                  }}
                >
                  Start Free Trial
                </Button>
              </Card>
            </Grid>

            <Grid item xs={12} md={4}>
              <Card elevation={3} sx={{ borderRadius: 3, textAlign: 'center', p: 4 }}>
                <Typography variant="h4" fontWeight="bold" gutterBottom>
                  Lifetime
                </Typography>
                <Typography variant="h2" fontWeight="bold" color="primary" gutterBottom>
                  $99
                </Typography>
                <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
                  One-time payment
                </Typography>
                <Button
                  variant="outlined"
                  fullWidth
                  size="large"
                  onClick={() => navigate('/signup')}
                >
                  Get Lifetime Access
                </Button>
              </Card>
            </Grid>
          </Grid>
        </Container>
      </Box>

      {/* CTA Section */}
      <Container maxWidth="md" sx={{ py: 10, textAlign: 'center' }}>
        <Typography variant="h2" fontWeight="bold" gutterBottom>
          Ready to start your journey?
        </Typography>
        <Typography variant="h6" color="text.secondary" sx={{ mb: 4 }}>
          Join thousands of users creating meaningful messages to their future selves
        </Typography>
        <Button
          variant="contained"
          size="large"
          onClick={() => navigate('/signup')}
          sx={{
            px: 6,
            py: 2,
            fontSize: '1.3rem',
            fontWeight: 'bold',
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            '&:hover': {
              background: 'linear-gradient(135deg, #5568d3 0%, #6a3d8f 100%)',
              transform: 'translateY(-4px)',
              boxShadow: '0 12px 24px rgba(102, 126, 234, 0.4)'
            }
          }}
        >
          🚀 Start Free Today
        </Button>
      </Container>

      {/* Footer */}
      <Box sx={{ bgcolor: '#2c3e50', color: 'white', py: 4 }}>
        <Container maxWidth="lg">
          <Typography variant="body2" textAlign="center">
            © 2024 Future You. All rights reserved.
          </Typography>
        </Container>
      </Box>
    </Box>
  );
};

export default Landing;
