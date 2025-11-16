#!/usr/bin/env python3
"""Verification script for Shannon Dashboard Server.

This script verifies that all server components are correctly installed
and functioning before deployment.

Run: python verify_server.py
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))


def print_header(title):
    """Print section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_success(message):
    """Print success message."""
    print(f"✓ {message}")


def print_error(message):
    """Print error message."""
    print(f"✗ {message}", file=sys.stderr)


def verify_imports():
    """Verify all required imports work."""
    print_header("Verifying Imports")

    try:
        import fastapi
        print_success(f"FastAPI v{fastapi.__version__}")
    except ImportError as e:
        print_error(f"FastAPI import failed: {e}")
        return False

    try:
        import socketio
        print_success(f"Socket.IO v{socketio.__version__}")
    except ImportError as e:
        print_error(f"Socket.IO import failed: {e}")
        return False

    try:
        import uvicorn
        print_success(f"Uvicorn v{uvicorn.__version__}")
    except ImportError as e:
        print_error(f"Uvicorn import failed: {e}")
        return False

    try:
        from shannon.server import app, sio, socket_app
        print_success(f"Shannon Server module: {app.title}")
    except ImportError as e:
        print_error(f"Shannon Server import failed: {e}")
        return False

    try:
        from shannon.server.websocket import (
            ConnectionManager,
            emit_skill_event,
            emit_file_event,
            conn_manager
        )
        print_success("WebSocket module imported successfully")
    except ImportError as e:
        print_error(f"WebSocket module import failed: {e}")
        return False

    return True


def verify_structure():
    """Verify file structure."""
    print_header("Verifying File Structure")

    required_files = [
        "src/shannon/server/__init__.py",
        "src/shannon/server/app.py",
        "src/shannon/server/websocket.py",
        "src/shannon/server/README.md",
        "tests/server/__init__.py",
        "tests/server/test_websocket.py",
        "run_server.py",
        "examples/server_integration.py",
    ]

    all_exist = True
    for file_path in required_files:
        path = Path(file_path)
        if path.exists():
            print_success(f"{file_path}")
        else:
            print_error(f"{file_path} - NOT FOUND")
            all_exist = False

    return all_exist


def verify_app_config():
    """Verify FastAPI app configuration."""
    print_header("Verifying App Configuration")

    try:
        from shannon.server import app

        # Check title
        if app.title == "Shannon Dashboard Server":
            print_success("App title correct")
        else:
            print_error(f"App title incorrect: {app.title}")
            return False

        # Check version
        if app.version == "4.0.0":
            print_success("App version correct")
        else:
            print_error(f"App version incorrect: {app.version}")
            return False

        # Check CORS middleware
        has_cors = any(
            middleware.__class__.__name__ == 'CORSMiddleware'
            for middleware in app.user_middleware
        )
        if has_cors:
            print_success("CORS middleware configured")
        else:
            print_error("CORS middleware missing")
            return False

        # Check routes
        routes = [route.path for route in app.routes]
        required_routes = ["/health", "/api/skills"]
        for route in required_routes:
            if route in routes:
                print_success(f"Route {route} registered")
            else:
                print_error(f"Route {route} missing")
                return False

        return True

    except Exception as e:
        print_error(f"App configuration check failed: {e}")
        return False


def verify_socketio():
    """Verify Socket.IO configuration."""
    print_header("Verifying Socket.IO Configuration")

    try:
        from shannon.server import sio

        # Check async mode
        if sio.async_mode == 'asgi':
            print_success("Socket.IO async mode: ASGI")
        else:
            print_error(f"Socket.IO async mode incorrect: {sio.async_mode}")
            return False

        # Check CORS
        if sio.cors_allowed_origins == '*':
            print_success("Socket.IO CORS configured")
        else:
            print_error("Socket.IO CORS not configured")
            return False

        print_success("Socket.IO server configured correctly")
        return True

    except Exception as e:
        print_error(f"Socket.IO configuration check failed: {e}")
        return False


def verify_connection_manager():
    """Verify ConnectionManager functionality."""
    print_header("Verifying Connection Manager")

    try:
        from shannon.server.websocket import conn_manager, ExecutionState

        # Check initial state
        if hasattr(conn_manager, 'connections'):
            print_success("Connection tracking initialized")
        else:
            print_error("Connection tracking missing")
            return False

        if hasattr(conn_manager, 'session_rooms'):
            print_success("Session room tracking initialized")
        else:
            print_error("Session room tracking missing")
            return False

        if hasattr(conn_manager, 'execution_state'):
            print_success("Execution state tracking initialized")
        else:
            print_error("Execution state tracking missing")
            return False

        # Check execution states
        states = [ExecutionState.RUNNING, ExecutionState.HALTED,
                 ExecutionState.COMPLETED, ExecutionState.FAILED]
        print_success(f"ExecutionState enum: {len(states)} states")

        return True

    except Exception as e:
        print_error(f"Connection manager check failed: {e}")
        return False


def run_tests():
    """Run test suite."""
    print_header("Running Test Suite")

    import subprocess

    try:
        result = subprocess.run(
            ["python", "-m", "pytest", "tests/server/test_websocket.py", "-v",
             "--tb=short", "-q"],
            capture_output=True,
            text=True,
            timeout=30
        )

        # Check if tests passed
        if result.returncode == 0:
            # Count passed tests
            output = result.stdout
            if "30 passed" in output:
                print_success("All 30 tests passed")
                return True
            else:
                print_error(f"Not all tests passed:\n{output}")
                return False
        else:
            print_error(f"Tests failed:\n{result.stdout}\n{result.stderr}")
            return False

    except subprocess.TimeoutExpired:
        print_error("Tests timed out after 30 seconds")
        return False
    except Exception as e:
        print_error(f"Test execution failed: {e}")
        return False


def main():
    """Run all verification checks."""
    print("\n" + "=" * 70)
    print("  Shannon Dashboard Server - Verification Script")
    print("=" * 70)

    checks = [
        ("Imports", verify_imports),
        ("File Structure", verify_structure),
        ("App Configuration", verify_app_config),
        ("Socket.IO Configuration", verify_socketio),
        ("Connection Manager", verify_connection_manager),
        ("Test Suite", run_tests),
    ]

    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print_error(f"Verification failed: {e}")
            results.append((name, False))

    # Summary
    print_header("Verification Summary")

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status:8} {name}")

    print()
    print(f"Results: {passed}/{total} checks passed")

    if passed == total:
        print()
        print("=" * 70)
        print("  ✓ ALL CHECKS PASSED - SERVER IS PRODUCTION READY!")
        print("=" * 70)
        print()
        print("Next steps:")
        print("  1. Start server: python run_server.py --reload")
        print("  2. Test connection: curl http://localhost:8000/health")
        print("  3. View docs: http://localhost:8000/api/docs")
        return 0
    else:
        print()
        print("=" * 70)
        print("  ✗ SOME CHECKS FAILED - PLEASE FIX ISSUES ABOVE")
        print("=" * 70)
        return 1


if __name__ == '__main__':
    sys.exit(main())
