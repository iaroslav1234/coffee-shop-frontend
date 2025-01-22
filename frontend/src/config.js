const config = {
    apiUrl: process.env.NODE_ENV === 'development' 
        ? 'http://localhost:9999'
        : 'https://coffee-shop-backend-production.up.railway.app'
};

export default config;
