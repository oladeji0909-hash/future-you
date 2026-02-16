import React, { useState } from 'react';
import { Box, Container, Typography, TextField, Button, Paper, Avatar } from '@mui/material';
import { SmartToy, Person } from '@mui/icons-material';
import { useAppDispatch, useAppSelector } from '../hooks';
import { addChatMessage } from '../slices/companionSlice';
import { companionAPI } from '../services/api';

const Companion: React.FC = () => {
  const [message, setMessage] = useState('');
  const dispatch = useAppDispatch();
  const messages = useAppSelector(state => state.companion.messages);

  const handleSend = async () => {
    if (!message.trim()) return;

    const userMessage = {
      role: 'user' as const,
      content: message,
      timestamp: new Date().toISOString(),
    };
    dispatch(addChatMessage(userMessage));
    setMessage('');

    try {
      const response = await companionAPI.chat(message);
      const companionMessage = {
        role: 'companion' as const,
        content: response.data.response,
        timestamp: new Date().toISOString(),
      };
      dispatch(addChatMessage(companionMessage));
    } catch (err) {
      console.error('Failed to send message', err);
    }
  };

  return (
    <Container maxWidth="md">
      <Box sx={{ mt: 4, mb: 4, height: 'calc(100vh - 200px)', display: 'flex', flexDirection: 'column' }}>
        <Typography variant="h4" gutterBottom>Future Buddy 🤖</Typography>
        <Typography variant="subtitle1" color="text.secondary" gutterBottom>
          Your AI companion for reflection and support
        </Typography>

        <Paper sx={{ flex: 1, p: 2, mb: 2, overflow: 'auto', bgcolor: 'background.default' }}>
          {messages.length === 0 && (
            <Box sx={{ textAlign: 'center', mt: 4 }}>
              <Typography color="text.secondary">
                Start a conversation with your Future Buddy!
              </Typography>
            </Box>
          )}
          
          {messages.map((msg, index) => (
            <Box
              key={index}
              sx={{
                display: 'flex',
                gap: 2,
                mb: 2,
                justifyContent: msg.role === 'user' ? 'flex-end' : 'flex-start',
              }}
            >
              {msg.role === 'companion' && (
                <Avatar sx={{ bgcolor: 'secondary.main' }}>
                  <SmartToy />
                </Avatar>
              )}
              
              <Paper
                sx={{
                  p: 2,
                  maxWidth: '70%',
                  bgcolor: msg.role === 'user' ? 'primary.main' : 'background.paper',
                  color: msg.role === 'user' ? 'white' : 'text.primary',
                }}
              >
                <Typography>{msg.content}</Typography>
              </Paper>
              
              {msg.role === 'user' && (
                <Avatar sx={{ bgcolor: 'primary.main' }}>
                  <Person />
                </Avatar>
              )}
            </Box>
          ))}
        </Paper>

        <Box sx={{ display: 'flex', gap: 1 }}>
          <TextField
            fullWidth
            placeholder="Type your message..."
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSend()}
          />
          <Button variant="contained" onClick={handleSend}>
            Send
          </Button>
        </Box>
      </Box>
    </Container>
  );
};

export default Companion;
