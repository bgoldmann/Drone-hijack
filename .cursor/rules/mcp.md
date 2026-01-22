# MCP (Model Context Protocol) Integration Guide

Comprehensive guide for integrating and working with Model Context Protocol (MCP) in applications. Covers MCP servers, clients, tools, resources, prompts, security, and best practices.

## Overview

Model Context Protocol (MCP) is an open standard protocol (from Anthropic) for connecting LLMs to external tools, data sources, and prompts via a standardized interface. It enables AI hosts (e.g., Claude, ChatGPT, or custom apps) to call external "skills" in a uniform way.

### Key Components

- **MCP Host**: The AI application that wants to use skills (e.g., Claude Desktop, custom chatbot)
- **MCP Client**: The component in the host that opens and maintains connections to MCP servers
- **MCP Server(s)**: Expose sets of skills:
  - **Tools**: Executable actions with defined inputs/outputs
  - **Resources**: Data, files, databases accessible by the host
  - **Prompts**: Templated instructions that can be invoked

### What Are MCP Skills?

In MCP, a "skill" is one of the following provided by an MCP server:

- A **tool** with a schema (parameters & types), description, and action logic
- A **resource** like documents, code repos, databases
- A **prompt template** for standardized interactions

Skills become discoverable via the MCP server, and the MCP client/host can decide to invoke them based on user input or task determination.

## Protocol Basics

### Transport Protocols

MCP supports JSON-RPC 2.0 over:

- **stdio**: Standard input/output (common for local development)
- **HTTP**: HTTP-based transport for remote servers
- **WebSocket**: Real-time bidirectional communication
- **SSE**: Server-Sent Events for streaming

### Communication Flow

```text
[User] → [AI Host (Agent/Chatbot)]
         ↳ [MCP Client]
             ↳ MCP Server A (Tools + Resources)
             ↳ MCP Server B (DB + Prompt templates)
             ↳ MCP Server C (Cloud APIs)
```

## Setting Up MCP

### Installation

MCP SDKs are available for multiple languages:

#### TypeScript/JavaScript

```bash
npm install @modelcontextprotocol/sdk
```

#### Python

```bash
pip install mcp
```

#### Other Languages

- **C#**: Available via NuGet
- **Java**: Available via Maven/Gradle
- **Rust**: Available via crates.io

### Environment Setup

1. Choose your programming language
2. Select transport protocol based on deployment:
   - **stdio**: Local development, CLI tools
   - **HTTP**: Remote servers, cloud deployments
   - **WebSocket**: Real-time applications
   - **SSE**: Server-sent event streaming

## Building MCP Servers

### TypeScript/JavaScript Server Example

```typescript
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';

const server = new Server(
  {
    name: 'example-server',
    version: '1.0.0',
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// List available tools
server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: 'save-note',
      description: 'Save a note to file',
      inputSchema: {
        type: 'object',
        properties: {
          title: {
            type: 'string',
            description: 'Note title',
          },
          content: {
            type: 'string',
            description: 'Note content',
          },
        },
        required: ['title', 'content'],
      },
    },
  ],
}));

// Handle tool calls
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  if (name === 'save-note') {
    // Implement file writing logic
    const { title, content } = args as { title: string; content: string };
    // ... save to file ...
    return {
      content: [
        {
          type: 'text',
          text: `Note "${title}" saved successfully`,
        },
      ],
    };
  }

  throw new Error(`Unknown tool: ${name}`);
});

// Start server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error('MCP server running on stdio');
}

main().catch(console.error);
```

### Python Server Example

```python
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import json

app = Server("example-server")

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="save-note",
            description="Save a note to file",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Note title"
                    },
                    "content": {
                        "type": "string",
                        "description": "Note content"
                    }
                },
                "required": ["title", "content"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "save-note":
        title = arguments.get("title")
        content = arguments.get("content")
        # Implement file writing logic
        # ...
        return [TextContent(
            type="text",
            text=f'Note "{title}" saved successfully'
        )]
    raise ValueError(f"Unknown tool: {name}")

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

## Defining MCP Skills

### Tools

Tools are executable actions with defined schemas. Define tools with:

- **Name**: Unique identifier
- **Description**: What the tool does
- **Input Schema**: JSON Schema defining parameters
- **Action Logic**: Implementation that performs the action

#### Tool Schema Best Practices

```typescript
{
  name: 'search-database',
  description: 'Search the database for records matching the query',
  inputSchema: {
    type: 'object',
    properties: {
      query: {
        type: 'string',
        description: 'Search query string',
      },
      limit: {
        type: 'number',
        description: 'Maximum number of results',
        default: 10,
      },
      filters: {
        type: 'object',
        description: 'Additional filter criteria',
        properties: {
          status: { type: 'string' },
          dateFrom: { type: 'string', format: 'date' },
        },
      },
    },
    required: ['query'],
  },
}
```

### Resources

Resources are data sources accessible by the host:

```typescript
// List available resources
server.setRequestHandler(ListResourcesRequestSchema, async () => ({
  resources: [
    {
      uri: 'file://notes/example.md',
      name: 'Example Note',
      description: 'An example markdown note',
      mimeType: 'text/markdown',
    },
    {
      uri: 'database://users',
      name: 'Users Database',
      description: 'Access to users table',
      mimeType: 'application/json',
    },
  ],
}));

// Read resource
server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
  const { uri } = request.params;
  
  if (uri.startsWith('file://')) {
    // Read file
    const content = await fs.readFile(uri.replace('file://', ''), 'utf-8');
    return {
      contents: [
        {
          uri,
          mimeType: 'text/markdown',
          text: content,
        },
      ],
    };
  }
  
  // Handle other resource types
});
```

### Prompts

Prompts are templated instructions:

```typescript
server.setRequestHandler(ListPromptsRequestSchema, async () => ({
  prompts: [
    {
      name: 'code-review',
      description: 'Template for code review prompts',
      arguments: [
        {
          name: 'code',
          description: 'The code to review',
          required: true,
        },
        {
          name: 'focus',
          description: 'Focus areas (security, performance, style)',
          required: false,
        },
      ],
    },
  ],
}));

server.setRequestHandler(GetPromptRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;
  
  if (name === 'code-review') {
    const { code, focus = 'general' } = args;
    return {
      messages: [
        {
          role: 'user',
          content: {
            type: 'text',
            text: `Review this code with focus on ${focus}:\n\n\`\`\`\n${code}\n\`\`\``,
          },
        },
      ],
    };
  }
});
```

## MCP Client Implementation

### Connecting to MCP Servers

```typescript
import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js';

const client = new Client(
  {
    name: 'my-client',
    version: '1.0.0',
  },
  {
    capabilities: {},
  }
);

// Connect to server
const transport = new StdioClientTransport({
  command: 'node',
  args: ['server.js'],
});

await client.connect(transport);

// Discover available tools
const { tools } = await client.listTools();
console.log('Available tools:', tools.map(t => t.name));

// Call a tool
const result = await client.callTool({
  name: 'save-note',
  arguments: {
    title: 'My Note',
    content: 'Note content here',
  },
});

console.log('Tool result:', result);
```

### Multi-Server Orchestration

```typescript
// Connect to multiple servers
const servers = {
  files: new Client(/* ... */),
  database: new Client(/* ... */),
  apis: new Client(/* ... */),
};

// Orchestrate tool calls across servers
async function processTask(task: string) {
  // Fetch resource from files server
  const data = await servers.files.readResource({
    uri: 'file://data/input.json',
  });
  
  // Transform using database server tool
  const transformed = await servers.database.callTool({
    name: 'transform-data',
    arguments: { data: data.contents[0].text },
  });
  
  // Send to API via APIs server
  const result = await servers.apis.callTool({
    name: 'send-to-api',
    arguments: { payload: transformed },
  });
  
  return result;
}
```

## Security Best Practices

### Authentication & Authorization

```typescript
// Validate requests
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  // Check authentication token
  const token = request.meta?.authToken;
  if (!isValidToken(token)) {
    throw new Error('Unauthorized');
  }
  
  // Check permissions for specific tools
  if (request.params.name === 'admin-tool' && !hasAdminPermission(token)) {
    throw new Error('Insufficient permissions');
  }
  
  // Continue with tool execution
});
```

### Input Validation

Always validate tool inputs strictly:

```typescript
import { validate } from 'jsonschema';

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;
  
  // Get tool schema
  const tool = tools.find(t => t.name === name);
  if (!tool) {
    throw new Error(`Unknown tool: ${name}`);
  }
  
  // Validate against schema
  const validation = validate(args, tool.inputSchema);
  if (!validation.valid) {
    throw new Error(`Invalid arguments: ${validation.errors.join(', ')}`);
  }
  
  // Proceed with execution
});
```

### Least Privilege

- Tools should expose only necessary functionality
- Servers should run with minimal privileges
- Use sandboxed environments for risky operations
- Limit resource access by permissions

### Audit Logging

```typescript
// Log all tool calls
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;
  
  // Log to audit system
  await auditLogger.log({
    timestamp: new Date(),
    tool: name,
    arguments: sanitizeForLogging(args),
    userId: request.meta?.userId,
  });
  
  // Execute tool
  const result = await executeTool(name, args);
  
  // Log result
  await auditLogger.log({
    timestamp: new Date(),
    tool: name,
    result: 'success',
  });
  
  return result;
});
```

## Error Handling

### Tool Errors

```typescript
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  try {
    const result = await executeTool(request.params);
    return {
      content: [{ type: 'text', text: JSON.stringify(result) }],
    };
  } catch (error) {
    // Return structured error
    return {
      content: [
        {
          type: 'text',
          text: `Error: ${error.message}`,
        },
      ],
      isError: true,
    };
  }
});
```

### Connection Errors

```typescript
// Client-side error handling
try {
  await client.connect(transport);
} catch (error) {
  if (error.code === 'ECONNREFUSED') {
    console.error('Server is not running');
  } else if (error.code === 'ETIMEDOUT') {
    console.error('Connection timeout');
  } else {
    console.error('Connection error:', error);
  }
}

// Reconnection logic
async function connectWithRetry(client, transport, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      await client.connect(transport);
      return;
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      await new Promise(resolve => setTimeout(resolve, 1000 * (i + 1)));
    }
  }
}
```

## Deployment & Scaling

### Local Development (stdio)

```typescript
// Server runs as subprocess
const transport = new StdioClientTransport({
  command: 'node',
  args: ['server.js'],
  env: { NODE_ENV: 'development' },
});
```

### Remote Server (HTTP)

```typescript
// HTTP server
import express from 'express';
import { Server } from '@modelcontextprotocol/sdk/server/index.js';

const app = express();
app.use(express.json());

const mcpServer = new Server(/* ... */);

app.post('/mcp', async (req, res) => {
  // Handle MCP requests over HTTP
  const result = await mcpServer.handleRequest(req.body);
  res.json(result);
});

app.listen(3000);
```

### Production Considerations

- Support concurrent clients/sessions if needed
- Use connection pooling for database resources
- Implement rate limiting for tool calls
- Monitor server health and performance
- Use containerization (Docker) for isolation

## Testing MCP Servers

### Unit Testing Tools

```typescript
import { describe, it, expect } from 'vitest';

describe('MCP Server Tools', () => {
  it('should save a note correctly', async () => {
    const result = await server.handleRequest({
      method: 'tools/call',
      params: {
        name: 'save-note',
        arguments: {
          title: 'Test Note',
          content: 'Test content',
        },
      },
    });
    
    expect(result.content[0].text).toContain('saved successfully');
  });
  
  it('should validate required parameters', async () => {
    await expect(
      server.handleRequest({
        method: 'tools/call',
        params: {
          name: 'save-note',
          arguments: {}, // Missing required params
        },
      })
    ).rejects.toThrow();
  });
});
```

### Integration Testing

```typescript
// Test full client-server interaction
describe('MCP Integration', () => {
  let client: Client;
  let server: Server;
  
  beforeEach(async () => {
    // Setup client and server
    server = createTestServer();
    client = new Client(/* ... */);
    const transport = createTestTransport(server);
    await client.connect(transport);
  });
  
  it('should list and call tools', async () => {
    const { tools } = await client.listTools();
    expect(tools.length).toBeGreaterThan(0);
    
    const result = await client.callTool({
      name: tools[0].name,
      arguments: { /* ... */ },
    });
    
    expect(result).toBeDefined();
  });
});
```

## Versioning & Maintenance

### Tool Versioning

```typescript
const tools = [
  {
    name: 'search-database',
    version: '1.0.0',
    description: 'Search the database',
    // ...
  },
  {
    name: 'search-database',
    version: '2.0.0',
    description: 'Search the database (v2 with filters)',
    // ... new schema
  },
];
```

### Backward Compatibility

- Maintain older tool versions when possible
- Document breaking changes clearly
- Provide migration guides
- Test backward compatibility regularly

### Monitoring & Health Checks

```typescript
// Health check endpoint
app.get('/health', async (req, res) => {
  const health = {
    status: 'healthy',
    uptime: process.uptime(),
    tools: await server.listTools(),
    timestamp: new Date().toISOString(),
  };
  res.json(health);
});
```

## Common Patterns

### Tool Chaining

```typescript
// Chain multiple tool calls
async function processWorkflow(input: string) {
  // Step 1: Parse input
  const parsed = await client.callTool({
    name: 'parse-input',
    arguments: { input },
  });
  
  // Step 2: Validate
  const validated = await client.callTool({
    name: 'validate-data',
    arguments: { data: parsed.content[0].text },
  });
  
  // Step 3: Save
  const saved = await client.callTool({
    name: 'save-result',
    arguments: { data: validated.content[0].text },
  });
  
  return saved;
}
```

### Resource Streaming

```typescript
// Stream large resources
server.setRequestHandler(ReadResourceRequestSchema, async function* (request) {
  const { uri } = request.params;
  const stream = createReadStream(uri);
  
  for await (const chunk of stream) {
    yield {
      contents: [
        {
          uri,
          mimeType: 'text/plain',
          text: chunk.toString(),
        },
      ],
    };
  }
});
```

## Best Practices Summary

1. **Clear Tool Schemas**: Define input/output types clearly so LLM doesn't "guess" wrongly
2. **Prompt Templates**: Use prompt primitives for repeated workflows (summaries, QA, translation)
3. **Discovery & Documentation**: Clients should fetch server metadata; provide good docs
4. **Isolation**: Run tools in sandboxed environments for risky operations
5. **Input Validation**: Always validate tool inputs strictly against schemas
6. **Error Handling**: Return structured errors with clear messages
7. **Security**: Implement authentication, authorization, and audit logging
8. **Monitoring**: Track tool usage, errors, and performance
9. **Versioning**: Maintain backward compatibility when possible
10. **Testing**: Write comprehensive unit and integration tests

## Additional Resources

- **Official Documentation**: <https://modelcontextprotocol.io>
- **GitHub**: <https://github.com/modelcontextprotocol>
- **TypeScript SDK**: <https://github.com/modelcontextprotocol/typescript-sdk>
- **Python SDK**: <https://github.com/modelcontextprotocol/python-sdk>
- **Specification**: <https://spec.modelcontextprotocol.io>
