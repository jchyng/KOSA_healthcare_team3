#!/bin/bash
# FastAPI 백엔드 서버 실행 스크립트
#
# 사용법:
#   - backend 폴더에서: ./scripts/run_server.sh
#   - 프로젝트 root에서: ./backend/scripts/run_server.sh
#   - 어디서든: bash /path/to/healthcare_ai_agent/backend/scripts/run_server.sh

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Get backend directory (one level up from scripts/)
BACKEND_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

# Navigate to backend directory
cd "$BACKEND_DIR"

echo "🚀 Starting FastAPI server..."
echo "📁 Working directory: $BACKEND_DIR"
echo "🌐 Server URL: http://localhost:8000"
echo "📖 API Docs: http://localhost:8000/docs"
echo ""

# Run FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
