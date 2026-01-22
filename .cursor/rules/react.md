# React Development Guide

Comprehensive guide for building React applications in Cursor IDE. Covers components, hooks, state management, patterns, performance optimization, and best practices.

## Overview

React is a JavaScript library for building user interfaces with:
- **Component-Based Architecture**: Reusable, composable UI components
- **Declarative UI**: Describe what UI should look like, React handles updates
- **Virtual DOM**: Efficient updates and rendering
- **Unidirectional Data Flow**: Data flows down, events flow up
- **Hooks**: Modern state and lifecycle management

## Setup & Installation

### Create React App (Traditional)

```bash
npx create-react-app my-app
cd my-app
npm start
```

### Vite (Recommended)

```bash
npm create vite@latest my-app -- --template react
cd my-app
npm install
npm run dev
```

### TypeScript Setup

```bash
# With Vite
npm create vite@latest my-app -- --template react-ts

# Install types
npm install --save-dev @types/react @types/react-dom
```

## Components

### Functional Components (Modern)

```typescript
import React from 'react';

interface ButtonProps {
  label: string;
  onClick: () => void;
  variant?: 'primary' | 'secondary';
}

export function Button({ label, onClick, variant = 'primary' }: ButtonProps) {
  return (
    <button
      className={`btn btn-${variant}`}
      onClick={onClick}
    >
      {label}
    </button>
  );
}
```

### Component Composition

```typescript
// Card component
interface CardProps {
  children: React.ReactNode;
  title?: string;
  footer?: React.ReactNode;
}

export function Card({ children, title, footer }: CardProps) {
  return (
    <div className="card">
      {title && <h3 className="card-title">{title}</h3>}
      <div className="card-body">{children}</div>
      {footer && <div className="card-footer">{footer}</div>}
    </div>
  );
}

// Usage
<Card
  title="User Profile"
  footer={<button>Save</button>}
>
  <p>Content goes here</p>
</Card>
```

### Children Prop Patterns

```typescript
// Pattern 1: Simple children
function Container({ children }: { children: React.ReactNode }) {
  return <div className="container">{children}</div>;
}

// Pattern 2: Render props
function DataFetcher({ render }: { render: (data: any) => React.ReactNode }) {
  const [data, setData] = useState(null);
  // ... fetch data
  return <>{render(data)}</>;
}

// Pattern 3: Slot pattern (named children)
interface LayoutProps {
  header?: React.ReactNode;
  sidebar?: React.ReactNode;
  main: React.ReactNode;
  footer?: React.ReactNode;
}

function Layout({ header, sidebar, main, footer }: LayoutProps) {
  return (
    <div className="layout">
      {header && <header>{header}</header>}
      <div className="content">
        {sidebar && <aside>{sidebar}</aside>}
        <main>{main}</main>
      </div>
      {footer && <footer>{footer}</footer>}
    </div>
  );
}
```

## Hooks

### useState

```typescript
import { useState } from 'react';

function Counter() {
  const [count, setCount] = useState(0);

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>Increment</button>
      <button onClick={() => setCount(prev => prev - 1)}>Decrement</button>
      <button onClick={() => setCount(0)}>Reset</button>
    </div>
  );
}

// Complex state
function Form() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    age: 0,
  });

  const updateField = (field: string, value: string | number) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  return (
    <form>
      <input
        value={formData.name}
        onChange={(e) => updateField('name', e.target.value)}
      />
      <input
        type="email"
        value={formData.email}
        onChange={(e) => updateField('email', e.target.value)}
      />
      <input
        type="number"
        value={formData.age}
        onChange={(e) => updateField('age', parseInt(e.target.value))}
      />
    </form>
  );
}
```

### useEffect

```typescript
import { useEffect, useState } from 'react';

// Basic effect
function DataFetcher({ userId }: { userId: string }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      setLoading(true);
      try {
        const response = await fetch(`/api/users/${userId}`);
        const userData = await response.json();
        setData(userData);
      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, [userId]); // Re-run when userId changes

  if (loading) return <div>Loading...</div>;
  return <div>{JSON.stringify(data)}</div>;
}

// Cleanup effect
function Timer() {
  const [seconds, setSeconds] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setSeconds(prev => prev + 1);
    }, 1000);

    // Cleanup function
    return () => clearInterval(interval);
  }, []); // Empty deps = run once on mount, cleanup on unmount

  return <div>Seconds: {seconds}</div>;
}

// Conditional effect
function WindowSize() {
  const [windowSize, setWindowSize] = useState({
    width: window.innerWidth,
    height: window.innerHeight,
  });

  useEffect(() => {
    function handleResize() {
      setWindowSize({
        width: window.innerWidth,
        height: window.innerHeight,
      });
    }

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return <div>Window: {windowSize.width} x {windowSize.height}</div>;
}
```

### useContext

```typescript
import { createContext, useContext, useState, ReactNode } from 'react';

// Create context
interface ThemeContextType {
  theme: 'light' | 'dark';
  toggleTheme: () => void;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

// Provider component
export function ThemeProvider({ children }: { children: ReactNode }) {
  const [theme, setTheme] = useState<'light' | 'dark'>('light');

  const toggleTheme = () => {
    setTheme(prev => prev === 'light' ? 'dark' : 'light');
  };

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

// Custom hook
export function useTheme() {
  const context = useContext(ThemeContext);
  if (context === undefined) {
    throw new Error('useTheme must be used within ThemeProvider');
  }
  return context;
}

// Usage
function App() {
  return (
    <ThemeProvider>
      <Header />
      <Main />
    </ThemeProvider>
  );
}

function Header() {
  const { theme, toggleTheme } = useTheme();
  return (
    <header className={theme}>
      <button onClick={toggleTheme}>Toggle Theme</button>
    </header>
  );
}
```

### useReducer

```typescript
import { useReducer } from 'react';

// Define state and actions
interface CounterState {
  count: number;
  history: number[];
}

type CounterAction =
  | { type: 'increment' }
  | { type: 'decrement' }
  | { type: 'reset' }
  | { type: 'set'; payload: number };

function counterReducer(state: CounterState, action: CounterAction): CounterState {
  switch (action.type) {
    case 'increment':
      return {
        count: state.count + 1,
        history: [...state.history, state.count + 1],
      };
    case 'decrement':
      return {
        count: state.count - 1,
        history: [...state.history, state.count - 1],
      };
    case 'reset':
      return { count: 0, history: [] };
    case 'set':
      return {
        count: action.payload,
        history: [...state.history, action.payload],
      };
    default:
      return state;
  }
}

function Counter() {
  const [state, dispatch] = useReducer(counterReducer, {
    count: 0,
    history: [],
  });

  return (
    <div>
      <p>Count: {state.count}</p>
      <button onClick={() => dispatch({ type: 'increment' })}>+</button>
      <button onClick={() => dispatch({ type: 'decrement' })}>-</button>
      <button onClick={() => dispatch({ type: 'reset' })}>Reset</button>
      <button onClick={() => dispatch({ type: 'set', payload: 10 })}>Set to 10</button>
      <p>History: {state.history.join(', ')}</p>
    </div>
  );
}
```

### useMemo & useCallback

```typescript
import { useMemo, useCallback, useState } from 'react';

// useMemo: Memoize expensive calculations
function ExpensiveComponent({ items }: { items: number[] }) {
  const expensiveValue = useMemo(() => {
    console.log('Computing expensive value...');
    return items.reduce((sum, item) => sum + item * item, 0);
  }, [items]); // Re-compute only when items change

  return <div>Result: {expensiveValue}</div>;
}

// useCallback: Memoize functions
function ParentComponent() {
  const [count, setCount] = useState(0);
  const [items, setItems] = useState([1, 2, 3]);

  // Without useCallback, this function is recreated on every render
  const handleClick = useCallback(() => {
    console.log('Button clicked');
  }, []); // Stable reference

  // With dependencies
  const handleItemClick = useCallback((id: number) => {
    console.log('Item clicked:', id);
  }, []); // Dependencies: none in this case

  return (
    <div>
      <button onClick={() => setCount(count + 1)}>Count: {count}</button>
      <ChildComponent onClick={handleClick} items={items} />
    </div>
  );
}

function ChildComponent({ onClick, items }: { onClick: () => void; items: number[] }) {
  // This component won't re-render unnecessarily because onClick is stable
  return <button onClick={onClick}>Click me</button>;
}
```

### Custom Hooks

```typescript
// useFetch hook
function useFetch<T>(url: string) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    async function fetchData() {
      try {
        setLoading(true);
        setError(null);
        const response = await fetch(url);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const json = await response.json();
        setData(json);
      } catch (err) {
        setError(err instanceof Error ? err : new Error('Unknown error'));
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, [url]);

  return { data, loading, error };
}

// Usage
function UserProfile({ userId }: { userId: string }) {
  const { data, loading, error } = useFetch<User>(`/api/users/${userId}`);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;
  if (!data) return <div>No user found</div>;

  return <div>{data.name}</div>;
}

// useLocalStorage hook
function useLocalStorage<T>(key: string, initialValue: T) {
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      console.error(error);
      return initialValue;
    }
  });

  const setValue = (value: T | ((val: T) => T)) => {
    try {
      const valueToStore = value instanceof Function ? value(storedValue) : value;
      setStoredValue(valueToStore);
      window.localStorage.setItem(key, JSON.stringify(valueToStore));
    } catch (error) {
      console.error(error);
    }
  };

  return [storedValue, setValue] as const;
}

// Usage
function Settings() {
  const [theme, setTheme] = useLocalStorage<'light' | 'dark'>('theme', 'light');

  return (
    <select value={theme} onChange={(e) => setTheme(e.target.value as 'light' | 'dark')}>
      <option value="light">Light</option>
      <option value="dark">Dark</option>
    </select>
  );
}
```

### useRef

```typescript
import { useRef, useEffect } from 'react';

// Access DOM elements
function TextInputWithFocus() {
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    // Focus input on mount
    inputRef.current?.focus();
  }, []);

  return (
    <div>
      <input ref={inputRef} type="text" />
      <button onClick={() => inputRef.current?.focus()}>Focus Input</button>
    </div>
  );
}

// Store mutable values without causing re-renders
function Timer() {
  const [count, setCount] = useState(0);
  const intervalRef = useRef<NodeJS.Timeout | null>(null);

  const startTimer = () => {
    if (intervalRef.current) return; // Already running

    intervalRef.current = setInterval(() => {
      setCount(prev => prev + 1);
    }, 1000);
  };

  const stopTimer = () => {
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    }
  };

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={startTimer}>Start</button>
      <button onClick={stopTimer}>Stop</button>
    </div>
  );
}
```

## State Management

### Local State (useState/useReducer)

For component-specific state:

```typescript
function TodoItem({ todo }: { todo: Todo }) {
  const [isEditing, setIsEditing] = useState(false);
  const [editText, setEditText] = useState(todo.text);

  // ... component logic
}
```

### Context API (useContext)

For shared state across component tree:

```typescript
// See useContext section above for full example
```

### Lifting State Up

```typescript
// Parent component manages state
function TodoApp() {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [filter, setFilter] = useState<'all' | 'active' | 'completed'>('all');

  const filteredTodos = todos.filter(todo => {
    if (filter === 'active') return !todo.completed;
    if (filter === 'completed') return todo.completed;
    return true;
  });

  return (
    <div>
      <TodoList todos={filteredTodos} onToggle={handleToggle} />
      <TodoFilter filter={filter} onFilterChange={setFilter} />
    </div>
  );
}
```

### External State Management

For complex apps, consider:
- **Redux Toolkit**: Predictable state container
- **Zustand**: Lightweight state management
- **Jotai**: Atomic state management
- **Recoil**: Facebook's state management library

## Event Handling

```typescript
function EventExamples() {
  const handleClick = (e: React.MouseEvent<HTMLButtonElement>) => {
    e.preventDefault();
    console.log('Button clicked');
  };

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    console.log('Form data:', Object.fromEntries(formData));
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    console.log('Input changed:', e.target.value);
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      console.log('Enter pressed');
    }
  };

  return (
    <div>
      <button onClick={handleClick}>Click me</button>
      
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          onChange={handleChange}
          onKeyDown={handleKeyDown}
        />
        <button type="submit">Submit</button>
      </form>
    </div>
  );
}
```

## Conditional Rendering

```typescript
function ConditionalExamples({ user, items }: Props) {
  // if/else
  if (!user) {
    return <div>Please log in</div>;
  }

  // Ternary operator
  return (
    <div>
      {user.isAdmin ? <AdminPanel /> : <UserPanel />}
      
      {/* Logical AND */}
      {user.isVerified && <Badge text="Verified" />}
      
      {/* Multiple conditions */}
      {items.length > 0 ? (
        <ItemList items={items} />
      ) : (
        <EmptyState message="No items found" />
      )}
      
      {/* Early return pattern */}
      {!items.length && <EmptyState />}
    </div>
  );
}
```

## Lists & Keys

```typescript
interface Todo {
  id: string;
  text: string;
  completed: boolean;
}

function TodoList({ todos }: { todos: Todo[] }) {
  return (
    <ul>
      {todos.map(todo => (
        <li key={todo.id}>
          {todo.text}
        </li>
      ))}
    </ul>
  );
}

// Keys should be stable, unique, and predictable
// ❌ Bad: Using index as key when items can reorder
{todos.map((todo, index) => (
  <TodoItem key={index} todo={todo} />
))}

// ✅ Good: Using stable ID
{todos.map(todo => (
  <TodoItem key={todo.id} todo={todo} />
))}
```

## Forms

```typescript
import { useState, FormEvent } from 'react';

function ContactForm() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    message: '',
  });
  const [errors, setErrors] = useState<Record<string, string>>({});

  const validate = () => {
    const newErrors: Record<string, string> = {};
    
    if (!formData.name.trim()) {
      newErrors.name = 'Name is required';
    }
    
    if (!formData.email.trim()) {
      newErrors.email = 'Email is required';
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      newErrors.email = 'Invalid email format';
    }
    
    if (!formData.message.trim()) {
      newErrors.message = 'Message is required';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    
    if (!validate()) {
      return;
    }

    try {
      await fetch('/api/contact', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });
      alert('Message sent!');
      setFormData({ name: '', email: '', message: '' });
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label htmlFor="name">Name</label>
        <input
          id="name"
          type="text"
          value={formData.name}
          onChange={(e) =>
            setFormData(prev => ({ ...prev, name: e.target.value }))
          }
        />
        {errors.name && <span className="error">{errors.name}</span>}
      </div>

      <div>
        <label htmlFor="email">Email</label>
        <input
          id="email"
          type="email"
          value={formData.email}
          onChange={(e) =>
            setFormData(prev => ({ ...prev, email: e.target.value }))
          }
        />
        {errors.email && <span className="error">{errors.email}</span>}
      </div>

      <div>
        <label htmlFor="message">Message</label>
        <textarea
          id="message"
          value={formData.message}
          onChange={(e) =>
            setFormData(prev => ({ ...prev, message: e.target.value }))
          }
        />
        {errors.message && <span className="error">{errors.message}</span>}
      </div>

      <button type="submit">Send</button>
    </form>
  );
}
```

## Performance Optimization

### React.memo

```typescript
import { memo } from 'react';

// Prevent re-renders when props haven't changed
const ExpensiveComponent = memo(function ExpensiveComponent({
  data,
  onAction,
}: {
  data: Data;
  onAction: () => void;
}) {
  // Expensive rendering
  return <div>{/* Complex UI */}</div>;
}, (prevProps, nextProps) => {
  // Custom comparison (optional)
  return prevProps.data.id === nextProps.data.id;
});
```

### useMemo & useCallback

See hooks section above.

### Code Splitting

```typescript
import { lazy, Suspense } from 'react';

// Lazy load component
const HeavyComponent = lazy(() => import('./HeavyComponent'));

function App() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <HeavyComponent />
    </Suspense>
  );
}
```

### Virtual Scrolling (for long lists)

```typescript
import { FixedSizeList } from 'react-window';

function VirtualizedList({ items }: { items: Item[] }) {
  const Row = ({ index, style }: { index: number; style: React.CSSProperties }) => (
    <div style={style}>
      {items[index].name}
    </div>
  );

  return (
    <FixedSizeList
      height={600}
      itemCount={items.length}
      itemSize={35}
      width="100%"
    >
      {Row}
    </FixedSizeList>
  );
}
```

## Error Boundaries

```typescript
import { Component, ErrorInfo, ReactNode } from 'react';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
}

class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
  };

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Error caught by boundary:', error, errorInfo);
    // Log to error reporting service
  }

  public render() {
    if (this.state.hasError) {
      return this.props.fallback || <div>Something went wrong</div>;
    }

    return this.props.children;
  }
}

// Usage
function App() {
  return (
    <ErrorBoundary fallback={<ErrorFallback />}>
      <MyComponent />
    </ErrorBoundary>
  );
}
```

## Testing

### React Testing Library

```typescript
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { Counter } from './Counter';

test('increments counter on button click', () => {
  render(<Counter />);
  
  const button = screen.getByRole('button', { name: /increment/i });
  fireEvent.click(button);
  
  expect(screen.getByText(/count: 1/i)).toBeInTheDocument();
});

test('handles async operations', async () => {
  render(<DataFetcher userId="123" />);
  
  expect(screen.getByText(/loading/i)).toBeInTheDocument();
  
  await waitFor(() => {
    expect(screen.getByText(/user name/i)).toBeInTheDocument();
  });
});
```

## Best Practices

### 1. Component Organization

```
components/
├── Button/
│   ├── Button.tsx
│   ├── Button.test.tsx
│   └── Button.module.css
├── Card/
│   └── index.ts
└── utils/
    └── helpers.ts
```

### 2. Prop Types & Defaults

```typescript
interface ButtonProps {
  label: string;
  variant?: 'primary' | 'secondary';
  disabled?: boolean;
  onClick?: () => void;
}

function Button({
  label,
  variant = 'primary', // Default value
  disabled = false,
  onClick,
}: ButtonProps) {
  // ...
}
```

### 3. Destructuring Props

```typescript
// ✅ Good: Destructure props
function UserCard({ name, email, avatar }: UserCardProps) {
  return <div>{name}</div>;
}

// ❌ Avoid: Access via props object
function UserCard(props: UserCardProps) {
  return <div>{props.name}</div>;
}
```

### 4. Avoid Direct State Mutations

```typescript
// ❌ Bad: Mutating state directly
setItems(items.push(newItem));

// ✅ Good: Creating new array
setItems([...items, newItem]);
setItems(prev => [...prev, newItem]);

// ❌ Bad: Mutating nested object
user.profile.name = 'New Name';

// ✅ Good: Creating new object
setUser({
  ...user,
  profile: { ...user.profile, name: 'New Name' },
});
```

### 5. Extract Complex Logic

```typescript
// Extract business logic from components
function useTodos() {
  const [todos, setTodos] = useState<Todo[]>([]);

  const addTodo = useCallback((text: string) => {
    setTodos(prev => [...prev, { id: Date.now().toString(), text, completed: false }]);
  }, []);

  const toggleTodo = useCallback((id: string) => {
    setTodos(prev =>
      prev.map(todo => (todo.id === id ? { ...todo, completed: !todo.completed } : todo))
    );
  }, []);

  return { todos, addTodo, toggleTodo };
}
```

### 6. Use TypeScript

```typescript
// Define clear interfaces
interface User {
  id: string;
  name: string;
  email: string;
  role: 'admin' | 'user' | 'guest';
}

function UserProfile({ user }: { user: User }) {
  // TypeScript provides autocomplete and type checking
}
```

## Common Patterns

### Controlled vs Uncontrolled Components

```typescript
// Controlled: React controls the input value
function ControlledInput() {
  const [value, setValue] = useState('');
  return <input value={value} onChange={(e) => setValue(e.target.value)} />;
}

// Uncontrolled: DOM controls the input value
function UncontrolledInput() {
  const inputRef = useRef<HTMLInputElement>(null);
  const handleSubmit = () => {
    console.log(inputRef.current?.value);
  };
  return <input ref={inputRef} />;
}
```

### Compound Components

```typescript
// Components that work together
function Tabs({ children }: { children: React.ReactNode }) {
  const [activeTab, setActiveTab] = useState(0);
  
  return (
    <TabsContext.Provider value={{ activeTab, setActiveTab }}>
      {children}
    </TabsContext.Provider>
  );
}

function TabList({ children }: { children: React.ReactNode }) {
  return <div className="tab-list">{children}</div>;
}

function Tab({ index, children }: { index: number; children: React.ReactNode }) {
  const { activeTab, setActiveTab } = useTabsContext();
  return (
    <button
      className={activeTab === index ? 'active' : ''}
      onClick={() => setActiveTab(index)}
    >
      {children}
    </button>
  );
}

// Usage
<Tabs>
  <TabList>
    <Tab index={0}>Tab 1</Tab>
    <Tab index={1}>Tab 2</Tab>
  </TabList>
</Tabs>
```

## Checklist for React Development

Before committing React code:

- [ ] Components are properly typed with TypeScript
- [ ] Props have sensible default values where appropriate
- [ ] State updates use immutable patterns
- [ ] useEffect has proper dependencies and cleanup
- [ ] useMemo/useCallback used for expensive operations
- [ ] Lists have stable, unique keys
- [ ] Error boundaries implemented for error handling
- [ ] Components are tested with React Testing Library
- [ ] Performance optimizations applied where needed (memo, lazy loading)
- [ ] Accessibility attributes (aria-*, role, alt) included
- [ ] Event handlers properly typed
- [ ] No direct DOM mutations outside refs