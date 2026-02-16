import React, { useState, useEffect } from 'react';
import {
  Box,
  Container,
  Typography,
  Button,
  TextField,
  Card,
  CardContent,
  Chip,
  Grid,
  Paper,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Alert,
} from '@mui/material';
import { Add, Delete, Search, FilterList } from '@mui/icons-material';
import { useAppDispatch, useAppSelector } from '../hooks';
import { setMessages, addMessage, removeMessage } from '../slices/messagesSlice';
import { messagesAPI } from '../services/api';

const Messages: React.FC = () => {
  const [content, setContent] = useState('');
  const [scheduledDate, setScheduledDate] = useState('');
  const [deliveryTiming, setDeliveryTiming] = useState('ai_optimal');
  const [showForm, setShowForm] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [filterStatus, setFilterStatus] = useState('all');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const dispatch = useAppDispatch();
  const messages = useAppSelector(state => state.messages.messages);

  useEffect(() => {
    loadMessages();
  }, []);

  const loadMessages = async () => {
    try {
      const response = await messagesAPI.getAll();
      dispatch(setMessages(response.data));
    } catch (err) {
      setError('Failed to load messages');
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    try {
      const response = await messagesAPI.create({
        content,
        delivery_timing: deliveryTiming,
        scheduled_for: scheduledDate || undefined,
      });
      dispatch(addMessage(response.data));
      setContent('');
      setScheduledDate('');
      setShowForm(false);
      setSuccess('Message created successfully!');
      setTimeout(() => setSuccess(''), 3000);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to create message');
    }
  };

  const handleDelete = async (id: number) => {
    if (!window.confirm('Are you sure you want to delete this message?')) return;
    try {
      await messagesAPI.delete(id);
      dispatch(removeMessage(id));
      setSuccess('Message deleted');
      setTimeout(() => setSuccess(''), 3000);
    } catch (err) {
      setError('Failed to delete message');
    }
  };

  const filteredMessages = messages.filter(msg => {
    const matchesSearch = msg.content.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesFilter = filterStatus === 'all' || msg.status === filterStatus;
    return matchesSearch && matchesFilter;
  });

  return (
    <Container maxWidth="lg">
      <Box sx={{ mt: 4, mb: 4 }}>
        {/* Header */}
        <Box 
          sx={{ 
            mb: 4,
            p: 4,
            borderRadius: 3,
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            color: 'white',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center'
          }}
        >
          <Box>
            <Typography variant="h3" fontWeight="bold" gutterBottom>
              📬 Your Messages
            </Typography>
            <Typography variant="body1" sx={{ opacity: 0.95 }}>
              Messages to your future self
            </Typography>
          </Box>
          <Button
            variant="contained"
            size="large"
            startIcon={<Add />}
            onClick={() => setShowForm(true)}
            sx={{
              bgcolor: 'white',
              color: '#667eea',
              '&:hover': { bgcolor: '#f5f5f5' }
            }}
          >
            New Message
          </Button>
        </Box>

        {/* Alerts */}
        {error && <Alert severity="error" sx={{ mb: 3 }} onClose={() => setError('')}>{error}</Alert>}
        {success && <Alert severity="success" sx={{ mb: 3 }} onClose={() => setSuccess('')}>{success}</Alert>}

        {/* Search & Filter */}
        <Paper elevation={2} sx={{ p: 3, mb: 3, borderRadius: 3 }}>
          <Grid container spacing={2} alignItems="center">
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                placeholder="Search messages..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                InputProps={{
                  startAdornment: <Search sx={{ mr: 1, color: 'text.secondary' }} />
                }}
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <FormControl fullWidth>
                <InputLabel>Filter by Status</InputLabel>
                <Select
                  value={filterStatus}
                  label="Filter by Status"
                  onChange={(e) => setFilterStatus(e.target.value)}
                  startAdornment={<FilterList sx={{ mr: 1, color: 'text.secondary' }} />}
                >
                  <MenuItem value="all">All Messages</MenuItem>
                  <MenuItem value="draft">Draft</MenuItem>
                  <MenuItem value="scheduled">Scheduled</MenuItem>
                  <MenuItem value="delivered">Delivered</MenuItem>
                  <MenuItem value="read">Read</MenuItem>
                </Select>
              </FormControl>
            </Grid>
          </Grid>
        </Paper>

        {/* Messages List */}
        {filteredMessages.length === 0 ? (
          <Paper elevation={2} sx={{ p: 6, textAlign: 'center', borderRadius: 3 }}>
            <Typography variant="h6" color="text.secondary" gutterBottom>
              No messages yet
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
              Create your first message to your future self
            </Typography>
            <Button
              variant="contained"
              startIcon={<Add />}
              onClick={() => setShowForm(true)}
              sx={{
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
              }}
            >
              Create Message
            </Button>
          </Paper>
        ) : (
          <Grid container spacing={3}>
            {filteredMessages.map((message) => (
              <Grid item xs={12} md={6} key={message.id}>
                <Card 
                  elevation={2}
                  sx={{ 
                    borderRadius: 3,
                    transition: 'all 0.3s',
                    '&:hover': {
                      transform: 'translateY(-4px)',
                      boxShadow: '0 8px 16px rgba(0,0,0,0.15)'
                    }
                  }}
                >
                  <CardContent>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                      <Chip 
                        label={message.status} 
                        size="small" 
                        color={
                          message.status === 'delivered' ? 'success' :
                          message.status === 'scheduled' ? 'primary' :
                          message.status === 'read' ? 'info' : 'default'
                        }
                      />
                      <IconButton 
                        size="small" 
                        onClick={() => handleDelete(message.id)}
                        sx={{ color: 'error.main' }}
                      >
                        <Delete fontSize="small" />
                      </IconButton>
                    </Box>
                    
                    <Typography variant="body1" sx={{ mb: 2, minHeight: 60 }}>
                      {message.content.substring(0, 150)}
                      {message.content.length > 150 && '...'}
                    </Typography>
                    
                    <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                      <Chip 
                        label={message.delivery_timing.replace('_', ' ')} 
                        size="small" 
                        variant="outlined"
                      />
                      {message.scheduled_for && (
                        <Chip 
                          label={new Date(message.scheduled_for).toLocaleDateString()} 
                          size="small" 
                          variant="outlined"
                          color="primary"
                        />
                      )}
                      {message.tags?.map(tag => (
                        <Chip key={tag} label={tag} size="small" variant="outlined" />
                      ))}
                    </Box>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        )}

        {/* Create Message Dialog */}
        <Dialog 
          open={showForm} 
          onClose={() => setShowForm(false)}
          maxWidth="md"
          fullWidth
        >
          <DialogTitle>
            <Typography variant="h5" fontWeight="bold">
              ✨ Create Message to Future You
            </Typography>
          </DialogTitle>
          <DialogContent>
            <Box component="form" onSubmit={handleSubmit} sx={{ mt: 2 }}>
              <TextField
                fullWidth
                multiline
                rows={8}
                label="Your Message"
                placeholder="What do you want to tell your future self?"
                value={content}
                onChange={(e) => setContent(e.target.value)}
                sx={{ mb: 3 }}
                required
              />
              
              <FormControl fullWidth sx={{ mb: 3 }}>
                <InputLabel>Delivery Timing</InputLabel>
                <Select
                  value={deliveryTiming}
                  label="Delivery Timing"
                  onChange={(e) => setDeliveryTiming(e.target.value)}
                >
                  <MenuItem value="ai_optimal">🤖 AI Optimal (Recommended)</MenuItem>
                  <MenuItem value="specific_date">📅 Specific Date</MenuItem>
                  <MenuItem value="random">🎲 Random Surprise</MenuItem>
                  <MenuItem value="milestone">🎯 Milestone Based</MenuItem>
                </Select>
              </FormControl>

              {deliveryTiming === 'specific_date' && (
                <TextField
                  fullWidth
                  type="datetime-local"
                  label="Schedule For"
                  value={scheduledDate}
                  onChange={(e) => setScheduledDate(e.target.value)}
                  InputLabelProps={{ shrink: true }}
                  sx={{ mb: 3 }}
                />
              )}
            </Box>
          </DialogContent>
          <DialogActions sx={{ p: 3 }}>
            <Button onClick={() => setShowForm(false)}>
              Cancel
            </Button>
            <Button 
              variant="contained" 
              onClick={handleSubmit}
              sx={{
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                px: 4
              }}
            >
              Create Message
            </Button>
          </DialogActions>
        </Dialog>
      </Box>
    </Container>
  );
};

export default Messages;
