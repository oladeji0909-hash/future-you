import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Grid,
  Card,
  CardContent,
  CardActions,
  Button,
  Box,
  Chip,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  CircularProgress,
  Alert,
  Paper
} from '@mui/material';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import { useNavigate } from 'react-router-dom';
import { useSelector } from 'react-redux';
import { RootState } from '../store';
import api from '../services/api';

interface PricingTier {
  name: string;
  price: number;
  features: string[];
  message_limit: number | null;
}

interface TierWithMeta extends PricingTier {
  key: string;
  color: string;
  gradient: string;
  popular?: boolean;
}

const Pricing: React.FC = () => {
  const navigate = useNavigate();
  const { user } = useSelector((state: RootState) => state.auth);
  const [pricing, setPricing] = useState<Record<string, PricingTier> | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [checkoutLoading, setCheckoutLoading] = useState<string | null>(null);

  useEffect(() => {
    fetchPricing();
  }, []);

  const fetchPricing = async () => {
    try {
      const response = await api.get('/api/payments/pricing');
      setPricing(response.data);
    } catch (err) {
      setError('Failed to load pricing');
    } finally {
      setLoading(false);
    }
  };

  const handleUpgrade = async (tier: string) => {
    if (!user) {
      navigate('/login');
      return;
    }

    if (tier === 'free') {
      return;
    }

    setCheckoutLoading(tier);
    try {
      const response = await api.post('/api/payments/create-checkout-session', {
        tier: tier,
        success_url: `${window.location.origin}/dashboard?payment=success`,
        cancel_url: `${window.location.origin}/pricing?payment=cancelled`
      });

      window.location.href = response.data.url;
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to start checkout');
      setCheckoutLoading(null);
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="80vh">
        <CircularProgress />
      </Box>
    );
  }

  if (!pricing) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4 }}>
        <Alert severity="error">{error || 'Failed to load pricing'}</Alert>
      </Container>
    );
  }

  const tiers: TierWithMeta[] = [
    { key: 'free', ...pricing.free, color: '#9e9e9e', gradient: 'linear-gradient(135deg, #bdc3c7 0%, #2c3e50 100%)' },
    { key: 'premium', ...pricing.premium, color: '#667eea', gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', popular: true },
    { key: 'lifetime', ...pricing.lifetime, color: '#f093fb', gradient: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)' }
  ];

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 8 }}>
      <Box textAlign="center" mb={6}>
        <Typography variant="h3" gutterBottom fontWeight="bold">
          Choose Your Plan
        </Typography>
        <Typography variant="h6" color="text.secondary" mb={2}>
          Start free, upgrade when you're ready
        </Typography>
        {user && (
          <Chip 
            label={`Current Plan: ${user.subscription_tier}`} 
            color="primary" 
            sx={{ mt: 2 }}
          />
        )}
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }} onClose={() => setError('')}>
          {error}
        </Alert>
      )}

      <Grid container spacing={4} justifyContent="center">
        {tiers.map((tier) => (
          <Grid item xs={12} md={4} key={tier.key}>
            <Card
              sx={{
                height: '100%',
                display: 'flex',
                flexDirection: 'column',
                position: 'relative',
                border: tier.popular ? '2px solid #667eea' : '1px solid #e0e0e0',
                borderRadius: 3,
                overflow: 'hidden',
                transform: tier.popular ? 'scale(1.05)' : 'scale(1)',
                transition: 'all 0.3s ease',
                boxShadow: tier.popular ? '0 8px 24px rgba(102, 126, 234, 0.3)' : '0 2px 8px rgba(0,0,0,0.1)',
                '&:hover': {
                  transform: tier.popular ? 'scale(1.08)' : 'scale(1.03)',
                  boxShadow: tier.popular ? '0 12px 32px rgba(102, 126, 234, 0.4)' : '0 8px 16px rgba(0,0,0,0.15)'
                }
              }}
            >
              <Box
                sx={{
                  background: tier.gradient,
                  height: 120,
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'center',
                  justifyContent: 'center',
                  position: 'relative'
                }}
              >
                {tier.popular && (
                  <Chip
                    label="MOST POPULAR"
                    size="small"
                    sx={{
                      position: 'absolute',
                      top: 12,
                      right: 12,
                      bgcolor: 'rgba(255,255,255,0.9)',
                      color: '#667eea',
                      fontWeight: 'bold',
                      fontSize: '0.7rem'
                    }}
                  />
                )}
                <Typography
                  variant="h5"
                  fontWeight="bold"
                  color="white"
                  sx={{ textTransform: 'uppercase', letterSpacing: 1 }}
                >
                  {tier.name}
                </Typography>
                <Box sx={{ mt: 1, display: 'flex', alignItems: 'baseline' }}>
                  <Typography variant="h3" fontWeight="bold" color="white">
                    ${tier.price}
                  </Typography>
                  {tier.key === 'premium' && (
                    <Typography variant="body1" color="rgba(255,255,255,0.9)" sx={{ ml: 0.5 }}>
                      /mo
                    </Typography>
                  )}
                </Box>
              </Box>

              <CardContent sx={{ flexGrow: 1, pt: 3, pb: 2 }}>
                <Box textAlign="center" mb={2}>
                  {tier.key === 'lifetime' && (
                    <Typography variant="body2" color="text.secondary" fontWeight="500">
                      💎 One-time payment
                    </Typography>
                  )}
                  {tier.key === 'free' && (
                    <Typography variant="body2" color="text.secondary" fontWeight="500">
                      ✨ Forever free
                    </Typography>
                  )}
                  {tier.key === 'premium' && (
                    <Typography variant="body2" color="text.secondary" fontWeight="500">
                      🚀 Best value
                    </Typography>
                  )}
                </Box>

                <Box textAlign="center" mb={2}>
                  <Chip
                    label={
                      tier.message_limit
                        ? `${tier.message_limit} messages/month`
                        : 'Unlimited messages'
                    }
                    size="small"
                    sx={{ bgcolor: tier.color, color: 'white' }}
                  />
                </Box>

                <List dense>
                  {tier.features.map((feature, index) => (
                    <ListItem key={index} disableGutters>
                      <ListItemIcon sx={{ minWidth: 36 }}>
                        <CheckCircleIcon sx={{ color: tier.color }} fontSize="small" />
                      </ListItemIcon>
                      <ListItemText
                        primary={feature}
                        primaryTypographyProps={{ variant: 'body2' }}
                      />
                    </ListItem>
                  ))}
                </List>
              </CardContent>

              <CardActions sx={{ p: 2, pt: 0 }}>
                <Button
                  fullWidth
                  variant={tier.popular ? 'contained' : 'outlined'}
                  size="large"
                  onClick={() => handleUpgrade(tier.key)}
                  disabled={
                    checkoutLoading !== null ||
                    (user?.subscription_tier === tier.key) ||
                    tier.key === 'free'
                  }
                  sx={{
                    py: 1.5,
                    fontWeight: 'bold',
                    fontSize: '1rem',
                    background: tier.popular ? tier.gradient : 'transparent',
                    borderColor: tier.color,
                    color: tier.popular ? 'white' : tier.color,
                    border: tier.popular ? 'none' : `2px solid ${tier.color}`,
                    '&:hover': {
                      background: tier.popular ? 'linear-gradient(135deg, #5568d3 0%, #6a3d8f 100%)' : `${tier.color}15`,
                      borderColor: tier.color,
                      transform: 'translateY(-2px)',
                      boxShadow: `0 4px 12px ${tier.color}40`
                    },
                    '&:disabled': {
                      background: '#e0e0e0',
                      color: '#9e9e9e'
                    }
                  }}
                >
                  {checkoutLoading === tier.key ? (
                    <CircularProgress size={24} color="inherit" />
                  ) : user?.subscription_tier === tier.key ? (
                    'Current Plan'
                  ) : tier.key === 'free' ? (
                    'Get Started'
                  ) : (
                    'Upgrade Now'
                  )}
                </Button>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Box mt={8} textAlign="center">
        <Typography variant="h5" gutterBottom fontWeight="bold">
          Frequently Asked Questions
        </Typography>
        <Grid container spacing={3} mt={2}>
          <Grid item xs={12} md={6}>
            <Box textAlign="left">
              <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
                Can I change plans later?
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Yes! You can upgrade or downgrade at any time. Changes take effect immediately.
              </Typography>
            </Box>
          </Grid>
          <Grid item xs={12} md={6}>
            <Box textAlign="left">
              <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
                What payment methods do you accept?
              </Typography>
              <Typography variant="body2" color="text.secondary">
                We accept all major credit cards through Stripe's secure payment processing.
              </Typography>
            </Box>
          </Grid>
          <Grid item xs={12} md={6}>
            <Box textAlign="left">
              <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
                Is there a refund policy?
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Yes! We offer a 30-day money-back guarantee. No questions asked.
              </Typography>
            </Box>
          </Grid>
          <Grid item xs={12} md={6}>
            <Box textAlign="left">
              <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
                How does the AI timing work?
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Our AI analyzes your message content and patterns to deliver at the perfect moment for maximum impact.
              </Typography>
            </Box>
          </Grid>
        </Grid>
      </Box>

      <Paper elevation={3} sx={{ mt: 6, p: 4, borderRadius: 3, textAlign: 'center' }}>
        <Typography variant="h5" gutterBottom fontWeight="bold">
          Ready to connect with your future self?
        </Typography>
        <Typography variant="body1" color="text.secondary" mb={3}>
          Join thousands of users creating meaningful messages to their future selves.
        </Typography>
        <Button
          variant="contained"
          size="large"
          onClick={() => navigate(user ? '/dashboard' : '/signup')}
          sx={{
            bgcolor: '#667eea',
            '&:hover': { bgcolor: '#5568d3' },
            px: 4,
            py: 1.5
          }}
        >
          {user ? 'Go to Dashboard' : 'Start Free Today'}
        </Button>
      </Paper>
    </Container>
  );
};

export default Pricing;
