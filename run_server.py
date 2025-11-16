#!/usr/bin/env python3
"""Shannon Dashboard Server - Development Runner.

Start the FastAPI server with Socket.IO for development and testing.

Usage:
    python run_server.py [--host HOST] [--port PORT] [--reload]

Examples:
    # Default: localhost:8000
    python run_server.py

    # Custom host/port
    python run_server.py --host 0.0.0.0 --port 5000

    # With auto-reload for development
    python run_server.py --reload
"""

import argparse
import logging
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

import uvicorn

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)


def main():
    """Run the Shannon Dashboard Server."""
    parser = argparse.ArgumentParser(description='Shannon Dashboard Server')
    parser.add_argument(
        '--host',
        default='127.0.0.1',
        help='Host to bind to (default: 127.0.0.1)'
    )
    parser.add_argument(
        '--port',
        type=int,
        default=8000,
        help='Port to bind to (default: 8000)'
    )
    parser.add_argument(
        '--reload',
        action='store_true',
        help='Enable auto-reload for development'
    )
    parser.add_argument(
        '--log-level',
        default='info',
        choices=['debug', 'info', 'warning', 'error'],
        help='Logging level (default: info)'
    )

    args = parser.parse_args()

    logger.info("=" * 70)
    logger.info("Shannon Dashboard Server v4.0.0")
    logger.info("=" * 70)
    logger.info(f"Host: {args.host}")
    logger.info(f"Port: {args.port}")
    logger.info(f"Auto-reload: {args.reload}")
    logger.info(f"Log level: {args.log_level}")
    logger.info("=" * 70)
    logger.info("")
    logger.info("Endpoints:")
    logger.info(f"  Health Check:  http://{args.host}:{args.port}/health")
    logger.info(f"  API Docs:      http://{args.host}:{args.port}/api/docs")
    logger.info(f"  WebSocket:     ws://{args.host}:{args.port}/socket.io")
    logger.info("")
    logger.info("Press CTRL+C to stop the server")
    logger.info("=" * 70)

    try:
        # Run server with Socket.IO ASGI app
        uvicorn.run(
            "shannon.server:socket_app",
            host=args.host,
            port=args.port,
            reload=args.reload,
            log_level=args.log_level,
            access_log=True
        )
    except KeyboardInterrupt:
        logger.info("\nServer stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
