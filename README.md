# 1C Accounting MCP Server

MCP server for 1C Enterprise Accounting integration with AI assistants.

## Quick Start

### Run via NPX (Recommended)
\\\ash
npx @tarasov46/1c-accounting-mcp
\\\

### Global Installation
\\\ash
npm install -g @tarasov46/1c-accounting-mcp
1c-accounting-mcp
\\\

## System Requirements

- **Node.js**: 16.0.0+ (for NPX launcher)
- **Python**: 3.8+ (for MCP server)
- **pip**: for Python dependencies installation

NPX launcher automatically checks and installs Python dependencies on first run.

## Available Tools

| Tool | Description | Parameters |
|------|-------------|------------|
| \hello_1c\ | Server greeting and information | \
ame\ (string) |
| \	est_calculation\ | Test calculator | \\, \\ (numbers), \operation\ |
| \generate_test_data\ | Generate test data | \count\ (number) |

## Configuration

### Claude Desktop
\\\json
{
  "mcpServers": {
    "1c-accounting": {
      "command": "npx",
      "args": ["@tarasov46/1c-accounting-mcp"]
    }
  }
}
\\\

### n8n
1. Install MCP Client community node
2. Configure MCP Client credentials:
   - **Transport**: Command Line
   - **Command**: \
px\
   - **Args**: \["@tarasov46/1c-accounting-mcp"]\

## Local Development

\\\ash
git clone https://github.com/tarasov46/1c-accounting-mcp.git
cd 1c-accounting-mcp
pip install -r requirements.txt
node bin/index.js
\\\

## License

MIT License
