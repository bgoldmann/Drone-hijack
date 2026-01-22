# PRD Generation from External Sources Guide

Guide for generating Product Requirements Documents (PRDs) by analyzing existing websites or iOS apps. Use this when you need to reverse-engineer or replicate features from external applications.

## Overview

This guide helps you:
- Analyze websites or iOS app store pages
- Extract features, workflows, and requirements
- Convert findings into structured PRDs
- Document UI/UX patterns observed
- Create implementable user stories

## Workflow

### Step 1: Gather Information

#### For Websites:
1. **Use browser automation** (agent-browser) to explore the site:
   ```bash
   agent-browser open <url>
   agent-browser snapshot -i  # Get interactive elements
   agent-browser screenshot full-page.png  # Capture visuals
   ```

2. **Analyze key pages:**
   - Homepage
   - User flows (signup, login, main features)
   - Navigation structure
   - Forms and interactions

3. **Note observations:**
   - UI components and patterns
   - User workflows
   - Data structures (from forms, API calls if visible)
   - Responsive design behavior

#### For iOS Apps:
1. **Review App Store listing:**
   - App description and features
   - Screenshots and videos
   - User reviews (identify pain points and desired features)
   - App Store URL: `https://apps.apple.com/app/id[APP_ID]`

2. **If you have access to the app:**
   - Document screens and navigation flow
   - Note UI components and interactions
   - Observe data patterns and workflows

3. **Additional resources:**
   - App website (if available)
   - Marketing materials
   - Support documentation

### Step 2: Extract Features

Organize findings into categories:

#### Core Features
- Primary functionality the app/website provides
- User-facing capabilities
- Business logic workflows

#### User Flows
- Registration/signup process
- Onboarding experience
- Main feature interactions
- Settings and preferences

#### UI/UX Patterns
- Navigation structure (tabs, menus, drawers)
- Form designs and validation
- Feedback mechanisms (notifications, errors)
- Visual design elements

#### Technical Observations
- API endpoints (if visible in network tab)
- Data models (from forms and displays)
- Authentication methods
- Performance characteristics

### Step 3: Generate PRD Structure

Use the standard PRD structure from `prd-generation.md`, adapted for reverse engineering:

#### 1. Introduction/Overview
```markdown
# PRD: [Feature Name] (Based on [Source App/Website])

This PRD documents requirements for [feature] based on analysis of [source URL/App Name].

**Source:** [URL or App Store link]
**Analysis Date:** [Date]
```

#### 2. Observed Features
List what you found in the source application:
- Feature 1: Description of what it does
- Feature 2: Description of what it does
- Feature 3: Description of what it does

#### 3. Goals
What we want to achieve by implementing these features:
- Replicate [specific functionality]
- Improve upon [aspect] from the source
- Adapt for [our use case]

#### 4. User Stories

Convert observed features into user stories:

```markdown
### US-001: [Title based on observed feature]
**Description:** As a [user type], I want [observed functionality] so that [inferred benefit].

**Observed Behavior:**
- [What you saw in the source app]
- [How it worked]
- [User interaction flow]

**Acceptance Criteria:**
- [ ] Feature works like observed version
- [ ] [Specific verifiable behavior]
- [ ] npm run typecheck passes
- [ ] Verify in browser/device
```

**Important:** Base stories on what you observed, but adapt acceptance criteria for your implementation context.

#### 5. Functional Requirements

Document specific behaviors observed:

- **FR-1:** [Exact behavior from source]
- **FR-2:** [Another observed behavior]
- **FR-3:** [Data validation patterns observed]

#### 6. UI/UX Requirements

Capture design patterns:

- **Navigation:** [Type of navigation observed]
- **Layout:** [Layout patterns]
- **Components:** [Specific UI components to replicate]
- **Interactions:** [Animation, transitions, feedback]

#### 7. Technical Considerations

Infer technical requirements:

- **Data Models:** [Structures inferred from forms/display]
- **API Requirements:** [Endpoints or operations needed]
- **Authentication:** [Auth methods observed]
- **Performance:** [Response times, loading states observed]

#### 8. Adaptations & Improvements

Document how you'll adapt the observed features:

- What to keep from source
- What to improve
- What to change for our use case
- What to omit

#### 9. Open Questions

Questions that couldn't be answered from external analysis:

- [Question about internal logic]
- [Question about edge cases]
- [Question about data handling]

### Step 4: Analysis Techniques

#### Browser Analysis (Websites)

Use agent-browser to systematically explore:

```bash
# Initial navigation
agent-browser open https://example.com
agent-browser snapshot -i

# Navigate through flows
agent-browser click @e1  # Navigation link
agent-browser snapshot -i
agent-browser screenshot step1.png

# Test interactions
agent-browser fill @e2 "test@example.com"
agent-browser click @e3
agent-browser wait --load networkidle
agent-browser snapshot -i
```

#### Document Findings

As you explore, document:
- **Screenshots:** Save visual references
- **Element snapshots:** Record interactive elements
- **Navigation paths:** Document user flows
- **Form structures:** Note input fields and validation

#### iOS App Analysis

For iOS apps, focus on:

1. **App Store Analysis:**
   - Read feature descriptions
   - Analyze screenshots for UI patterns
   - Review user feedback for common requests/issues

2. **Feature Extraction:**
   - Main navigation (tab bar, navigation controller)
   - Primary features from description
   - User workflows implied by screenshots

3. **Design Patterns:**
   - iOS design patterns observed (standard components)
   - Custom UI elements
   - Interaction patterns

### Step 5: Create User Stories

Convert observations to implementable stories:

**Example - From Website Analysis:**
```markdown
### US-001: User Registration Form
**Description:** As a new user, I want to create an account so that I can access the platform.

**Observed Behavior:**
- Registration form with email, password, and name fields
- Email validation shown in real-time
- Password strength indicator
- Submit button disabled until all fields valid
- Success redirect to dashboard after submission

**Acceptance Criteria:**
- [ ] Registration form with email, password, and name inputs
- [ ] Real-time email format validation
- [ ] Password strength indicator (weak/medium/strong)
- [ ] Submit button disabled when validation fails
- [ ] Success redirect to dashboard page
- [ ] npm run typecheck passes
- [ ] Verify in browser using agent-browser
```

### Step 6: Validate & Refine

Before finalizing the PRD:

1. **Cross-reference:** Ensure all major features are captured
2. **Prioritize:** Identify MVP features vs nice-to-haves
3. **Clarify:** Add notes where observation was unclear
4. **Adapt:** Adjust requirements for your specific context

## Best Practices

### 1. Be Systematic

Follow a consistent exploration pattern:
- Start with homepage/landing
- Follow main user flows
- Test key interactions
- Document thoroughly

### 2. Capture Visuals

Screenshots and recordings are invaluable:
- Take screenshots of key screens
- Record interaction flows if possible
- Annotate screenshots with notes

### 3. Infer, Don't Assume

Clearly distinguish:
- **Observed:** What you directly saw
- **Inferred:** What you concluded from observations
- **Unknown:** What couldn't be determined

### 4. Focus on Behavior

Document what the app DOES, not just what it looks like:
- User actions
- System responses
- Data flows
- Error handling

### 5. Adapt to Your Context

Don't blindly copy - adapt:
- Consider your tech stack
- Adjust for your user base
- Improve upon weaknesses observed
- Add features that make sense for your use case

## Tools & Resources

### Browser Analysis
- **agent-browser:** Automated browser interaction (see `agent-browser.md`)
- **Browser DevTools:** Network tab, element inspector
- **Screenshots:** Visual documentation

### iOS App Analysis
- **App Store:** Official app descriptions and screenshots
- **App Annie/App Store Connect:** Analytics if available
- **User Reviews:** Feature requests and pain points

### Documentation
- **Markdown:** Standard PRD format
- **Screenshots:** Visual references
- **Diagrams:** User flow charts if needed

## Example Workflow

```markdown
# Analyzing https://example-app.com

1. Open homepage → Document layout, navigation
2. Click "Sign Up" → Document registration flow
3. Complete form → Note validation rules
4. Navigate to main feature → Document core functionality
5. Test interactions → Document user flows
6. Screenshot key screens → Visual references

Result: PRD with 12 user stories covering registration, 
authentication, and core features.
```

## Integration with PRD Generation

After analysis, use the standard PRD generation process:

1. Review your extracted features
2. Organize into logical user stories
3. Use `prd-generation.md` checklist
4. Convert to `prd.json` format (via `ralph-task-workflow.md`)
5. Begin implementation with Ralph

## Checklist

Before finalizing PRD from external source:

- [ ] Analyzed all key pages/features
- [ ] Documented user flows observed
- [ ] Captured screenshots/visual references
- [ ] Converted features to user stories
- [ ] Distinguished observed vs inferred behaviors
- [ ] Adapted requirements for our context
- [ ] Included technical considerations
- [ ] Noted open questions
- [ ] Saved to `tasks/prd-[feature-name].md`

## Notes

- This process works best for feature replication or inspiration
- Some internal logic may not be observable - document as unknowns
- User reviews can provide valuable insights into desired features
- Combine multiple sources when possible for comprehensive analysis
- Always adapt findings to your specific requirements and constraints
