#!/bin/bash

# E-Commerce Application Startup Script

echo "=========================================="
echo "  ShopHub E-Commerce Application"
echo "=========================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Error: Virtual environment not found!"
    echo "Please create a virtual environment first:"
    echo "  python3 -m venv venv"
    exit 1
fi

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "Shutting down servers..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "Servers stopped. Goodbye!"
    exit 0
}

trap cleanup INT TERM

# Start Django backend
echo "Starting Django backend on http://localhost:8000..."
./venv/bin/python manage.py runserver > /dev/null 2>&1 &
BACKEND_PID=$!

# Wait for backend to start
sleep 2

# Start frontend server
echo "Starting frontend on http://localhost:8080..."
cd frontend
python3 server.py > /dev/null 2>&1 &
FRONTEND_PID=$!
cd ..

# Wait for frontend to start
sleep 1

echo ""
echo "=========================================="
echo "  Application is running!"
echo "=========================================="
echo ""
echo "  Backend API: http://localhost:8000"
echo "  Frontend:    http://localhost:8080"
echo ""
echo "  Press Ctrl+C to stop all servers"
echo "=========================================="
echo ""

# Keep script running
wait
