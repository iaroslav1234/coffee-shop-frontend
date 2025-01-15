import React from 'react';
import {
  Box,
  Container,
  Typography,
  Button,
  Paper,
} from '@mui/material';
import ErrorOutlineIcon from '@mui/icons-material/ErrorOutline';
import { useNavigate } from 'react-router-dom';

class ErrorBoundaryClass extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null, errorInfo: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    this.setState({
      error: error,
      errorInfo: errorInfo
    });
    
    // You can also log the error to an error reporting service here
    console.error('Error caught by boundary:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return <ErrorFallback error={this.state.error} />;
    }

    return this.props.children;
  }
}

const ErrorFallback = ({ error }) => {
  const navigate = useNavigate();

  const handleRetry = () => {
    window.location.reload();
  };

  const handleGoHome = () => {
    navigate('/');
    window.location.reload();
  };

  return (
    <Container component="main" maxWidth="sm">
      <Box
        sx={{
          minHeight: '100vh',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
        }}
      >
        <Paper
          elevation={3}
          sx={{
            p: 4,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            backgroundColor: 'rgba(255, 255, 255, 0.95)',
            backdropFilter: 'blur(10px)',
            borderRadius: 2,
          }}
        >
          <ErrorOutlineIcon
            sx={{
              fontSize: 64,
              color: 'error.main',
              mb: 2,
            }}
          />
          <Typography variant="h5" component="h1" gutterBottom>
            Oops! Something went wrong
          </Typography>
          <Typography
            variant="body1"
            color="text.secondary"
            align="center"
            sx={{ mb: 3 }}
          >
            We're sorry for the inconvenience. Please try refreshing the page or
            return to the home page.
          </Typography>
          {process.env.NODE_ENV === 'development' && error && (
            <Typography
              variant="body2"
              component="pre"
              sx={{
                p: 2,
                backgroundColor: 'grey.100',
                borderRadius: 1,
                overflow: 'auto',
                maxWidth: '100%',
                mb: 3,
              }}
            >
              {error.toString()}
            </Typography>
          )}
          <Box sx={{ display: 'flex', gap: 2 }}>
            <Button
              variant="contained"
              onClick={handleRetry}
              sx={{
                background: 'linear-gradient(45deg, #9575cd 30%, #7c4dff 90%)',
                '&:hover': {
                  background: 'linear-gradient(45deg, #7c4dff 30%, #6c3fff 90%)',
                },
              }}
            >
              Try Again
            </Button>
            <Button
              variant="outlined"
              onClick={handleGoHome}
              sx={{
                borderColor: '#7c4dff',
                color: '#7c4dff',
                '&:hover': {
                  borderColor: '#6c3fff',
                  backgroundColor: 'rgba(124, 77, 255, 0.04)',
                },
              }}
            >
              Go to Home
            </Button>
          </Box>
        </Paper>
      </Box>
    </Container>
  );
};

export default ErrorBoundaryClass;
