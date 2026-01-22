# GraphQL Development Guide

Comprehensive guide for building GraphQL APIs and clients in Cursor IDE. Covers schemas, queries, mutations, subscriptions, resolvers, and best practices.

## Overview

GraphQL is a query language and runtime for APIs that provides:
- **Single Endpoint**: One endpoint for all data operations
- **Flexible Queries**: Clients request exactly what they need
- **Strongly Typed**: Schema defines available data and operations
- **Real-time**: Subscriptions for live data updates
- **Introspection**: Self-documenting API with schema discovery

## Setup & Installation

### Apollo Server (Node.js)

```bash
npm install apollo-server graphql
npm install -D @types/node typescript ts-node
```

### Apollo Client (React/Next.js)

```bash
npm install @apollo/client graphql
```

### GraphQL Yoga (Modern Alternative)

```bash
npm install graphql-yoga graphql
```

### GraphQL Code Generator

```bash
npm install -D @graphql-codegen/cli @graphql-codegen/typescript @graphql-codegen/typescript-operations @graphql-codegen/typescript-react-apollo
```

## Schema Definition

### Basic Schema

```typescript
// schema.ts
import { gql } from 'apollo-server';

export const typeDefs = gql`
  type Query {
    hello: String
    user(id: ID!): User
    users: [User!]!
  }

  type Mutation {
    createUser(input: CreateUserInput!): User!
    updateUser(id: ID!, input: UpdateUserInput!): User!
    deleteUser(id: ID!): Boolean!
  }

  type User {
    id: ID!
    name: String!
    email: String!
    posts: [Post!]!
    createdAt: DateTime!
  }

  type Post {
    id: ID!
    title: String!
    content: String!
    author: User!
    createdAt: DateTime!
  }

  input CreateUserInput {
    name: String!
    email: String!
    password: String!
  }

  input UpdateUserInput {
    name: String
    email: String
  }

  scalar DateTime
`;
```

### Schema with Enums

```typescript
export const typeDefs = gql`
  enum UserRole {
    ADMIN
    USER
    GUEST
  }

  enum PostStatus {
    DRAFT
    PUBLISHED
    ARCHIVED
  }

  type User {
    id: ID!
    name: String!
    email: String!
    role: UserRole!
    posts(status: PostStatus): [Post!]!
  }

  type Post {
    id: ID!
    title: String!
    status: PostStatus!
    author: User!
  }
`;
```

### Schema with Interfaces & Unions

```typescript
export const typeDefs = gql`
  interface ContentItem {
    id: ID!
    title: String!
    createdAt: DateTime!
  }

  type Post implements ContentItem {
    id: ID!
    title: String!
    createdAt: DateTime!
    content: String!
    author: User!
  }

  type Page implements ContentItem {
    id: ID!
    title: String!
    createdAt: DateTime!
    slug: String!
    body: String!
  }

  union SearchResult = Post | Page | User

  type Query {
    search(query: String!): [SearchResult!]!
    contentItems: [ContentItem!]!
  }
`;
```

## Resolvers

### Basic Resolvers

```typescript
// resolvers.ts
import { IResolvers } from 'apollo-server';

export const resolvers: IResolvers = {
  Query: {
    hello: () => 'Hello, world!',
    
    user: async (_, { id }, { dataSources }) => {
      return await dataSources.users.getById(id);
    },
    
    users: async (_, __, { dataSources }) => {
      return await dataSources.users.getAll();
    },
  },

  Mutation: {
    createUser: async (_, { input }, { dataSources }) => {
      return await dataSources.users.create(input);
    },
    
    updateUser: async (_, { id, input }, { dataSources }) => {
      return await dataSources.users.update(id, input);
    },
    
    deleteUser: async (_, { id }, { dataSources }) => {
      await dataSources.users.delete(id);
      return true;
    },
  },

  User: {
    posts: async (user, _, { dataSources }) => {
      return await dataSources.posts.getByUserId(user.id);
    },
  },
};
```

### Resolver with Field-Level Authorization

```typescript
import { ForbiddenError } from 'apollo-server';

export const resolvers: IResolvers = {
  Query: {
    user: async (_, { id }, { dataSources, user }) => {
      const userData = await dataSources.users.getById(id);
      
      // Only allow viewing own profile or if admin
      if (user?.id !== id && user?.role !== 'ADMIN') {
        throw new ForbiddenError('Not authorized');
      }
      
      return userData;
    },
  },

  User: {
    email: (user, _, { user: currentUser }) => {
      // Only show email to owner or admins
      if (currentUser?.id === user.id || currentUser?.role === 'ADMIN') {
        return user.email;
      }
      return null;
    },
  },
};
```

### Resolver with DataLoader (N+1 Prevention)

```typescript
import DataLoader from 'dataloader';

// Create DataLoader for batch loading
const createUserLoader = (db: Database) => {
  return new DataLoader(async (ids: readonly string[]) => {
    const users = await db.users.findByIds(Array.from(ids));
    const userMap = new Map(users.map(user => [user.id, user]));
    return ids.map(id => userMap.get(id) || null);
  });
};

export const resolvers: IResolvers = {
  Post: {
    author: async (post, _, { userLoader }) => {
      return await userLoader.load(post.userId);
    },
  },
};

// In context creation
const context = ({ req }) => {
  return {
    userLoader: createUserLoader(db),
  };
};
```

## Apollo Server Setup

### Basic Server

```typescript
// server.ts
import { ApolloServer } from 'apollo-server';
import { typeDefs } from './schema';
import { resolvers } from './resolvers';

const server = new ApolloServer({
  typeDefs,
  resolvers,
  context: ({ req }) => {
    // Extract user from request (JWT, session, etc.)
    const token = req.headers.authorization?.replace('Bearer ', '');
    const user = token ? verifyToken(token) : null;
    
    return { user };
  },
});

server.listen().then(({ url }) => {
  console.log(`Server ready at ${url}`);
});
```

### Server with Data Sources

```typescript
import { ApolloServer } from 'apollo-server';
import { RESTDataSource } from 'apollo-datasource-rest';

class UsersAPI extends RESTDataSource {
  constructor() {
    super();
    this.baseURL = 'https://api.example.com/';
  }

  async getUser(id: string) {
    return this.get(`users/${id}`);
  }

  async getAllUsers() {
    return this.get('users');
  }
}

const server = new ApolloServer({
  typeDefs,
  resolvers,
  dataSources: () => ({
    usersAPI: new UsersAPI(),
  }),
});
```

### Server with File Uploads

```bash
npm install graphql-upload apollo-server-express express
```

```typescript
import { ApolloServer } from 'apollo-server-express';
import express from 'express';
import { graphqlUploadExpress } from 'graphql-upload';

const app = express();

app.use(graphqlUploadExpress({ maxFileSize: 10000000, maxFiles: 10 }));

const server = new ApolloServer({
  typeDefs,
  resolvers,
});

await server.start();
server.applyMiddleware({ app });

app.listen(4000);
```

## Apollo Client (React)

### Client Setup

```typescript
// lib/apollo-client.ts
import { ApolloClient, InMemoryCache, createHttpLink } from '@apollo/client';
import { setContext } from '@apollo/client/link/context';

const httpLink = createHttpLink({
  uri: process.env.NEXT_PUBLIC_GRAPHQL_URL || 'http://localhost:4000/graphql',
});

const authLink = setContext((_, { headers }) => {
  const token = localStorage.getItem('token');
  
  return {
    headers: {
      ...headers,
      authorization: token ? `Bearer ${token}` : '',
    },
  };
});

export const client = new ApolloClient({
  link: authLink.concat(httpLink),
  cache: new InMemoryCache(),
});
```

### Provider Setup

```typescript
// app/layout.tsx or _app.tsx
import { ApolloProvider } from '@apollo/client';
import { client } from '@/lib/apollo-client';

export default function RootLayout({ children }) {
  return (
    <ApolloProvider client={client}>
      {children}
    </ApolloProvider>
  );
}
```

### Using Queries

```typescript
// hooks/useUsers.ts
import { useQuery, gql } from '@apollo/client';

const GET_USERS = gql`
  query GetUsers {
    users {
      id
      name
      email
      posts {
        id
        title
      }
    }
  }
`;

export function useUsers() {
  const { data, loading, error } = useQuery(GET_USERS);

  return {
    users: data?.users || [],
    loading,
    error,
  };
}

// Component usage
function UsersList() {
  const { users, loading, error } = useUsers();

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <ul>
      {users.map(user => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
}
```

### Using Mutations

```typescript
import { useMutation, gql } from '@apollo/client';

const CREATE_USER = gql`
  mutation CreateUser($input: CreateUserInput!) {
    createUser(input: $input) {
      id
      name
      email
    }
  }
`;

function CreateUserForm() {
  const [createUser, { loading, error }] = useMutation(CREATE_USER, {
    refetchQueries: ['GetUsers'], // Refetch after mutation
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    
    try {
      const { data } = await createUser({
        variables: {
          input: {
            name: formData.get('name'),
            email: formData.get('email'),
            password: formData.get('password'),
          },
        },
      });
      
      console.log('User created:', data.createUser);
    } catch (err) {
      console.error('Error:', err);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      {/* Form fields */}
      <button type="submit" disabled={loading}>
        {loading ? 'Creating...' : 'Create User'}
      </button>
      {error && <div>Error: {error.message}</div>}
    </form>
  );
}
```

### Using Subscriptions

```typescript
import { useSubscription, gql } from '@apollo/client';

const POST_CREATED = gql`
  subscription PostCreated {
    postCreated {
      id
      title
      author {
        name
      }
    }
  }
`;

function PostsFeed() {
  const { data, loading } = useSubscription(POST_CREATED);

  if (loading) return <div>Connecting...</div>;

  return (
    <div>
      <h2>New Post</h2>
      {data?.postCreated && (
        <div>
          <h3>{data.postCreated.title}</h3>
          <p>By {data.postCreated.author.name}</p>
        </div>
      )}
    </div>
  );
}
```

### Optimistic Updates

```typescript
const UPDATE_POST = gql`
  mutation UpdatePost($id: ID!, $title: String!) {
    updatePost(id: $id, title: $title) {
      id
      title
    }
  }
`;

function PostEditor({ post }) {
  const [updatePost] = useMutation(UPDATE_POST, {
    optimisticResponse: {
      updatePost: {
        id: post.id,
        title: 'Optimistic title', // Will be replaced with server response
        __typename: 'Post',
      },
    },
    update: (cache, { data }) => {
      // Update cache manually if needed
      cache.modify({
        id: cache.identify(post),
        fields: {
          title: () => data.updatePost.title,
        },
      });
    },
  });

  // ...
}
```

## Fragments

### Defining Fragments

```typescript
import { gql } from '@apollo/client';

const USER_FRAGMENT = gql`
  fragment UserInfo on User {
    id
    name
    email
    avatar
  }
`;

const USER_WITH_POSTS = gql`
  fragment UserWithPosts on User {
    ...UserInfo
    posts {
      id
      title
    }
  }
  ${USER_FRAGMENT}
`;

const GET_USER = gql`
  query GetUser($id: ID!) {
    user(id: $id) {
      ...UserWithPosts
    }
  }
  ${USER_WITH_POSTS}
`;
```

## Error Handling

### Server-Side Error Handling

```typescript
import { ApolloError, UserInputError, ForbiddenError } from 'apollo-server';

export const resolvers: IResolvers = {
  Mutation: {
    createUser: async (_, { input }, { dataSources }) => {
      // Validation
      if (!input.email || !input.email.includes('@')) {
        throw new UserInputError('Invalid email address');
      }

      try {
        const user = await dataSources.users.create(input);
        return user;
      } catch (error) {
        if (error.code === 'DUPLICATE_EMAIL') {
          throw new UserInputError('Email already exists');
        }
        throw new ApolloError('Failed to create user', 'CREATE_USER_ERROR', {
          originalError: error,
        });
      }
    },
  },
};
```

### Client-Side Error Handling

```typescript
import { useQuery } from '@apollo/client';
import { onError } from '@apollo/client/link/error';

const errorLink = onError(({ graphQLErrors, networkError, operation, forward }) => {
  if (graphQLErrors) {
    graphQLErrors.forEach(({ message, locations, path, extensions }) => {
      console.error(
        `GraphQL error: Message: ${message}, Location: ${locations}, Path: ${path}`
      );
      
      if (extensions?.code === 'UNAUTHENTICATED') {
        // Handle auth error
        localStorage.removeItem('token');
        window.location.href = '/login';
      }
    });
  }

  if (networkError) {
    console.error(`Network error: ${networkError}`);
  }
});

// Add to Apollo Client
const client = new ApolloClient({
  link: errorLink.concat(authLink).concat(httpLink),
  cache: new InMemoryCache(),
});
```

## Pagination

### Cursor-Based Pagination

```typescript
// Schema
export const typeDefs = gql`
  type Query {
    posts(first: Int, after: String): PostConnection!
  }

  type PostConnection {
    edges: [PostEdge!]!
    pageInfo: PageInfo!
  }

  type PostEdge {
    node: Post!
    cursor: String!
  }

  type PageInfo {
    hasNextPage: Boolean!
    hasPreviousPage: Boolean!
    startCursor: String
    endCursor: String
  }
`;

// Resolver
export const resolvers: IResolvers = {
  Query: {
    posts: async (_, { first = 10, after }, { dataSources }) => {
      const posts = await dataSources.posts.getPaginated(first, after);
      
      return {
        edges: posts.map(post => ({
          node: post,
          cursor: Buffer.from(post.id).toString('base64'),
        })),
        pageInfo: {
          hasNextPage: posts.length === first,
          hasPreviousPage: !!after,
          startCursor: posts[0] ? Buffer.from(posts[0].id).toString('base64') : null,
          endCursor: posts[posts.length - 1] 
            ? Buffer.from(posts[posts.length - 1].id).toString('base64') 
            : null,
        },
      };
    },
  },
};

// Client query
const GET_POSTS = gql`
  query GetPosts($first: Int, $after: String) {
    posts(first: $first, after: $after) {
      edges {
        node {
          id
          title
        }
        cursor
      }
      pageInfo {
        hasNextPage
        endCursor
      }
    }
  }
`;

// Using fetchMore
function PostsList() {
  const { data, fetchMore, loading } = useQuery(GET_POSTS, {
    variables: { first: 10 },
  });

  const loadMore = () => {
    fetchMore({
      variables: {
        after: data.posts.pageInfo.endCursor,
      },
    });
  };

  return (
    <div>
      {data.posts.edges.map(({ node }) => (
        <div key={node.id}>{node.title}</div>
      ))}
      {data.posts.pageInfo.hasNextPage && (
        <button onClick={loadMore}>Load More</button>
      )}
    </div>
  );
}
```

## Testing

### Testing Resolvers

```typescript
import { createTestClient } from 'apollo-server-testing';
import { ApolloServer } from 'apollo-server';
import { typeDefs } from './schema';
import { resolvers } from './resolvers';

const server = new ApolloServer({
  typeDefs,
  resolvers,
});

const { query, mutate } = createTestClient(server);

describe('User resolvers', () => {
  test('should fetch users', async () => {
    const GET_USERS = gql`
      query GetUsers {
        users {
          id
          name
        }
      }
    `;

    const result = await query({ query: GET_USERS });
    
    expect(result.data.users).toBeDefined();
    expect(Array.isArray(result.data.users)).toBe(true);
  });
});
```

### Testing with Mocking

```typescript
import { MockedProvider } from '@apollo/client/testing';
import { render, screen } from '@testing-library/react';

const mocks = [
  {
    request: {
      query: GET_USERS,
    },
    result: {
      data: {
        users: [
          { id: '1', name: 'User 1' },
          { id: '2', name: 'User 2' },
        ],
      },
    },
  },
];

test('renders users', async () => {
  render(
    <MockedProvider mocks={mocks} addTypename={false}>
      <UsersList />
    </MockedProvider>
  );

  expect(await screen.findByText('User 1')).toBeInTheDocument();
});
```

## Best Practices

### 1. Naming Conventions

```graphql
# ✅ Good: Descriptive, consistent naming
query GetUserById($userId: ID!) {
  user(id: $userId) {
    id
    name
  }
}

mutation CreatePost($input: CreatePostInput!) {
  createPost(input: $input) {
    id
    title
  }
}

# ❌ Avoid: Vague names
query Get($id: ID!) { ... }
mutation Do($data: Data!) { ... }
```

### 2. Use Input Types for Mutations

```graphql
# ✅ Good: Use input types
mutation CreateUser($input: CreateUserInput!) {
  createUser(input: $input) { ... }
}

# ❌ Avoid: Multiple arguments
mutation CreateUser($name: String!, $email: String!, $password: String!) {
  createUser(name: $name, email: $email, password: $password) { ... }
}
```

### 3. Avoid Over-Fetching

```graphql
# ✅ Good: Request only needed fields
query GetUser {
  user(id: "1") {
    id
    name
    email
  }
}

# ❌ Avoid: Fetching all fields
query GetUser {
  user(id: "1") {
    ...allUserFields
  }
}
```

### 4. Use DataLoader for N+1 Problems

Always use DataLoader when resolving relationships to prevent N+1 queries.

### 5. Implement Proper Error Handling

Use appropriate error types (UserInputError, ForbiddenError, ApolloError) and provide helpful error messages.

### 6. Document with Descriptions

```graphql
"""
A user in the system
"""
type User {
  """
  Unique identifier for the user
  """
  id: ID!
  
  """
  User's full name
  """
  name: String!
  
  """
  User's email address (only visible to owner and admins)
  """
  email: String!
}
```

### 7. Use Enums for Constants

```graphql
enum PostStatus {
  DRAFT
  PUBLISHED
  ARCHIVED
}

type Post {
  status: PostStatus!
}
```

### 8. Implement Rate Limiting

```typescript
import rateLimit from 'express-rate-limit';

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
});

app.use('/graphql', limiter);
```

## Checklist for GraphQL Development

Before committing GraphQL-related code:

- [ ] Schema is well-documented with descriptions
- [ ] Input types used for mutations (not multiple arguments)
- [ ] DataLoader implemented for N+1 prevention
- [ ] Error handling implemented (appropriate error types)
- [ ] Authentication/authorization checks in resolvers
- [ ] Pagination implemented for list queries
- [ ] Fragments used for reusable field sets
- [ ] Subscriptions tested (if applicable)
- [ ] Queries are optimized (no over-fetching)
- [ ] Client-side error handling implemented
- [ ] Optimistic updates used where appropriate (mutations)
- [ ] Rate limiting configured (server-side)
- [ ] Schema versioning strategy defined (if breaking changes)
- [ ] Tests written for resolvers and client queries