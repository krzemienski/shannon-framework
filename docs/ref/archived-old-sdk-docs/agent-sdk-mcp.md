# MCP in the SDK - Complete Content

## Overview
The documentation explains how Model Context Protocol servers extend Claude Code with custom tools, supporting external processes, HTTP/SSE connections, and SDK-embedded implementations.

## Key Configuration Methods

**Basic Setup:** MCPs are configured in `.mcp.json` at project root, specifying command, arguments, and environment variables for each server.

**SDK Integration:** Both TypeScript and Python SDKs support MCP servers through the `query()` function, accepting server configurations and `allowedTools` parameters.

## Transport Options

1. **stdio Servers:** External processes communicating via stdin/stdout (Node.js or Python)
2. **HTTP/SSE Servers:** Remote servers with network communication, supporting custom headers
3. **SDK MCP Servers:** In-process servers within applications (detailed in Custom Tools guide)

## Resource Management
MCPs expose resources that Claude can list and read using `mcp__list_resources` and `mcp__read_resource` tools.

## Authentication & Security

- **Environment Variables:** Supports dynamic token injection
- **OAuth2:** Not currently supported for in-client MCP authentication

## Error Handling
The system provides connection status monitoring through system events.
