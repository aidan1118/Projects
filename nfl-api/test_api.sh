#!/bin/bash

# NFL API Test Script
echo "🧪 Testing NFL API Endpoints..."
echo "================================"

BASE_URL="http://localhost:5001"

# Test basic connection
echo "1. Testing API connection..."
curl -s "$BASE_URL/" | head -5
echo ""

# Test bye weeks
echo "2. Testing bye weeks (2024)..."
curl -s "$BASE_URL/nfl/bye-weeks?year=2024" | head -10
echo ""

# Test team performance for Buffalo Bills
echo "3. Testing team performance (BUF - Buffalo Bills)..."
curl -s "$BASE_URL/nfl/team-performance?year=2024&team=BUF" | head -15
echo ""

# Test all teams performance (first few)
echo "4. Testing all teams performance (first 5 results)..."  
curl -s "$BASE_URL/nfl/team-performance?year=2024" | head -20
echo ""

echo "✅ API test complete!"
echo "🔗 Full API documentation: $BASE_URL/"