@echo off
REM FastAPI 백엔드 서버 실행 스크립트 (Windows용)
REM
REM 사용법:
REM   - backend 폴더에서: scripts\run_server.bat
REM   - 프로젝트 root에서: backend\scripts\run_server.bat

REM 현재 스크립트 위치 찾기
set SCRIPT_DIR=%~dp0
REM backend 디렉토리로 이동 (scripts의 상위 폴더)
cd /d "%SCRIPT_DIR%.."

echo.
echo Starting FastAPI server...
echo Working directory: %CD%
echo Server URL: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.

REM 가상환경 활성화 후 서버 실행
call venv\Scripts\activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
