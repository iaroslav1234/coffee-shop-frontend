# Coffee Shop Manager

A full-stack web application for managing coffee shop operations, including inventory tracking, sales management, and financial reporting.

## Features

- User Authentication (Login/Register)
- Password Reset via Email
- Dashboard with Key Metrics
- Inventory Management
- Sales Tracking
- Financial Reports
- Low Stock Alerts

## Tech Stack

### Frontend
- React
- Material-UI
- React Router
- Context API for State Management

### Backend
- FastAPI
- SQLAlchemy
- PostgreSQL
- JWT Authentication
- Email Integration

## Getting Started

### Prerequisites
- Node.js (v14 or higher)
- Python (v3.8 or higher)
- PostgreSQL

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/coffee-shop-manager.git
cd coffee-shop-manager
```

2. Set up the frontend:
```bash
cd frontend
npm install
cp .env.example .env
# Update .env with your configuration
```

3. Set up the backend:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Update .env with your configuration
```

4. Start the development servers:

Frontend:
```bash
cd frontend
npm start
```

Backend:
```bash
cd backend
uvicorn main:app --reload
```

5. Access the application at `http://localhost:3000`

## Environment Variables

### Frontend (.env)
```
REACT_APP_API_URL=http://localhost:8000
```

### Backend (.env)
```
# Email Configuration
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
FROM_EMAIL=your_email@gmail.com
SUPPORT_EMAIL=support@coffeeshop.com

# Frontend URL
FRONTEND_URL=http://localhost:3000

# JWT Secret
SECRET_KEY=your_secret_key
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
