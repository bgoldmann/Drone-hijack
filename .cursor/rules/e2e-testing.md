# E2E Testing Development Guide

Comprehensive guide for end-to-end testing in Cursor IDE. Covers Playwright, Cypress, test patterns, best practices, and CI/CD integration.

## Overview

End-to-end (E2E) testing verifies that your application works from the user's perspective:
- **Full Application Flow**: Tests complete user journeys
- **Browser Automation**: Simulates real user interactions
- **CI/CD Integration**: Automated testing in pipelines
- **Visual Testing**: Screenshot and visual regression testing
- **Performance Testing**: Measure load times and performance

## Playwright

### Installation

```bash
npm install -D @playwright/test
npx playwright install
```

### Configuration

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
    {
      name: 'Mobile Chrome',
      use: { ...devices['Pixel 5'] },
    },
  ],
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
});
```

### Basic Test

```typescript
// e2e/home.spec.ts
import { test, expect } from '@playwright/test';

test('homepage loads correctly', async ({ page }) => {
  await page.goto('/');
  
  await expect(page).toHaveTitle(/My App/);
  await expect(page.locator('h1')).toBeVisible();
  await expect(page.locator('h1')).toContainText('Welcome');
});
```

### Navigation and Interaction

```typescript
test('user can navigate and interact', async ({ page }) => {
  await page.goto('/');
  
  // Click button
  await page.click('button:has-text("Sign In")');
  
  // Fill form
  await page.fill('input[name="email"]', 'user@example.com');
  await page.fill('input[name="password"]', 'password123');
  
  // Submit form
  await page.click('button[type="submit"]');
  
  // Wait for navigation
  await page.waitForURL('/dashboard');
  
  // Assert content
  await expect(page.locator('h1')).toContainText('Dashboard');
});
```

### Waiting Strategies

```typescript
test('waiting strategies', async ({ page }) => {
  await page.goto('/');
  
  // Wait for element to be visible
  await page.waitForSelector('.user-menu', { state: 'visible' });
  
  // Wait for element to be hidden
  await page.waitForSelector('.loading-spinner', { state: 'hidden' });
  
  // Wait for network response
  await page.waitForResponse(response => 
    response.url().includes('/api/users') && response.status() === 200
  );
  
  // Wait for navigation
  await page.waitForNavigation();
  
  // Wait for specific URL
  await page.waitForURL('/dashboard');
  
  // Wait for timeout
  await page.waitForTimeout(1000); // Use sparingly
});
```

### Selectors

```typescript
test('various selectors', async ({ page }) => {
  await page.goto('/');
  
  // CSS selector
  await page.click('.button-primary');
  
  // Text selector
  await page.click('text=Sign In');
  await page.click('button:has-text("Submit")');
  
  // Role selector (recommended)
  await page.click('role=button[name="Sign In"]');
  await page.click('role=textbox[name="Email"]');
  
  // Data attribute
  await page.click('[data-testid="submit-button"]');
  
  // Locator API (chainable)
  const submitButton = page.locator('button').filter({ hasText: 'Submit' });
  await submitButton.click();
  
  // XPath (use sparingly)
  await page.click('xpath=//button[contains(text(), "Submit")]');
});
```

### Assertions

```typescript
test('assertions', async ({ page }) => {
  await page.goto('/');
  
  // Visibility
  await expect(page.locator('.header')).toBeVisible();
  await expect(page.locator('.hidden')).toBeHidden();
  
  // Text content
  await expect(page.locator('h1')).toContainText('Welcome');
  await expect(page.locator('.error')).toHaveText('Error occurred');
  
  // Attributes
  await expect(page.locator('input')).toHaveAttribute('type', 'email');
  await expect(page.locator('a')).toHaveAttribute('href', '/dashboard');
  
  // CSS
  await expect(page.locator('.alert')).toHaveClass(/error/);
  await expect(page.locator('button')).toHaveCSS('background-color', 'rgb(0, 0, 255)');
  
  // Count
  await expect(page.locator('.item')).toHaveCount(5);
  
  // URL
  await expect(page).toHaveURL(/dashboard/);
  await expect(page).toHaveTitle(/Dashboard/);
});
```

### Handling Forms

```typescript
test('form submission', async ({ page }) => {
  await page.goto('/contact');
  
  // Fill form fields
  await page.fill('[name="name"]', 'John Doe');
  await page.fill('[name="email"]', 'john@example.com');
  await page.fill('[name="message"]', 'Test message');
  
  // Select dropdown
  await page.selectOption('[name="subject"]', 'Support');
  
  // Check checkbox
  await page.check('[name="newsletter"]');
  
  // Uncheck checkbox
  await page.uncheck('[name="terms"]');
  
  // Radio button
  await page.check('[name="priority"][value="high"]');
  
  // File upload
  await page.setInputFiles('[name="file"]', 'path/to/file.pdf');
  
  // Submit form
  await page.click('button[type="submit"]');
  
  // Wait for success message
  await expect(page.locator('.success-message')).toBeVisible();
});
```

### API Testing

```typescript
test('API request interception', async ({ page }) => {
  // Intercept and mock API response
  await page.route('**/api/users', route => {
    route.fulfill({
      status: 200,
      body: JSON.stringify([
        { id: 1, name: 'John', email: 'john@example.com' },
        { id: 2, name: 'Jane', email: 'jane@example.com' },
      ]),
    });
  });
  
  await page.goto('/users');
  
  // Wait for mocked data to appear
  await expect(page.locator('.user-card')).toHaveCount(2);
});

test('verify API call', async ({ page }) => {
  let requestBody;
  
  await page.route('**/api/users', route => {
    requestBody = route.request().postDataJSON();
    route.continue();
  });
  
  await page.goto('/users');
  await page.click('button:has-text("Create User")');
  await page.fill('[name="name"]', 'New User');
  await page.click('button[type="submit"]');
  
  expect(requestBody).toEqual({ name: 'New User' });
});
```

### Authentication

```typescript
// auth.setup.ts
import { test as setup, expect } from '@playwright/test';

const authFile = 'playwright/.auth/user.json';

setup('authenticate', async ({ page }) => {
  await page.goto('/login');
  await page.fill('[name="email"]', 'test@example.com');
  await page.fill('[name="password"]', 'password123');
  await page.click('button[type="submit"]');
  
  await page.waitForURL('/dashboard');
  
  // Save authentication state
  await page.context().storageState({ path: authFile });
});

// test.spec.ts
import { test } from '@playwright/test';

test.use({ storageState: 'playwright/.auth/user.json' });

test('authenticated test', async ({ page }) => {
  await page.goto('/dashboard');
  // Already authenticated
  await expect(page.locator('.user-menu')).toBeVisible();
});
```

### Visual Testing

```typescript
test('visual regression', async ({ page }) => {
  await page.goto('/');
  
  // Take screenshot
  await expect(page).toHaveScreenshot('homepage.png');
  
  // Element screenshot
  await expect(page.locator('.header')).toHaveScreenshot('header.png');
  
  // Full page screenshot
  await expect(page).toHaveScreenshot('full-page.png', {
    fullPage: true,
  });
});
```

### Page Object Model

```typescript
// pages/LoginPage.ts
import { Page, Locator } from '@playwright/test';

export class LoginPage {
  readonly page: Page;
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly submitButton: Locator;
  readonly errorMessage: Locator;

  constructor(page: Page) {
    this.page = page;
    this.emailInput = page.locator('[name="email"]');
    this.passwordInput = page.locator('[name="password"]');
    this.submitButton = page.locator('button[type="submit"]');
    this.errorMessage = page.locator('.error-message');
  }

  async goto() {
    await this.page.goto('/login');
  }

  async login(email: string, password: string) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.submitButton.click();
  }

  async isLoggedIn() {
    await this.page.waitForURL('/dashboard');
  }
}

// test.spec.ts
import { test, expect } from '@playwright/test';
import { LoginPage } from '../pages/LoginPage';

test('login flow', async ({ page }) => {
  const loginPage = new LoginPage(page);
  
  await loginPage.goto();
  await loginPage.login('test@example.com', 'password123');
  await loginPage.isLoggedIn();
  
  await expect(page.locator('.dashboard')).toBeVisible();
});
```

## Cypress

### Installation

```bash
npm install -D cypress
npx cypress open
```

### Configuration

```javascript
// cypress.config.js
const { defineConfig } = require('cypress');

module.exports = defineConfig({
  e2e: {
    baseUrl: 'http://localhost:3000',
    viewportWidth: 1280,
    viewportHeight: 720,
    video: true,
    screenshotOnRunFailure: true,
    setupNodeEvents(on, config) {
      // implement node event listeners here
    },
  },
});
```

### Basic Test

```javascript
// cypress/e2e/home.cy.js
describe('Homepage', () => {
  it('loads correctly', () => {
    cy.visit('/');
    cy.title().should('contain', 'My App');
    cy.get('h1').should('be.visible').and('contain', 'Welcome');
  });
});
```

### Commands and Actions

```javascript
describe('User interactions', () => {
  it('can navigate and interact', () => {
    cy.visit('/');
    
    // Click
    cy.get('button').contains('Sign In').click();
    
    // Type
    cy.get('[name="email"]').type('user@example.com');
    cy.get('[name="password"]').type('password123');
    
    // Select
    cy.get('[name="category"]').select('Electronics');
    
    // Check/Uncheck
    cy.get('[name="terms"]').check();
    cy.get('[name="newsletter"]').uncheck();
    
    // Upload file
    cy.get('[name="file"]').selectFile('cypress/fixtures/file.pdf');
    
    // Submit
    cy.get('form').submit();
    
    // Assert navigation
    cy.url().should('include', '/dashboard');
  });
});
```

### Custom Commands

```javascript
// cypress/support/commands.js
Cypress.Commands.add('login', (email, password) => {
  cy.visit('/login');
  cy.get('[name="email"]').type(email);
  cy.get('[name="password"]').type(password);
  cy.get('button[type="submit"]').click();
  cy.url().should('include', '/dashboard');
});

Cypress.Commands.add('getByTestId', (testId) => {
  return cy.get(`[data-testid="${testId}"]`);
});

// Usage
cy.login('test@example.com', 'password123');
cy.getByTestId('user-menu').click();
```

### API Testing with Cypress

```javascript
describe('API Testing', () => {
  it('can intercept API calls', () => {
    cy.intercept('GET', '**/api/users', {
      statusCode: 200,
      body: [
        { id: 1, name: 'John' },
        { id: 2, name: 'Jane' },
      ],
    }).as('getUsers');
    
    cy.visit('/users');
    cy.wait('@getUsers');
    
    cy.get('.user-card').should('have.length', 2);
  });
  
  it('can make API requests', () => {
    cy.request({
      method: 'POST',
      url: '/api/users',
      body: { name: 'New User', email: 'new@example.com' },
    }).then((response) => {
      expect(response.status).to.eq(201);
      expect(response.body).to.have.property('id');
    });
  });
});
```

## Best Practices

### 1. Test User Journeys, Not Implementation

```typescript
// ✅ Good: Test user flow
test('user can complete purchase', async ({ page }) => {
  await page.goto('/products');
  await page.click('[data-testid="product-card"]');
  await page.click('button:has-text("Add to Cart")');
  await page.goto('/cart');
  await page.click('button:has-text("Checkout")');
  // ... complete checkout flow
});

// ❌ Bad: Test implementation details
test('clicking button triggers onClick handler', async ({ page }) => {
  // Testing internal implementation
});
```

### 2. Use Data Test IDs

```tsx
// Component
<button data-testid="submit-button" onClick={handleSubmit}>
  Submit
</button>

// Test
await page.click('[data-testid="submit-button"]');
```

### 3. Keep Tests Independent

Each test should be able to run independently and not rely on other tests.

### 4. Use Page Object Model

Extract page interactions into reusable page objects for maintainability.

### 5. Wait Strategically

```typescript
// ✅ Good: Wait for specific conditions
await page.waitForSelector('.user-menu', { state: 'visible' });
await page.waitForResponse(response => response.url().includes('/api'));

// ❌ Bad: Arbitrary timeouts
await page.waitForTimeout(5000);
```

### 6. Clean Up Test Data

```typescript
test.beforeEach(async ({ page }) => {
  // Set up test data
});

test.afterEach(async ({ page }) => {
  // Clean up test data
  await page.request.delete('/api/test/users');
});
```

### 7. Use Fixtures

```typescript
// Playwright
import { test as base } from '@playwright/test';

type MyFixtures = {
  authenticatedPage: Page;
};

export const test = base.extend<MyFixtures>({
  authenticatedPage: async ({ page }, use) => {
    // Authenticate
    await page.goto('/login');
    await page.fill('[name="email"]', 'test@example.com');
    await page.fill('[name="password"]', 'password');
    await page.click('button[type="submit"]');
    await page.waitForURL('/dashboard');
    
    await use(page);
  },
});
```

### 8. Parallelize Tests

Configure parallel execution for faster test runs:

```typescript
// playwright.config.ts
export default defineConfig({
  fullyParallel: true,
  workers: process.env.CI ? 2 : 4,
});
```

### 9. Handle Flakiness

```typescript
// Use retries
test('flaky test', async ({ page }) => {
  // Test code
}).retries(2);

// Use auto-waiting
await expect(page.locator('.element')).toBeVisible({ timeout: 10000 });
```

### 10. Test on Multiple Browsers

```typescript
// playwright.config.ts
projects: [
  { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
  { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
  { name: 'webkit', use: { ...devices['Desktop Safari'] } },
]
```

## CI/CD Integration

### GitHub Actions (Playwright)

```yaml
# .github/workflows/e2e.yml
name: E2E Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: 18
      - name: Install dependencies
        run: npm ci
      - name: Install Playwright
        run: npx playwright install --with-deps
      - name: Run E2E tests
        run: npm run test:e2e
      - uses: actions/upload-artifact@v3
        if: always()
        with:
          name: playwright-report
          path: playwright-report/
```

### GitHub Actions (Cypress)

```yaml
name: E2E Tests

on: [push, pull_request]

jobs:
  cypress-run:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: 18
      - name: Install dependencies
        run: npm ci
      - name: Run Cypress tests
        run: npm run cypress:run
      - uses: cypress-io/github-action@v5
        with:
          upload: true
```

## Checklist for E2E Testing

Before committing E2E test code:

- [ ] Tests focus on user journeys, not implementation details
- [ ] Data test IDs used for selectors (not brittle CSS)
- [ ] Tests are independent (can run in any order)
- [ ] Page Object Model used for complex pages
- [ ] Proper waiting strategies (no arbitrary timeouts)
- [ ] Test data cleaned up after tests
- [ ] Authentication handled via fixtures/setup
- [ ] API calls mocked/intercepted where appropriate
- [ ] Visual regression tests added (if applicable)
- [ ] Tests run in CI/CD pipeline
- [ ] Tests run on multiple browsers (at least Chrome, Firefox)
- [ ] Screenshots captured on failures
- [ ] Flaky tests identified and fixed or retried
- [ ] Tests are fast (< 30 seconds per test when possible)