import React, { useState } from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  IconButton,
  Drawer,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Box,
  Button,
} from '@mui/material';
import {
  Menu as MenuIcon,
  Dashboard,
  Email,
  Chat,
  Analytics,
  LocalShipping,
  AttachMoney,
  Logout,
  Settings,
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { useAppDispatch, useAppSelector } from '../hooks';
import { logout } from '../slices/authSlice';

const Navigation: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [drawerOpen, setDrawerOpen] = useState(false);
  const navigate = useNavigate();
  const dispatch = useAppDispatch();
  const user = useAppSelector(state => state.auth.user);

  const menuItems = [
    { text: 'Dashboard', icon: <Dashboard />, path: '/dashboard' },
    { text: 'Messages', icon: <Email />, path: '/messages' },
    { text: 'AI Companion', icon: <Chat />, path: '/companion' },
    { text: 'Pricing', icon: <AttachMoney />, path: '/pricing' },
    { text: 'Settings', icon: <Settings />, path: '/settings' },
  ];

  const adminItems = [
    { text: 'Analytics', icon: <Analytics />, path: '/analytics' },
    { text: 'Delivery', icon: <LocalShipping />, path: '/delivery' },
  ];

  const handleLogout = () => {
    dispatch(logout());
    navigate('/login');
  };

  return (
    <Box sx={{ display: 'flex' }}>
      <AppBar position="fixed">
        <Toolbar>
          <IconButton
            edge="start"
            color="inherit"
            onClick={() => setDrawerOpen(true)}
            sx={{ mr: 2 }}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" sx={{ flexGrow: 1 }}>
            Future You
          </Typography>
          <Button color="inherit" onClick={handleLogout} startIcon={<Logout />}>
            Logout
          </Button>
        </Toolbar>
      </AppBar>

      <Drawer anchor="left" open={drawerOpen} onClose={() => setDrawerOpen(false)}>
        <Box sx={{ width: 250, pt: 2 }}>
          <Typography variant="h6" sx={{ px: 2, mb: 2 }}>
            Navigation
          </Typography>
          <List>
            {menuItems.map((item) => (
              <ListItem
                button
                key={item.text}
                onClick={() => {
                  navigate(item.path);
                  setDrawerOpen(false);
                }}
              >
                <ListItemIcon>{item.icon}</ListItemIcon>
                <ListItemText primary={item.text} />
              </ListItem>
            ))}
            {user?.is_admin && (
              <>
                <Box sx={{ px: 2, py: 1, mt: 1 }}>
                  <Typography variant="caption" color="text.secondary">
                    ADMIN
                  </Typography>
                </Box>
                {adminItems.map((item) => (
                  <ListItem
                    button
                    key={item.text}
                    onClick={() => {
                      navigate(item.path);
                      setDrawerOpen(false);
                    }}
                  >
                    <ListItemIcon>{item.icon}</ListItemIcon>
                    <ListItemText primary={item.text} />
                  </ListItem>
                ))}
              </>
            )}
          </List>
        </Box>
      </Drawer>

      <Box component="main" sx={{ flexGrow: 1, pt: 8 }}>
        {children}
      </Box>
    </Box>
  );
};

export default Navigation;
