---
name: screenshots
description: "Generate marketing screenshots of your app using Playwright. Use when the user wants to create screenshots for Product Hunt, social media, landing pages, or documentation."
risk: safe
source: "https://github.com/Shpigford/skills/tree/main/screenshots"
date_added: "2026-02-27"
---

# Screenshots

Generate marketing-quality screenshots of your app using Playwright directly. Screenshots are captured at true HiDPI (2x retina) resolution using `deviceScaleFactor: 2`.

## When to Use This Skill

Use this skill when:
- User wants to create screenshots for Product Hunt
- Creating screenshots for social media
- Generating images for landing pages
- Creating documentation screenshots
- User requests marketing-quality app screenshots

## Prerequisites

Playwright must be available. Check for it:
```bash
npx playwright --version 2>/dev/null || npm ls playwright 2>/dev/null | grep playwright
```

If not found, inform the user:
> Playwright is required. Install it with: `npm install -D playwright` or `npm install -D @playwright/test`

## Step 3: Analyze Codebase for Features

Thoroughly explore the codebase to understand the app and identify screenshot opportunities.

### 3.1: Read Documentation First

**Always start by reading these files** to understand what the app does:

1. **README.md** (and any README files in subdirectories) - Read the full README to understand:
   - What the app is and what problem it solves
   - Key features and capabilities
   - Screenshots or feature descriptions already documented

2. **CHANGELOG.md** or **HISTORY.md** - Recent features worth highlighting

3. **docs/** directory - Any additional documentation about features

### 3.3: Identify Key Components

Look for components that represent screenshottable features:

- Dashboard components
- Feature sections with distinct UI
- Forms and interactive inputs
- Data visualizations (charts, graphs, tables)
- Modals and dialogs
- Navigation and sidebars
- Settings panels
- User profile sections

### 3.4: Check for Marketing Assets

Look for existing marketing content that hints at key features:
- Landing page components (often in `components/landing/` or `components/marketing/`)
- Feature list components
- Pricing tables
- Testimonial sections

### 3.5: Build Feature List

Create a comprehensive list of discovered features with:
- Feature name (from README or component name)
- URL path (from routes)
- CSS selector to focus on (from component structure)
- Required UI state (logged in, data populated, modal open, specific tab selected)

## Step 4: Plan Screenshots with User

Present the discovered features to the user and ask them to confirm or modify the list.

Use `AskUserQuestion`:
- Header: "Features"
- Question: "I found these features in your codebase. Which would you like to screenshot?"
- Options: List 3-4 key features discovered, plus "Let me pick specific ones"

If user wants specific ones, ask follow-up questions to clarify exactly what to capture.

## Step 5: Create Screenshots Directory

```bash
mkdir -p screenshots
```

### Running the Script

```bash
node screenshot-script.mjs
```

After running, clean up the temporary script:
```bash
rm screenshot-script.mjs
```

### Element-Focused Screenshots

To screenshot a specific element instead of the full viewport:

```javascript
const element = await page.locator('[CSS_SELECTOR]');
await element.screenshot({ path: `${SCREENSHOTS_DIR}/element.png` });
```

### Full Page Screenshots

For scrollable content, capture the entire page:

```javascript
await page.screenshot({
  path: `${SCREENSHOTS_DIR}/full-page.png`,
  fullPage: true
});
```

### Waiting for Animations

If the page has animations, wait for them to complete:

```javascript
await page.waitForTimeout(500); // Wait 500ms for animations
```

### Clicking Elements Before Screenshot

To capture a modal, dropdown, or hover state:

```javascript
await page.click('button.open-modal');
await page.waitForSelector('.modal-content');
await page.screenshot({ path: `${SCREENSHOTS_DIR}/modal.png` });
```

### Dark Mode Screenshots

If the app supports dark mode:

```javascript
// Set dark mode preference
const context = await browser.newContext({
  viewport: { width: 1440, height: 900 },
  deviceScaleFactor: 2,
  colorScheme: 'dark',
});
```

## Step 8: File Naming Convention

Use descriptive, kebab-case filenames with numeric prefixes for ordering:

| Feature | Filename |
|---------|----------|
| Dashboard overview | `01-dashboard-overview.png` |
| Link management | `02-link-inbox.png` |
| Edition editor | `03-edition-editor.png` |
| Analytics | `04-analytics.png` |
| Settings | `05-settings.png` |

## Error Handling

- **Playwright not found**: Suggest `npm install -D playwright`
- **Page not loading**: Check if the dev server is running, suggest starting it
- **Login failed**: The smart locators try common patterns but may fail on unusual login forms. If login fails, analyze the login page HTML to find the correct selectors and customize the script.
- **Element not found**: Verify the CSS selector, offer to take a full page screenshot instead
- **Screenshot failed**: Check disk space, verify write permissions to screenshots directory

## Tips for Best Results

1. **Clean UI state**: Use demo/seed data for realistic content
2. **Consistent sizing**: Use the same viewport for all screenshots
3. **Wait for content**: Use `waitForLoadState('networkidle')` to ensure all content loads
4. **Hide dev tools**: Ensure no browser extensions or dev overlays are visible
5. **Dark mode variants**: Consider capturing both light and dark mode if supported


## Full Specification

Complete details, decision trees, protocols, and implementation specs: [references/full-details.md](references/full-details.md)
