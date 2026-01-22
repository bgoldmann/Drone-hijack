# TypeScript Guide

Comprehensive guide for writing type-safe TypeScript code in Cursor IDE. Covers type definitions, advanced types, generics, utility types, and common patterns.

## Core Concepts

### Type Annotations

```typescript
// Primitives
let count: number = 0;
let name: string = "John";
let isActive: boolean = true;
let data: null = null;
let value: undefined = undefined;

// Arrays
let numbers: number[] = [1, 2, 3];
let items: Array<string> = ["a", "b", "c"];

// Objects
let user: { name: string; age: number } = {
  name: "John",
  age: 30,
};

// Functions
function add(a: number, b: number): number {
  return a + b;
}

const multiply = (a: number, b: number): number => a * b;
```

### Type Inference

```typescript
// TypeScript infers types
let count = 0; // number
let name = "John"; // string
const numbers = [1, 2, 3]; // number[]

// Explicit when needed
let result: string | number = getValue(); // Union type
```

## Type Definitions

### Interfaces

```typescript
interface User {
  id: number;
  name: string;
  email: string;
  isActive?: boolean; // Optional property
  readonly createdAt: Date; // Read-only
}

interface AdminUser extends User {
  role: "admin";
  permissions: string[];
}

// Usage
const user: User = {
  id: 1,
  name: "John",
  email: "john@example.com",
  createdAt: new Date(),
};
```

### Type Aliases

```typescript
type UserId = number;
type Email = string;
type Status = "pending" | "active" | "inactive";

type User = {
  id: UserId;
  email: Email;
  status: Status;
};

// Union types
type ID = string | number;

// Intersection types
type Employee = User & {
  department: string;
  salary: number;
};
```

### Classes

```typescript
class User {
  private id: number;
  public name: string;
  protected email: string;
  
  constructor(id: number, name: string, email: string) {
    this.id = id;
    this.name = name;
    this.email = email;
  }
  
  getId(): number {
    return this.id;
  }
}

class Admin extends User {
  constructor(id: number, name: string, email: string, public role: string) {
    super(id, name, email);
  }
}
```

## Advanced Types

### Generics

```typescript
// Generic function
function identity<T>(arg: T): T {
  return arg;
}

const str = identity<string>("hello");
const num = identity(42); // Type inferred

// Generic interface
interface Repository<T> {
  findById(id: number): Promise<T | null>;
  findAll(): Promise<T[]>;
  create(data: Omit<T, "id">): Promise<T>;
}

// Generic class
class DataStore<T> {
  private items: T[] = [];
  
  add(item: T): void {
    this.items.push(item);
  }
  
  get(index: number): T | undefined {
    return this.items[index];
  }
}
```

### Utility Types

```typescript
// Partial - makes all properties optional
type PartialUser = Partial<User>;

// Required - makes all properties required
type RequiredUser = Required<User>;

// Pick - select specific properties
type UserPreview = Pick<User, "id" | "name">;

// Omit - exclude specific properties
type CreateUser = Omit<User, "id" | "createdAt">;

// Record - object with specific keys and values
type UserMap = Record<string, User>;

// Readonly - makes all properties readonly
type ReadonlyUser = Readonly<User>;

// NonNullable - exclude null and undefined
type NonNullString = NonNullable<string | null | undefined>;
```

### Conditional Types

```typescript
type NonNullable<T> = T extends null | undefined ? never : T;

type ApiResponse<T> = T extends string
  ? { message: T }
  : { data: T };

// Infer types
type ReturnType<T> = T extends (...args: any[]) => infer R ? R : never;
```

## Type Guards

```typescript
// Type predicate
function isString(value: unknown): value is string {
  return typeof value === "string";
}

function processValue(value: string | number) {
  if (isString(value)) {
    // TypeScript knows value is string here
    console.log(value.toUpperCase());
  } else {
    // TypeScript knows value is number here
    console.log(value.toFixed(2));
  }
}

// Discriminated unions
type Success = { status: "success"; data: unknown };
type Error = { status: "error"; message: string };
type Result = Success | Error;

function handleResult(result: Result) {
  if (result.status === "success") {
    // TypeScript knows result.data exists
    console.log(result.data);
  } else {
    // TypeScript knows result.message exists
    console.error(result.message);
  }
}
```

## Common Patterns

### Function Overloads

```typescript
function format(value: string): string;
function format(value: number): string;
function format(value: string | number): string {
  if (typeof value === "string") {
    return value.toUpperCase();
  }
  return value.toString();
}
```

### Index Signatures

```typescript
interface StringMap {
  [key: string]: string;
}

const map: StringMap = {
  name: "John",
  email: "john@example.com",
};
```

### Template Literal Types

```typescript
type EventName = `on${string}`;
type EventHandler = `handle${string}Click`;

type ApiEndpoint = `/api/${string}`;
const endpoint: ApiEndpoint = "/api/users";
```

## React with TypeScript

### Component Props

```typescript
interface ButtonProps {
  label: string;
  onClick: () => void;
  variant?: "primary" | "secondary";
  disabled?: boolean;
}

function Button({ label, onClick, variant = "primary", disabled }: ButtonProps) {
  return (
    <button
      onClick={onClick}
      className={variant}
      disabled={disabled}
    >
      {label}
    </button>
  );
}
```

### Hooks

```typescript
function useCounter(initialValue: number = 0) {
  const [count, setCount] = useState<number>(initialValue);
  
  const increment = useCallback(() => {
    setCount(prev => prev + 1);
  }, []);
  
  return { count, increment };
}
```

### Event Handlers

```typescript
function Form() {
  const [email, setEmail] = useState<string>("");
  
  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    // Handle submit
  };
  
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setEmail(e.target.value);
  };
  
  return (
    <form onSubmit={handleSubmit}>
      <input
        type="email"
        value={email}
        onChange={handleChange}
      />
    </form>
  );
}
```

## Async/Await Types

```typescript
async function fetchUser(id: number): Promise<User> {
  const response = await fetch(`/api/users/${id}`);
  return response.json();
}

async function processData(): Promise<void> {
  try {
    const user = await fetchUser(1);
    console.log(user.name);
  } catch (error) {
    if (error instanceof Error) {
      console.error(error.message);
    }
  }
}
```

## Type Assertions

```typescript
// as assertion
const value = document.getElementById("input") as HTMLInputElement;

// <> assertion (not in JSX)
const user = <User>{ id: 1, name: "John" };

// Non-null assertion (use carefully)
const element = document.getElementById("input")!;
```

## Best Practices

### 1. Avoid `any`

```typescript
// BAD
function process(data: any) { }

// GOOD
function process<T>(data: T) { }
// or
function process(data: unknown) { }
```

### 2. Use `unknown` for Untrusted Data

```typescript
function parseUser(data: unknown): User {
  if (typeof data === "object" && data !== null) {
    const obj = data as { id?: number; name?: string };
    if (typeof obj.id === "number" && typeof obj.name === "string") {
      return { id: obj.id, name: obj.name };
    }
  }
  throw new Error("Invalid user data");
}
```

### 3. Prefer Interfaces for Objects

```typescript
// Use interfaces for object shapes
interface User {
  id: number;
  name: string;
}

// Use types for unions, intersections, etc.
type Status = "active" | "inactive";
```

### 4. Use `const` Assertions

```typescript
// Without const assertion
const statuses = ["active", "inactive"]; // string[]

// With const assertion
const statuses = ["active", "inactive"] as const; // readonly ["active", "inactive"]
```

### 5. Strict Mode

```json
// tsconfig.json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true
  }
}
```

## Checklist for TypeScript

Before committing:

- [ ] No `any` types (unless absolutely necessary)
- [ ] All function parameters and return types defined
- [ ] Interfaces/types for all object shapes
- [ ] Error handling with proper types
- [ ] Generic types used where appropriate
- [ ] Utility types used when applicable
- [ ] Type guards for runtime validation
- [ ] Strict mode enabled in tsconfig.json
