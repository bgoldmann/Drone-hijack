# Cursor Rules for Ralph

This directory contains Cursor Rules for use with Ralph in Cursor IDE. These rules guide Cursor's AI when working on different aspects of development.

## Available Rules

These rules can be referenced in your `.cursorrules` file or used directly when working with Cursor Chat/Composer:

### Core Workflow

- **prd-generation.md** - Guide for generating Product Requirements Documents
- **prd-from-external.md** - Guide for creating PRDs by analyzing websites or iOS apps
- **ralph-workflow.md** - Complete guide to using Ralph and understanding `ralph.sh` script
- **ralph-task-workflow.md** - Reference guide for Ralph task-based workflow patterns
- **compound-engineering.md** - Compound engineering workflow for systematic development

### Design & User Experience
- **frontend-design.md** - Frontend design guidelines for creating distinctive interfaces
- **ui-ux.md** - UI/UX design guidelines covering accessibility and user experience patterns

### Backend Development
- **backend-development.md** - Backend development best practices for APIs, databases, security, and testing
- **fastapi.md** - FastAPI development guide for routing, Pydantic models, dependencies, and API best practices
- **supabase.md** - Comprehensive Supabase guide for authentication, database, real-time, and storage
- **postgresql.md** - PostgreSQL guide for SQL queries, migrations, indexing, optimization, and transactions
- **graphql.md** - GraphQL guide for schemas, queries, mutations, subscriptions, resolvers, and best practices

### Frontend Development
- **react.md** - React development guide for components, hooks, state management, patterns, and performance
- **nextjs.md** - Next.js development guide for App Router, Server Components, Server Actions, and routing
- **typescript.md** - TypeScript guide for type safety, advanced types, generics, and type patterns
- **tailwind-css.md** - Tailwind CSS guide for utility-first styling, responsive design, and modern UI development
- **seo.md** - SEO guide for meta tags, structured data, sitemaps, and search engine optimization

### Services & Integrations
- **stripe.md** - Stripe payment integration guide for one-time payments, subscriptions, webhooks, and billing
- **coinbase-commerce.md** - Coinbase Commerce integration guide for cryptocurrency payments and webhooks
- **vercel.md** - Vercel deployment guide for Next.js, serverless functions, edge functions, and optimization
- **firebase.md** - Firebase integration guide for authentication, Firestore, storage, Cloud Functions, and real-time features
- **google-services.md** - Google services integration guide for GCP, OAuth, Maps, Analytics, Drive, Sheets, and more
- **llms.md** - Large Language Models integration guide for OpenAI, Anthropic, and other providers
- **llm-seo.md** - LLM-assisted SEO guide for content optimization, SEO analysis, and AI-powered SEO workflows
- **mcp.md** - Model Context Protocol integration guide for connecting LLMs to external tools, data sources, and prompts

### Testing & Quality
- **testing.md** - Testing guide for unit tests, integration tests, E2E tests, and test patterns
- **e2e-testing.md** - End-to-end testing guide for Playwright, Cypress, test patterns, and CI/CD integration
- **agent-browser.md** - Browser automation for testing UI components

### DevOps & Tools
- **docker.md** - Docker guide for containerization, Dockerfiles, docker-compose, and multi-stage builds
- **cicd.md** - CI/CD guide for GitHub Actions, automated testing, and deployment workflows
- **git-github.md** - Git and GitHub workflow guide for branching, commits, PRs, and collaboration

### Security & Performance
- **security.md** - Security best practices covering authentication, input validation, and common vulnerabilities
- **performance.md** - Performance optimization guide for frontend, backend, and database optimization

### Document Processing
- **pdf-processing.md** - Comprehensive PDF manipulation guide
- **docx-processing.md** - Document creation, editing, and analysis guide

### Mobile Development
- **ios-app.md** - iOS app development guide for Swift/SwiftUI, Xcode setup, architecture patterns, and App Store deployment

## Using These Rules

### Option 1: Reference in .cursorrules

Add to your `.cursorrules` file:
```
When generating PRDs, follow the guidelines in .cursor/rules/prd-generation.md
```

### Option 2: Use Directly in Cursor Chat

When working with Cursor Chat or Composer, you can reference these rules:
```
Follow the PRD generation guidelines from .cursor/rules/prd-generation.md
```

### Option 3: Include in Composer Prompt

When `ralph.sh` generates a Composer prompt, it can reference specific rules based on the story type.

## Converting Amp Skills to Cursor Rules

If you have additional Amp skills in `amp-skills-main/`, you can convert them:

1. Copy the skill's `SKILL.md` file content
2. Remove Amp-specific frontmatter (name, description with triggers)
3. Remove Amp CLI-specific commands
4. Adapt to Cursor IDE context
5. Save as `.cursor/rules/[skill-name].md`

## Notes

- These rules are converted from Amp skills but adapted for Cursor IDE
- Original skills are preserved in `amp-skills-main/` for reference
- Rules can be customized for your project's specific needs
