# Tailwind CSS Development Guide

Comprehensive guide for using Tailwind CSS in Cursor IDE for utility-first styling, responsive design, custom configurations, and modern UI development.

## Overview

Tailwind CSS is a utility-first CSS framework that provides:
- **Utility Classes**: Low-level utility classes for rapid UI development
- **Responsive Design**: Mobile-first responsive utilities
- **Customizable**: Highly configurable via `tailwind.config.js`
- **JIT Mode**: Just-In-Time compiler for minimal CSS output
- **Dark Mode**: Built-in dark mode support
- **Component Extraction**: Extract repeated patterns into components

## Installation

### Next.js

```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

### Vite

```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

### React (CRA/Vite)

```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

## Configuration

### tailwind.config.js

```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./app/**/*.{js,jsx,ts,tsx}",
    "./components/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          500: '#0ea5e9',
          900: '#0c4a6e',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      spacing: {
        '128': '32rem',
        '144': '36rem',
      },
      borderRadius: {
        '4xl': '2rem',
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
    require('@tailwindcss/aspect-ratio'),
  ],
  darkMode: 'class', // or 'media'
}
```

### CSS Entry Point

```css
/* src/index.css or app/globals.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

/* Custom base styles */
@layer base {
  html {
    @apply antialiased;
  }
  
  body {
    @apply bg-gray-50 text-gray-900;
  }
  
  h1 {
    @apply text-3xl font-bold;
  }
  
  h2 {
    @apply text-2xl font-semibold;
  }
}
```

## Core Concepts

### Utility Classes

```tsx
// Spacing
<div className="p-4 m-2">Padding and margin</div>
<div className="px-6 py-3">Horizontal and vertical padding</div>
<div className="space-y-4">Vertical spacing between children</div>
<div className="gap-4">Gap in flex/grid</div>

// Typography
<h1 className="text-4xl font-bold text-gray-900">Heading</h1>
<p className="text-lg text-gray-600 leading-relaxed">Paragraph</p>
<span className="font-medium text-blue-600">Emphasized text</span>

// Colors
<div className="bg-blue-500 text-white">Blue background</div>
<button className="bg-green-500 hover:bg-green-600">Green button</button>
<div className="border-2 border-red-500">Red border</div>

// Layout
<div className="flex items-center justify-between">Flexbox</div>
<div className="grid grid-cols-3 gap-4">Grid</div>
<div className="container mx-auto px-4">Centered container</div>
```

### Responsive Design

```tsx
// Mobile-first approach
<div className="
  text-sm          /* Base (mobile) */
  md:text-base     /* Medium screens (768px+) */
  lg:text-lg       /* Large screens (1024px+) */
  xl:text-xl       /* Extra large (1280px+) */
  2xl:text-2xl     /* 2X large (1536px+) */
">

// Responsive layout
<div className="
  grid
  grid-cols-1      /* Mobile: 1 column */
  md:grid-cols-2   /* Tablet: 2 columns */
  lg:grid-cols-3   /* Desktop: 3 columns */
  gap-4
">

// Show/hide based on screen size
<div className="hidden md:block">Visible on medium+ screens</div>
<div className="block md:hidden">Visible only on mobile</div>
```

### Hover, Focus, and Active States

```tsx
<button className="
  bg-blue-500
  hover:bg-blue-600
  active:bg-blue-700
  focus:outline-none
  focus:ring-2
  focus:ring-blue-500
  focus:ring-offset-2
  transition-colors
  duration-200
">
  Button
</button>

// Group hover (parent hover affects children)
<div className="group">
  <div className="bg-gray-200 group-hover:bg-blue-500">Hover parent</div>
  <p className="text-gray-600 group-hover:text-white">Affected child</p>
</div>
```

### Dark Mode

```tsx
// Enable dark mode in config: darkMode: 'class'

// Toggle dark mode (example with React)
function ThemeToggle() {
  const [dark, setDark] = useState(false);
  
  useEffect(() => {
    if (dark) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [dark]);
  
  return (
    <button onClick={() => setDark(!dark)}>
      {dark ? 'Light' : 'Dark'}
    </button>
  );
}

// Use dark mode classes
<div className="
  bg-white
  dark:bg-gray-900
  text-gray-900
  dark:text-white
">
  Content
</div>
```

## Common Patterns

### Cards

```tsx
function Card({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="
      bg-white
      rounded-lg
      shadow-md
      p-6
      border
      border-gray-200
      hover:shadow-lg
      transition-shadow
      duration-200
    ">
      <h3 className="text-xl font-semibold mb-4">{title}</h3>
      {children}
    </div>
  );
}
```

### Buttons

```tsx
// Primary button
<button className="
  bg-blue-600
  text-white
  px-6
  py-2
  rounded-md
  font-medium
  hover:bg-blue-700
  active:bg-blue-800
  focus:outline-none
  focus:ring-2
  focus:ring-blue-500
  focus:ring-offset-2
  disabled:opacity-50
  disabled:cursor-not-allowed
  transition-colors
">
  Primary
</button>

// Secondary button
<button className="
  bg-gray-200
  text-gray-800
  px-6
  py-2
  rounded-md
  font-medium
  hover:bg-gray-300
  active:bg-gray-400
  focus:outline-none
  focus:ring-2
  focus:ring-gray-500
  focus:ring-offset-2
">
  Secondary
</button>

// Outline button
<button className="
  border-2
  border-blue-600
  text-blue-600
  px-6
  py-2
  rounded-md
  font-medium
  hover:bg-blue-50
  active:bg-blue-100
  focus:outline-none
  focus:ring-2
  focus:ring-blue-500
  focus:ring-offset-2
">
  Outline
</button>
```

### Forms

```tsx
function Form() {
  return (
    <form className="space-y-4">
      <div>
        <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
          Email
        </label>
        <input
          id="email"
          type="email"
          className="
            w-full
            px-3
            py-2
            border
            border-gray-300
            rounded-md
            shadow-sm
            focus:outline-none
            focus:ring-2
            focus:ring-blue-500
            focus:border-blue-500
          "
        />
      </div>

      <div>
        <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">
          Password
        </label>
        <input
          id="password"
          type="password"
          className="
            w-full
            px-3
            py-2
            border
            border-gray-300
            rounded-md
            shadow-sm
            focus:outline-none
            focus:ring-2
            focus:ring-blue-500
            focus:border-blue-500
          "
        />
      </div>

      <button
        type="submit"
        className="
          w-full
          bg-blue-600
          text-white
          py-2
          px-4
          rounded-md
          font-medium
          hover:bg-blue-700
          focus:outline-none
          focus:ring-2
          focus:ring-blue-500
          focus:ring-offset-2
        "
      >
        Submit
      </button>
    </form>
  );
}
```

### Navigation

```tsx
function Navbar() {
  return (
    <nav className="bg-white shadow-md">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center space-x-8">
            <a href="/" className="text-xl font-bold text-gray-900">
              Logo
            </a>
            <div className="hidden md:flex space-x-4">
              <a href="/" className="text-gray-600 hover:text-gray-900 px-3 py-2">
                Home
              </a>
              <a href="/about" className="text-gray-600 hover:text-gray-900 px-3 py-2">
                About
              </a>
              <a href="/contact" className="text-gray-600 hover:text-gray-900 px-3 py-2">
                Contact
              </a>
            </div>
          </div>
          <button className="md:hidden">
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
        </div>
      </div>
    </nav>
  );
}
```

### Grid Layouts

```tsx
// Responsive grid
<div className="
  grid
  grid-cols-1
  sm:grid-cols-2
  lg:grid-cols-3
  xl:grid-cols-4
  gap-6
">
  {items.map(item => (
    <Card key={item.id} item={item} />
  ))}
</div>

// Masonry layout (with columns)
<div className="columns-1 md:columns-2 lg:columns-3 gap-4">
  {posts.map(post => (
    <article key={post.id} className="break-inside-avoid mb-4">
      <PostCard post={post} />
    </article>
  ))}
</div>
```

### Flexbox Layouts

```tsx
// Centered content
<div className="flex items-center justify-center min-h-screen">
  <div>Centered content</div>
</div>

// Space between
<div className="flex items-center justify-between">
  <div>Left</div>
  <div>Right</div>
</div>

// Sticky header
<header className="sticky top-0 z-50 bg-white shadow-sm">
  <div className="flex items-center justify-between h-16 px-4">
    <div>Logo</div>
    <nav>Navigation</nav>
  </div>
</header>
```

## Advanced Features

### Custom Utilities with @layer

```css
@layer utilities {
  .text-balance {
    text-wrap: balance;
  }
  
  .scrollbar-hide {
    -ms-overflow-style: none;
    scrollbar-width: none;
  }
  
  .scrollbar-hide::-webkit-scrollbar {
    display: none;
  }
}
```

### Component Extraction

```css
@layer components {
  .btn-primary {
    @apply bg-blue-600 text-white px-6 py-2 rounded-md font-medium;
    @apply hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500;
  }
  
  .card {
    @apply bg-white rounded-lg shadow-md p-6 border border-gray-200;
  }
  
  .input-field {
    @apply w-full px-3 py-2 border border-gray-300 rounded-md;
    @apply focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500;
  }
}
```

### Arbitrary Values

```tsx
// Arbitrary values using square brackets
<div className="w-[500px] h-[300px]">
  Custom width and height
</div>

<div className="bg-[#1da1f2] text-[#ffffff]">
  Custom colors
</div>

<div className="top-[117px] left-[50%]">
  Custom positioning
</div>

<div className="grid-cols-[1fr_500px_2fr]">
  Custom grid template
</div>
```

### JIT Mode Features

```tsx
// Dynamic class generation (requires JIT)
<div className={`
  bg-${color}-500
  text-${color}-100
  border-${color}-300
`}>
  Dynamic colors (use with caution - prefer conditional classes)
</div>

// Better approach for dynamic values
const colorClasses = {
  blue: 'bg-blue-500 text-blue-100 border-blue-300',
  green: 'bg-green-500 text-green-100 border-green-300',
  red: 'bg-red-500 text-red-100 border-red-300',
};

<div className={colorClasses[color]}>
  Dynamic with predefined classes
</div>
```

## Plugins

### Forms Plugin

```bash
npm install @tailwindcss/forms
```

```javascript
// tailwind.config.js
plugins: [
  require('@tailwindcss/forms'),
],
```

```tsx
// Styled form inputs automatically
<input type="text" className="rounded-md border-gray-300" />
<input type="checkbox" className="rounded" />
```

### Typography Plugin

```bash
npm install @tailwindcss/typography
```

```tsx
// Prose classes for markdown/rich text
<article className="prose prose-lg max-w-none">
  <h1>Heading</h1>
  <p>Paragraph text with nice typography.</p>
  <ul>
    <li>List item</li>
  </ul>
</article>

// Customize prose
<article className="prose prose-blue prose-xl max-w-4xl">
  Customized prose
</article>
```

### Aspect Ratio Plugin

```bash
npm install @tailwindcss/aspect-ratio
```

```tsx
<div className="aspect-w-16 aspect-h-9">
  <iframe src="..." className="w-full h-full" />
</div>

<div className="aspect-square">
  <img src="..." alt="Square image" />
</div>
```

## Best Practices

### 1. Organize Classes

```tsx
// ✅ Good: Organized and readable
<button className={`
  bg-blue-600 text-white
  px-6 py-2 rounded-md
  font-medium
  hover:bg-blue-700
  focus:outline-none focus:ring-2 focus:ring-blue-500
  transition-colors duration-200
  disabled:opacity-50 disabled:cursor-not-allowed
`}>

// ❌ Avoid: All on one line (hard to read)
<button className="bg-blue-600 text-white px-6 py-2 rounded-md font-medium hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500">
```

### 2. Extract Reusable Components

```tsx
// Extract repeated patterns
function Button({ variant = 'primary', children, ...props }) {
  const baseClasses = 'px-6 py-2 rounded-md font-medium focus:outline-none focus:ring-2 focus:ring-offset-2 transition-colors';
  
  const variants = {
    primary: 'bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500',
    secondary: 'bg-gray-200 text-gray-800 hover:bg-gray-300 focus:ring-gray-500',
    outline: 'border-2 border-blue-600 text-blue-600 hover:bg-blue-50 focus:ring-blue-500',
  };
  
  return (
    <button className={`${baseClasses} ${variants[variant]}`} {...props}>
      {children}
    </button>
  );
}
```

### 3. Use clsx or classnames for Conditional Classes

```bash
npm install clsx
```

```tsx
import clsx from 'clsx';

function Button({ active, disabled, variant }) {
  return (
    <button
      className={clsx(
        'px-6 py-2 rounded-md font-medium',
        {
          'bg-blue-600 text-white': variant === 'primary',
          'bg-gray-200 text-gray-800': variant === 'secondary',
          'opacity-50 cursor-not-allowed': disabled,
          'ring-2 ring-blue-500': active,
        }
      )}
    >
      Button
    </button>
  );
}
```

### 4. Mobile-First Approach

```tsx
// ✅ Good: Mobile-first
<div className="
  text-sm        /* Mobile base */
  md:text-base   /* Tablet */
  lg:text-lg     /* Desktop */
">

// ❌ Avoid: Desktop-first
<div className="
  text-lg
  md:text-base
  sm:text-sm
">
```

### 5. Use Container for Responsive Widths

```tsx
<div className="container mx-auto px-4">
  {/* Content with max-width and padding */}
</div>

// Custom container in config
theme: {
  container: {
    center: true,
    padding: '2rem',
    screens: {
      sm: '640px',
      md: '768px',
      lg: '1024px',
      xl: '1280px',
    },
  },
}
```

### 6. Optimize for Production

```javascript
// tailwind.config.js - Ensure content paths are correct
content: [
  './src/**/*.{js,jsx,ts,tsx}',
  './app/**/*.{js,jsx,ts,tsx}',
  './components/**/*.{js,jsx,ts,tsx}',
],
```

```bash
# Build command will purge unused styles
npm run build
```

## Performance Tips

### 1. Avoid Dynamic Class Names

```tsx
// ❌ Bad: Can't be purged
<div className={`bg-${color}-500`}>

// ✅ Good: Full class names
<div className={color === 'blue' ? 'bg-blue-500' : 'bg-red-500'}>

// ✅ Better: Use component variants
const colorMap = {
  blue: 'bg-blue-500',
  red: 'bg-red-500',
};
<div className={colorMap[color]} />
```

### 2. Use JIT Mode (Default in Tailwind v3+)

JIT mode only generates CSS for classes you use, keeping bundle size minimal.

### 3. Purge Unused Styles

Ensure `content` paths in config match your file structure.

## Common Utilities Reference

### Spacing
- `p-{n}`, `px-{n}`, `py-{n}`, `pt-{n}`, `pr-{n}`, `pb-{n}`, `pl-{n}` - Padding
- `m-{n}`, `mx-{n}`, `my-{n}`, `mt-{n}`, `mr-{n}`, `mb-{n}`, `ml-{n}` - Margin
- `space-x-{n}`, `space-y-{n}` - Space between children

### Sizing
- `w-{n}`, `h-{n}`, `min-w-{n}`, `max-w-{n}`, `min-h-{n}`, `max-h-{n}` - Width/Height
- `w-full`, `h-full`, `w-screen`, `h-screen` - Full width/height

### Typography
- `text-{size}`, `font-{weight}`, `text-{color}`, `text-{align}`
- `leading-{n}`, `tracking-{n}`, `uppercase`, `lowercase`, `capitalize`

### Display
- `block`, `inline-block`, `inline`, `flex`, `grid`, `hidden`
- `absolute`, `relative`, `fixed`, `sticky`

### Positioning
- `top-{n}`, `right-{n}`, `bottom-{n}`, `left-{n}`
- `z-{n}` - Z-index

### Flexbox
- `flex`, `flex-col`, `flex-row`
- `items-{align}`, `justify-{align}`, `gap-{n}`

### Grid
- `grid`, `grid-cols-{n}`, `grid-rows-{n}`, `gap-{n}`

### Borders
- `border`, `border-{width}`, `border-{color}`, `rounded-{size}`

### Shadows
- `shadow`, `shadow-sm`, `shadow-md`, `shadow-lg`, `shadow-xl`, `shadow-2xl`
- `shadow-none`

### Transitions
- `transition`, `transition-{property}`, `duration-{n}`, `ease-{type}`

## Checklist for Tailwind CSS Development

Before committing Tailwind-related code:

- [ ] Mobile-first responsive design implemented
- [ ] Dark mode classes included (if applicable)
- [ ] Focus states added for accessibility
- [ ] Hover states provide visual feedback
- [ ] Custom utilities extracted with @layer when reused
- [ ] Component classes extracted when pattern is repeated 3+ times
- [ ] No dynamic class name generation (use conditional full class names)
- [ ] Content paths in tailwind.config.js match project structure
- [ ] Production build tested (unused styles purged)
- [ ] Custom theme values defined in config (colors, spacing, etc.)
- [ ] Plugins installed and configured if needed
- [ ] Arbitrary values only when necessary (prefer config)