# Paystar Proxy Server (Python)

A Python Flask-based proxy server for handling Paystar API requests. This server acts as an intermediary between your application and the Paystar API endpoints.

## Features

- HTTP proxy for Paystar API requests
- Request/response logging
- Error handling
- Health check endpoint
- CORS support
- Production-ready with Gunicorn
- Virtual environment support

## Requirements

- Python 3.7+
- pip3
- Node.js (for PM2 process management)

## Installation

1. Clone or download this project to your server
2. Navigate to the project directory
3. Install dependencies:

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Development
```bash
# Activate virtual environment
source venv/bin/activate

# Run the application
python app.py
```

### Production with Gunicorn
```bash
# Activate virtual environment
source venv/bin/activate

# Run with Gunicorn
gunicorn -c gunicorn.conf.py app:app
```

## API Endpoints

### Health Check
```
GET /health
```
Returns server status and timestamp.

**Response:**
```json
{
  "status": "ok",
  "timestamp": "2024-01-15T10:30:00.000Z",
  "service": "paystar-proxy"
}
```

### Proxy Request
```
POST /proxy
```

**Request Body:**
```json
{
  "config": {
    "method": "POST",
    "url": "https://core.paystar.ir/api/endpoint",
    "headers": {
      "Content-Type": "application/json",
      "Authorization": "Bearer your-token"
    },
    "data": "your-data"
  }
}
```

**Response:**
```json
{
  "data": "response-from-paystar-api"
}
```

## Deployment on Server 

### 1. Upload Files
Upload the project files to your server .

### 2. Run Deployment Script
```bash
cd /path/to/proxy-server
chmod +x deploy.sh
./deploy.sh
```

### 3. Manual Deployment (Alternative)

#### Install Dependencies
```bash
cd /path/to/proxy-server

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Run with PM2 (Recommended)
```bash
# Install PM2 globally if not already installed
npm install -g pm2

# Start the application
pm2 start main.py --name "paystar-proxy" --interpreter venv/bin/python

# Save PM2 configuration
pm2 save

# Set PM2 to start on boot
pm2 startup
```

#### Run with Systemd (Alternative)
Create a systemd service file:

```bash
sudo nano /etc/systemd/system/paystar-proxy.service
```

Add the following content:
```ini
[Unit]
Description=Paystar Proxy Server
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/path/to/proxy-server
Environment=PATH=/path/to/proxy-server/venv/bin
ExecStart=/path/to/proxy-server/venv/bin/gunicorn -c gunicorn.conf.py app:app
Restart=on-failure
Environment=NODE_ENV=production

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
sudo systemctl enable paystar-proxy
sudo systemctl start paystar-proxy
```

### 4. Configure Firewall
Make sure port 3000 is open:
```bash
sudo ufw allow 3000
```

## Environment Variables

- `PORT`: Server port (default: 3000)

## Logs

The server logs all requests and responses. Check logs with:

### PM2
```bash
pm2 logs paystar-proxy
```

### Systemd
```bash
sudo journalctl -u paystar-proxy -f
```

### Direct Logs
```bash
# Application logs
tail -f proxy.log

# Gunicorn logs
tail -f logs/access.log
tail -f logs/error.log
```

## Security

- CORS is enabled for cross-origin requests
- Request size is limited by Gunicorn configuration
- All errors are logged for monitoring
- Virtual environment isolation

## Testing

Test the proxy server:

```bash
# Health check
curl http://ip:3000/health

# Test proxy
curl -X POST http://ip:3000/proxy \
  -H "Content-Type: application/json" \
  -d '{
    "config": {
      "method": "GET",
      "url": "https://httpbin.org/get"
    }
  }'

# Run Python test script
python3 test_proxy.py
```

## Project Structure

```
proxy-server/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── gunicorn.conf.py   # Gunicorn configuration
├── test_proxy.py      # Test script
├── deploy.sh          # Deployment script
├── README.md          # Documentation
├── venv/              # Virtual environment (created during deployment)
└── logs/              # Log files (created during deployment)
    ├── access.log
    ├── error.log
    └── proxy.log
```

## Troubleshooting

### Common Issues

1. **Port already in use**: Check if another service is using port 3000
2. **Permission denied**: Make sure the deployment script is executable
3. **Python not found**: Ensure Python 3.7+ is installed
4. **Virtual environment issues**: Recreate the virtual environment if needed

### Useful Commands

```bash
# Check PM2 status
pm2 status

# Restart the application
pm2 restart paystar-proxy

# View logs
pm2 logs paystar-proxy

# Check if port is in use
netstat -tulpn | grep :3000

# Check Python version
python3 --version
``` 