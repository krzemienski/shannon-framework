#!/usr/bin/env python3
"""Test WebSocket connection to Shannon Dashboard Server."""

import socketio
import time
import sys

def test_connection():
    """Test Socket.IO connection to the server."""
    print("Testing WebSocket connection to http://localhost:8000...")

    # Create Socket.IO client with polling transport
    sio = socketio.Client(logger=True, engineio_logger=True)

    # Event handlers
    @sio.event
    def connect():
        print("\n✓ Connected to server successfully!")

    @sio.event
    def connected(data):
        print(f"\n✓ Received 'connected' event from server:")
        print(f"  Server version: {data.get('server_version')}")
        print(f"  Capabilities: {data.get('capabilities')}")
        print(f"  Session ID: {data.get('session_id')}")

    @sio.event
    def disconnect():
        print("\n✓ Disconnected from server")

    @sio.event
    def connect_error(data):
        print(f"\n✗ Connection error: {data}")

    try:
        # Connect to server with polling transport
        print("Connecting with polling transport...")
        sio.connect('http://localhost:8000', transports=['polling'])

        # Wait a bit to receive events
        print("Waiting for events...")
        time.sleep(3)

        # Disconnect
        print("Disconnecting...")
        sio.disconnect()

        print("\n✓ WebSocket connection test PASSED")
        return 0

    except Exception as e:
        print(f"\n✗ WebSocket connection test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(test_connection())
