#!/bin/bash

# Paystar Proxy Server Deployment Script (Python)
# Run this script on your server (94.101.187.180)

echo "🚀 Starting Paystar Proxy Server deployment (Python)..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Check if pip3 is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip3 first."
    exit 1
fi

echo "✅ Python 3 and pip3 are installed"

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "📋 Python version: $PYTHON_VERSION"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

if [ $? -ne 0 ]; then
    echo "❌ Failed to create virtual environment"
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✅ Dependencies installed successfully"

# Create logs directory
echo "📁 Creating logs directory..."
mkdir -p logs

# Check if PM2 is installed
if ! command -v pm2 &> /dev/null; then
    echo "📦 Installing PM2 globally..."
    npm install -g pm2
fi

# Stop existing process if running
echo "🛑 Stopping existing process..."
pm2 stop paystar-proxy 2>/dev/null || true
pm2 delete paystar-proxy 2>/dev/null || true

# Start the application with PM2
echo "🚀 Starting application with PM2..."
pm2 start main.py --name "paystar-proxy" --interpreter venv/bin/python

if [ $? -ne 0 ]; then
    echo "❌ Failed to start application"
    exit 1
fi

# Save PM2 configuration
echo "💾 Saving PM2 configuration..."
pm2 save

# Set PM2 to start on boot
echo "🔧 Setting PM2 to start on boot..."
pm2 startup

echo "✅ Deployment completed successfully!"
echo ""
echo "📊 Application status:"
pm2 status
echo ""
echo "📝 Logs:"
echo "  - PM2 logs: pm2 logs paystar-proxy"
echo "  - Application logs: tail -f proxy.log"
echo ""
echo "🌐 Health check: http://localhost:3000/health"
echo "🔗 Proxy endpoint: http://localhost:3000/proxy"
echo ""
echo "🧪 To test the proxy server:"
echo "  python3 test_proxy.py" 