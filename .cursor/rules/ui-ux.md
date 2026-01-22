# UI/UX Design Guidelines

Comprehensive guide for creating user-friendly, accessible, and effective user interfaces in Cursor IDE. Covers design principles, accessibility standards, user experience patterns, and implementation best practices.

## Core Principles

1. **User-Centered Design**: Design for users, not developers
2. **Accessibility First**: Make interfaces usable by everyone
3. **Progressive Enhancement**: Start with core functionality, enhance progressively
4. **Consistent Patterns**: Use familiar patterns users recognize
5. **Feedback & Affordance**: Users should understand what they can do and what happened

## Accessibility (a11y)

### Semantic HTML

Use proper HTML elements for their intended purpose:

```html
<!-- GOOD - Semantic HTML -->
<nav>
  <ul>
    <li><a href="/">Home</a></li>
    <li><a href="/about">About</a></li>
  </ul>
</nav>

<main>
  <article>
    <h1>Article Title</h1>
    <p>Content...</p>
  </article>
</main>

<!-- BAD - Div soup -->
<div class="nav">
  <div><div onclick="...">Home</div></div>
</div>
```

### ARIA Labels

Use ARIA when semantic HTML isn't enough:

```typescript
// Button without visible text (icon only)
<button aria-label="Close dialog">
  <XIcon />
</button>

// Loading state
<div role="status" aria-live="polite">
  {isLoading ? 'Loading...' : content}
</div>

// Form errors
<input
  aria-invalid={hasError}
  aria-describedby={hasError ? 'email-error' : undefined}
/>
{hasError && (
  <span id="email-error" role="alert">
    Please enter a valid email
  </span>
)}
```

### Keyboard Navigation

Ensure all interactive elements are keyboard accessible:

```typescript
// Focusable elements
<button>Click me</button>
<a href="/page">Link</a>
<input type="text" />

// Custom interactive elements
<div
  role="button"
  tabIndex={0}
  onKeyDown={(e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      handleClick();
    }
  }}
>
  Custom Button
</div>

// Skip to main content
<a href="#main-content" className="skip-link">
  Skip to main content
</a>
```

### Color Contrast

Ensure sufficient color contrast (WCAG AA minimum):

- **Normal text**: 4.5:1 contrast ratio
- **Large text** (18pt+): 3:1 contrast ratio
- **Interactive elements**: 3:1 contrast ratio for their states

```css
/* Good contrast */
.text-primary {
  color: #1a1a1a; /* Dark on light */
  background: #ffffff;
}

.text-secondary {
  color: #ffffff; /* Light on dark */
  background: #1a1a1a;
}

/* Test with tools: WebAIM Contrast Checker */
```

### Screen Reader Support

```typescript
// Descriptive labels
<label htmlFor="email">Email Address</label>
<input type="email" id="email" name="email" />

// Alt text for images
<img src="chart.png" alt="Sales increased 25% in Q3 2024" />

// Decorative images
<img src="decoration.png" alt="" aria-hidden="true" />

// Status announcements
<div role="status" aria-live="polite" aria-atomic="true">
  {notificationMessage}
</div>
```

## User Experience Patterns

### Loading States

Provide feedback during async operations:

```typescript
// Loading spinner
function LoadingButton() {
  const [isLoading, setIsLoading] = useState(false);
  
  return (
    <button disabled={isLoading}>
      {isLoading ? (
        <>
          <Spinner />
          Loading...
        </>
      ) : (
        'Submit'
      )}
    </button>
  );
}

// Skeleton loading
function UserCardSkeleton() {
  return (
    <div className="animate-pulse">
      <div className="h-8 bg-gray-200 rounded w-3/4 mb-2" />
      <div className="h-4 bg-gray-200 rounded w-1/2" />
    </div>
  );
}
```

### Error States

Clear, actionable error messages:

```typescript
// Form validation errors
function EmailInput() {
  const [error, setError] = useState('');
  
  return (
    <div>
      <label htmlFor="email">Email</label>
      <input
        id="email"
        type="email"
        aria-invalid={!!error}
        aria-describedby={error ? 'email-error' : undefined}
        onChange={(e) => {
          const value = e.target.value;
          if (!value.includes('@')) {
            setError('Please enter a valid email address');
          } else {
            setError('');
          }
        }}
      />
      {error && (
        <span id="email-error" role="alert" className="error">
          {error}
        </span>
      )}
    </div>
  );
}

// API error handling
function ErrorMessage({ error, onRetry }) {
  return (
    <div role="alert" className="error-container">
      <p>Something went wrong: {error.message}</p>
      <button onClick={onRetry}>Try Again</button>
    </div>
  );
}
```

### Empty States

Helpful empty states guide users:

```typescript
function EmptyState({ title, description, action }) {
  return (
    <div className="empty-state">
      <EmptyIcon />
      <h2>{title}</h2>
      <p>{description}</p>
      {action && <button onClick={action.handler}>{action.label}</button>}
    </div>
  );
}

// Usage
{items.length === 0 && (
  <EmptyState
    title="No items yet"
    description="Get started by creating your first item"
    action={{
      label: 'Create Item',
      handler: () => createItem()
    }}
  />
)}
```

### Success Feedback

Confirm successful actions:

```typescript
// Toast notifications
function useToast() {
  const [toast, setToast] = useState(null);
  
  const showToast = (message) => {
    setToast(message);
    setTimeout(() => setToast(null), 3000);
  };
  
  return { toast, showToast };
}

// Visual feedback
function CheckoutButton() {
  const [isSuccess, setIsSuccess] = useState(false);
  
  const handleCheckout = async () => {
    await processCheckout();
    setIsSuccess(true);
  };
  
  return (
    <button
      className={isSuccess ? 'success' : ''}
      onClick={handleCheckout}
    >
      {isSuccess ? '✓ Order Placed!' : 'Place Order'}
    </button>
  );
}
```

### Confirmation Dialogs

Prevent destructive actions:

```typescript
function DeleteButton({ onDelete }) {
  const [showConfirm, setShowConfirm] = useState(false);
  
  return (
    <>
      <button onClick={() => setShowConfirm(true)}>Delete</button>
      {showConfirm && (
        <Dialog role="alertdialog">
          <h2>Delete Item?</h2>
          <p>This action cannot be undone.</p>
          <button onClick={() => {
            onDelete();
            setShowConfirm(false);
          }}>
            Delete
          </button>
          <button onClick={() => setShowConfirm(false)}>
            Cancel
          </button>
        </Dialog>
      )}
    </>
  );
}
```

## Visual Design

### Typography Hierarchy

Clear visual hierarchy:

```css
/* Typography scale */
.text-xs { font-size: 0.75rem; }    /* 12px */
.text-sm { font-size: 0.875rem; }   /* 14px */
.text-base { font-size: 1rem; }     /* 16px */
.text-lg { font-size: 1.125rem; }   /* 18px */
.text-xl { font-size: 1.25rem; }    /* 20px */
.text-2xl { font-size: 1.5rem; }    /* 24px */
.text-3xl { font-size: 1.875rem; }  /* 30px */

/* Usage */
<h1 className="text-3xl font-bold">Page Title</h1>
<h2 className="text-2xl font-semibold">Section Title</h2>
<p className="text-base">Body text</p>
```

### Spacing System

Consistent spacing:

```css
/* 8px base unit */
.spacing-xs { margin: 0.25rem; }   /* 4px */
.spacing-sm { margin: 0.5rem; }    /* 8px */
.spacing-md { margin: 1rem; }      /* 16px */
.spacing-lg { margin: 1.5rem; }    /* 24px */
.spacing-xl { margin: 2rem; }      /* 32px */
```

### Color System

Semantic color usage:

```css
/* Status colors */
.success { color: #10b981; }  /* Green */
.error { color: #ef4444; }     /* Red */
.warning { color: #f59e0b; }   /* Amber */
.info { color: #3b82f6; }      /* Blue */

/* Background colors */
.bg-primary { background: #ffffff; }
.bg-secondary { background: #f3f4f6; }
.bg-accent { background: #3b82f6; }
```

### Responsive Design

Mobile-first approach:

```css
/* Mobile-first breakpoints */
.container {
  width: 100%;
  padding: 1rem;
}

@media (min-width: 640px) {
  .container {
    padding: 1.5rem;
  }
}

@media (min-width: 1024px) {
  .container {
    max-width: 1200px;
    margin: 0 auto;
  }
}
```

```typescript
// Responsive components
function ResponsiveGrid({ items }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {items.map(item => (
        <Card key={item.id} item={item} />
      ))}
    </div>
  );
}
```

## Interaction Design

### Button States

Clear interactive states:

```css
.button {
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  transition: all 0.2s;
  cursor: pointer;
}

.button:hover {
  opacity: 0.9;
  transform: translateY(-1px);
}

.button:active {
  transform: translateY(0);
}

.button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
```

### Form Design

User-friendly forms:

```typescript
function FormInput({ label, error, ...props }) {
  return (
    <div className="form-group">
      <label htmlFor={props.id} className="form-label">
        {label}
        {props.required && <span aria-label="required">*</span>}
      </label>
      <input
        {...props}
        className={`form-input ${error ? 'error' : ''}`}
        aria-invalid={!!error}
        aria-describedby={error ? `${props.id}-error` : undefined}
      />
      {error && (
        <span id={`${props.id}-error`} className="error-message" role="alert">
          {error}
        </span>
      )}
    </div>
  );
}
```

### Navigation Patterns

Clear navigation:

```typescript
// Breadcrumbs
function Breadcrumbs({ items }) {
  return (
    <nav aria-label="Breadcrumb">
      <ol>
        {items.map((item, index) => (
          <li key={item.path}>
            {index < items.length - 1 ? (
              <>
                <a href={item.path}>{item.label}</a>
                <span aria-hidden="true"> / </span>
              </>
            ) : (
              <span aria-current="page">{item.label}</span>
            )}
          </li>
        ))}
      </ol>
    </nav>
  );
}

// Tab navigation
function Tabs({ tabs, activeTab, onTabChange }) {
  return (
    <div role="tablist">
      {tabs.map(tab => (
        <button
          key={tab.id}
          role="tab"
          aria-selected={activeTab === tab.id}
          aria-controls={`panel-${tab.id}`}
          onClick={() => onTabChange(tab.id)}
        >
          {tab.label}
        </button>
      ))}
    </div>
  );
}
```

## Performance & UX

### Optimistic Updates

Instant feedback:

```typescript
function LikeButton({ postId }) {
  const [liked, setLiked] = useState(false);
  
  const handleLike = async () => {
    // Optimistically update UI
    setLiked(true);
    
    try {
      await likePost(postId);
    } catch (error) {
      // Rollback on error
      setLiked(false);
      showError('Failed to like post');
    }
  };
  
  return (
    <button onClick={handleLike} aria-label={liked ? 'Unlike' : 'Like'}>
      {liked ? '❤️' : '🤍'}
    </button>
  );
}
```

### Debouncing & Throttling

Improve performance:

```typescript
// Debounce search input
function SearchInput() {
  const [query, setQuery] = useState('');
  
  const debouncedSearch = useMemo(
    () => debounce((value: string) => {
      performSearch(value);
    }, 300),
    []
  );
  
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setQuery(value);
    debouncedSearch(value);
  };
  
  return <input value={query} onChange={handleChange} />;
}
```

### Progressive Loading

Load content progressively:

```typescript
// Lazy load images
function LazyImage({ src, alt }) {
  return (
    <img
      src={src}
      alt={alt}
      loading="lazy"
      decoding="async"
    />
  );
}

// Infinite scroll
function InfiniteList({ fetchMore }) {
  const observerRef = useRef();
  
  useEffect(() => {
    const observer = new IntersectionObserver((entries) => {
      if (entries[0].isIntersecting) {
        fetchMore();
      }
    });
    
    if (observerRef.current) {
      observer.observe(observerRef.current);
    }
    
    return () => observer.disconnect();
  }, [fetchMore]);
  
  return <div ref={observerRef}>Loading more...</div>;
}
```

## Testing & Validation

### User Testing Checklist

- [ ] Can users complete key tasks?
- [ ] Are error messages clear and helpful?
- [ ] Is navigation intuitive?
- [ ] Do forms validate properly?
- [ ] Are loading states clear?
- [ ] Does it work on mobile devices?
- [ ] Is it accessible with keyboard only?
- [ ] Do screen readers work correctly?

### Accessibility Testing

```bash
# Automated tools
# - axe DevTools
# - WAVE Browser Extension
# - Lighthouse (Chrome DevTools)
# - Pa11y (CLI tool)

# Manual testing
# - Keyboard navigation (Tab, Enter, Space, Arrow keys)
# - Screen reader testing (NVDA, JAWS, VoiceOver)
# - Color contrast checking
# - Zoom testing (200% browser zoom)
```

## Common Patterns

### Modal/Dialog

```typescript
function Modal({ isOpen, onClose, title, children }) {
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden';
      // Focus trap
      const firstFocusable = modalRef.current?.querySelector(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
      );
      firstFocusable?.focus();
    }
    
    return () => {
      document.body.style.overflow = '';
    };
  }, [isOpen]);
  
  if (!isOpen) return null;
  
  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-title"
      onClick={(e) => {
        if (e.target === e.currentTarget) onClose();
      }}
    >
      <div>
        <h2 id="modal-title">{title}</h2>
        <button onClick={onClose} aria-label="Close dialog">×</button>
        {children}
      </div>
    </div>
  );
}
```

### Toast Notifications

```typescript
function Toast({ message, type = 'info', duration = 3000 }) {
  const [isVisible, setIsVisible] = useState(true);
  
  useEffect(() => {
    const timer = setTimeout(() => setIsVisible(false), duration);
    return () => clearTimeout(timer);
  }, [duration]);
  
  return (
    <div
      role="alert"
      aria-live="polite"
      className={`toast ${type} ${isVisible ? 'visible' : ''}`}
    >
      {message}
    </div>
  );
}
```

## Checklist for UI/UX Implementation

Before deploying UI changes:

- [ ] Semantic HTML used correctly
- [ ] All interactive elements keyboard accessible
- [ ] ARIA labels for icon-only buttons
- [ ] Color contrast meets WCAG AA standards
- [ ] Form validation with clear error messages
- [ ] Loading states for async operations
- [ ] Error states with retry options
- [ ] Empty states with helpful guidance
- [ ] Success feedback for user actions
- [ ] Responsive design tested on mobile
- [ ] Focus management in modals/dialogs
- [ ] Screen reader tested (if possible)
- [ ] Keyboard navigation tested
- [ ] Images have descriptive alt text
- [ ] Confirmation dialogs for destructive actions
