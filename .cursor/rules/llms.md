# LLMs (Large Language Models) Integration Guide

Comprehensive guide for integrating and working with Large Language Models (LLMs) in applications. Covers OpenAI, Anthropic, and other providers, prompt engineering, API patterns, streaming, and best practices.

## Overview

This guide covers integrating LLMs into applications using various providers and APIs. Includes patterns for chat completions, embeddings, fine-tuning, and advanced use cases.

## Provider Overview

### Supported Providers

- **OpenAI**: GPT-4, GPT-3.5, embeddings, fine-tuning
- **Anthropic**: Claude models, advanced reasoning
- **Google**: Gemini, PaLM
- **Mistral**: Open-source models
- **Local Models**: Ollama, LM Studio

## OpenAI Integration

### Setup

```bash
npm install openai
# or
pip install openai
```

### API Client Initialization

#### TypeScript/JavaScript

```typescript
import OpenAI from 'openai';

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

// With organization (optional)
const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
  organization: process.env.OPENAI_ORG_ID,
});
```

#### Python

```python
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)
```

### Basic Chat Completion

#### TypeScript/JavaScript

```typescript
async function getChatCompletion(prompt: string) {
  const completion = await openai.chat.completions.create({
    model: 'gpt-4',
    messages: [
      { role: 'system', content: 'You are a helpful assistant.' },
      { role: 'user', content: prompt },
    ],
    temperature: 0.7,
    max_tokens: 1000,
  });

  return completion.choices[0].message.content;
}
```

#### Python

```python
def get_chat_completion(prompt: str):
    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=1000
    )
    
    return completion.choices[0].message.content
```

### Streaming Responses

#### TypeScript/JavaScript

```typescript
async function streamChatCompletion(prompt: string) {
  const stream = await openai.chat.completions.create({
    model: 'gpt-4',
    messages: [{ role: 'user', content: prompt }],
    stream: true,
  });

  for await (const chunk of stream) {
    const content = chunk.choices[0]?.delta?.content || '';
    process.stdout.write(content);
  }
}
```

#### Next.js API Route with Streaming

```typescript
// app/api/chat/route.ts
import { OpenAI } from 'openai';
import { streamText } from 'ai';

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

export async function POST(req: Request) {
  const { messages } = await req.json();

  const result = await streamText({
    model: openai('gpt-4'),
    messages,
  });

  return result.toDataStreamResponse();
}
```

### Function Calling / Tool Use

```typescript
async function callWithFunctions() {
  const completion = await openai.chat.completions.create({
    model: 'gpt-4',
    messages: [
      { role: 'user', content: 'What is the weather in San Francisco?' },
    ],
    tools: [
      {
        type: 'function',
        function: {
          name: 'get_weather',
          description: 'Get the current weather in a location',
          parameters: {
            type: 'object',
            properties: {
              location: {
                type: 'string',
                description: 'The city and state, e.g. San Francisco, CA',
              },
              unit: {
                type: 'string',
                enum: ['celsius', 'fahrenheit'],
              },
            },
            required: ['location'],
          },
        },
      },
    ],
    tool_choice: 'auto',
  });

  const message = completion.choices[0].message;
  
  if (message.tool_calls) {
    // Handle function calls
    for (const toolCall of message.tool_calls) {
      if (toolCall.function.name === 'get_weather') {
        const args = JSON.parse(toolCall.function.arguments);
        // Call your weather function
        const weather = await getWeather(args.location);
        // Continue conversation with function result
      }
    }
  }
}
```

### Embeddings

```typescript
async function getEmbedding(text: string) {
  const embedding = await openai.embeddings.create({
    model: 'text-embedding-3-small',
    input: text,
  });

  return embedding.data[0].embedding;
}

// Batch embeddings
async function getEmbeddings(texts: string[]) {
  const embeddings = await openai.embeddings.create({
    model: 'text-embedding-3-small',
    input: texts,
  });

  return embeddings.data.map(item => item.embedding);
}
```

## Anthropic (Claude) Integration

### Setup

```bash
npm install @anthropic-ai/sdk
```

### Basic Usage

```typescript
import Anthropic from '@anthropic-ai/sdk';

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

async function getClaudeResponse(prompt: string) {
  const message = await anthropic.messages.create({
    model: 'claude-3-5-sonnet-20241022',
    max_tokens: 1024,
    messages: [
      { role: 'user', content: prompt },
    ],
  });

  return message.content[0].text;
}
```

### Streaming with Anthropic

```typescript
async function streamClaudeResponse(prompt: string) {
  const stream = await anthropic.messages.stream({
    model: 'claude-3-5-sonnet-20241022',
    max_tokens: 1024,
    messages: [
      { role: 'user', content: prompt },
    ],
  });

  for await (const chunk of stream) {
    if (chunk.type === 'content_block_delta') {
      process.stdout.write(chunk.delta.text);
    }
  }
}
```

## Prompt Engineering

### Best Practices

#### 1. Clear Instructions

```typescript
// Good: Clear and specific
const prompt = `
Analyze the following customer review and extract:
1. Overall sentiment (positive, neutral, negative)
2. Key features mentioned
3. Specific complaints or praise

Review: "${review}"
`;

// Bad: Vague
const prompt = "Tell me about this review: ${review}";
```

#### 2. Use System Messages

```typescript
const messages = [
  {
    role: 'system',
    content: 'You are a technical documentation assistant. Provide clear, concise explanations with code examples.',
  },
  {
    role: 'user',
    content: userQuery,
  },
];
```

#### 3. Few-Shot Examples

```typescript
const prompt = `
Classify the sentiment of these reviews:

Review: "Amazing product! Works perfectly."
Sentiment: Positive

Review: "Poor quality, doesn't work as advertised."
Sentiment: Negative

Review: "${newReview}"
Sentiment:
`;
```

#### 4. Chain of Thought

```typescript
const prompt = `
Solve this math problem step by step:
1. Break down the problem
2. Show your work
3. Provide the final answer

Problem: ${mathProblem}
`;
```

### Prompt Templates

```typescript
// Reusable prompt template
function createPromptTemplate(template: string, variables: Record<string, string>) {
  let prompt = template;
  for (const [key, value] of Object.entries(variables)) {
    prompt = prompt.replace(`{${key}}`, value);
  }
  return prompt;
}

const template = `
You are analyzing a {documentType}.

Document: {content}

Please provide:
1. Summary
2. Key points
3. Recommendations
`;

const prompt = createPromptTemplate(template, {
  documentType: 'business proposal',
  content: documentText,
});
```

## Error Handling

### TypeScript/JavaScript

```typescript
async function safeChatCompletion(prompt: string) {
  try {
    const completion = await openai.chat.completions.create({
      model: 'gpt-4',
      messages: [{ role: 'user', content: prompt }],
    });

    return {
      success: true,
      content: completion.choices[0].message.content,
    };
  } catch (error: any) {
    if (error.status === 429) {
      // Rate limit error
      return {
        success: false,
        error: 'Rate limit exceeded. Please try again later.',
      };
    } else if (error.status === 401) {
      // Authentication error
      return {
        success: false,
        error: 'Invalid API key.',
      };
    } else {
      return {
        success: false,
        error: error.message || 'An error occurred',
      };
    }
  }
}
```

### Python

```python
import openai
from openai import APIError, RateLimitError

def safe_chat_completion(prompt: str):
    try:
        completion = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return {
            "success": True,
            "content": completion.choices[0].message.content
        }
    except RateLimitError:
        return {
            "success": False,
            "error": "Rate limit exceeded. Please try again later."
        }
    except APIError as e:
        return {
            "success": False,
            "error": str(e)
        }
```

### Retry Logic

```typescript
async function withRetry<T>(
  fn: () => Promise<T>,
  maxRetries: number = 3,
  delay: number = 1000
): Promise<T> {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error: any) {
      if (i === maxRetries - 1) throw error;
      
      if (error.status === 429) {
        // Exponential backoff for rate limits
        await new Promise(resolve => 
          setTimeout(resolve, delay * Math.pow(2, i))
        );
      } else {
        throw error;
      }
    }
  }
  throw new Error('Max retries exceeded');
}
```

## Token Management

### Token Counting

```typescript
import { encoding_for_model } from 'tiktoken';

function countTokens(text: string, model: string = 'gpt-4'): number {
  const encoding = encoding_for_model(model);
  const tokens = encoding.encode(text);
  return tokens.length;
}

// Estimate cost
function estimateCost(tokens: number, model: string = 'gpt-4'): number {
  const costsPer1k = {
    'gpt-4': 0.03, // Input tokens
    'gpt-4-turbo': 0.01,
    'gpt-3.5-turbo': 0.0005,
  };
  
  return (tokens / 1000) * (costsPer1k[model] || 0.01);
}
```

### Truncation

```typescript
function truncateToTokenLimit(
  text: string,
  maxTokens: number,
  model: string = 'gpt-4'
): string {
  const encoding = encoding_for_model(model);
  const tokens = encoding.encode(text);
  
  if (tokens.length <= maxTokens) {
    return text;
  }
  
  const truncated = tokens.slice(0, maxTokens);
  return encoding.decode(truncated);
}
```

## Common Patterns

### Chat Application

```typescript
// Chat message interface
interface Message {
  role: 'user' | 'assistant' | 'system';
  content: string;
}

class ChatBot {
  private messages: Message[] = [];

  constructor(private systemPrompt?: string) {
    if (systemPrompt) {
      this.messages.push({ role: 'system', content: systemPrompt });
    }
  }

  async sendMessage(userMessage: string): Promise<string> {
    this.messages.push({ role: 'user', content: userMessage });

    const completion = await openai.chat.completions.create({
      model: 'gpt-4',
      messages: this.messages,
    });

    const assistantMessage = completion.choices[0].message.content;
    this.messages.push({ role: 'assistant', content: assistantMessage });

    return assistantMessage;
  }

  clearHistory() {
    this.messages = this.systemPrompt
      ? [{ role: 'system', content: this.systemPrompt }]
      : [];
  }
}
```

### RAG (Retrieval Augmented Generation)

```typescript
async function ragQuery(query: string, documents: string[]) {
  // 1. Get query embedding
  const queryEmbedding = await getEmbedding(query);

  // 2. Get document embeddings
  const docEmbeddings = await getEmbeddings(documents);

  // 3. Find similar documents (cosine similarity)
  const similarities = docEmbeddings.map(embedding => 
    cosineSimilarity(queryEmbedding, embedding)
  );
  
  const topDocs = documents
    .map((doc, i) => ({ doc, similarity: similarities[i] }))
    .sort((a, b) => b.similarity - a.similarity)
    .slice(0, 3)
    .map(item => item.doc);

  // 4. Use relevant docs as context
  const context = topDocs.join('\n\n');
  const prompt = `Use the following context to answer the question:

Context:
${context}

Question: ${query}
Answer:`;

  // 5. Generate response
  return await getChatCompletion(prompt);
}

function cosineSimilarity(a: number[], b: number[]): number {
  const dotProduct = a.reduce((sum, val, i) => sum + val * b[i], 0);
  const magnitudeA = Math.sqrt(a.reduce((sum, val) => sum + val * val, 0));
  const magnitudeB = Math.sqrt(b.reduce((sum, val) => sum + val * val, 0));
  return dotProduct / (magnitudeA * magnitudeB);
}
```

### Text Classification

```typescript
async function classifyText(text: string, categories: string[]) {
  const prompt = `
Classify the following text into one of these categories: ${categories.join(', ')}

Text: "${text}"

Respond with only the category name:
`;

  const response = await getChatCompletion(prompt);
  return response.trim();
}
```

### Summarization

```typescript
async function summarizeText(text: string, maxLength: number = 100) {
  const prompt = `
Summarize the following text in ${maxLength} words or less:

${text}

Summary:
`;

  return await getChatCompletion(prompt);
}
```

## Advanced Features

### Temperature Control

```typescript
// Low temperature (0.0-0.3): More deterministic, focused
const focusedResponse = await openai.chat.completions.create({
  model: 'gpt-4',
  messages: [{ role: 'user', content: prompt }],
  temperature: 0.2, // More consistent
});

// High temperature (0.7-1.0): More creative, varied
const creativeResponse = await openai.chat.completions.create({
  model: 'gpt-4',
  messages: [{ role: 'user', content: prompt }],
  temperature: 0.9, // More creative
});
```

### Top-p Sampling

```typescript
const completion = await openai.chat.completions.create({
  model: 'gpt-4',
  messages: [{ role: 'user', content: prompt }],
  temperature: 0.7,
  top_p: 0.9, // Nucleus sampling
});
```

### Logit Bias

```typescript
// Bias towards certain tokens
const completion = await openai.chat.completions.create({
  model: 'gpt-4',
  messages: [{ role: 'user', content: prompt }],
  logit_bias: {
    'positive': 10, // Encourage "positive"
    'negative': -10, // Discourage "negative"
  },
});
```

## Environment Variables

```bash
# .env.local or .env
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_ORG_ID=org-... # Optional
```

## Best Practices

### 1. API Key Security

```typescript
// Never expose API keys in client-side code
// Use environment variables or server-side only

// Good: Server-side API route
export async function POST(req: Request) {
  const openai = new OpenAI({
    apiKey: process.env.OPENAI_API_KEY, // Server-side only
  });
}

// Bad: Client-side
const openai = new OpenAI({
  apiKey: 'sk-...', // NEVER do this
});
```

### 2. Rate Limiting

```typescript
// Implement client-side rate limiting
class RateLimiter {
  private requests: number[] = [];
  
  constructor(
    private maxRequests: number,
    private windowMs: number
  ) {}

  async waitIfNeeded() {
    const now = Date.now();
    this.requests = this.requests.filter(
      time => now - time < this.windowMs
    );

    if (this.requests.length >= this.maxRequests) {
      const oldest = Math.min(...this.requests);
      const waitTime = this.windowMs - (now - oldest);
      await new Promise(resolve => setTimeout(resolve, waitTime));
    }

    this.requests.push(Date.now());
  }
}
```

### 3. Cost Management

```typescript
// Track token usage
class TokenTracker {
  private totalTokens = 0;
  private totalCost = 0;

  recordUsage(tokens: number, model: string) {
    this.totalTokens += tokens;
    this.totalCost += estimateCost(tokens, model);
  }

  getStats() {
    return {
      totalTokens: this.totalTokens,
      totalCost: this.totalCost.toFixed(4),
    };
  }
}
```

### 4. Prompt Injection Prevention

```typescript
function sanitizeUserInput(input: string): string {
  // Remove potential prompt injection patterns
  const dangerousPatterns = [
    /ignore previous instructions/i,
    /system:/i,
    /assistant:/i,
  ];

  let sanitized = input;
  for (const pattern of dangerousPatterns) {
    sanitized = sanitized.replace(pattern, '');
  }

  return sanitized.trim();
}
```

## Checklist for LLM Integration

Before deploying LLM features:

- [ ] API keys stored in environment variables (never in code)
- [ ] Error handling for API failures
- [ ] Rate limiting implemented
- [ ] Token usage tracked
- [ ] Cost estimates calculated
- [ ] User input sanitized (prompt injection prevention)
- [ ] Streaming implemented for better UX (if applicable)
- [ ] Appropriate model selected (cost vs capability)
- [ ] Temperature and sampling parameters tuned
- [ ] Context window managed (truncation if needed)
- [ ] Retry logic for transient failures
- [ ] Timeout handling configured
- [ ] Logging for debugging and monitoring
