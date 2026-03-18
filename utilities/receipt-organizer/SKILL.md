---
name: receipt-organizer
description: "Scan Gmail for receipts/invoices/payments from any month, create a labeled folder, and tag all receipt emails into it. Run monthly before sending to accountant."
---

# Receipt Organizer

Automatically find all receipt and payment emails in Gmail for a given month, create a labeled folder, and tag every matching email into it.

## Prerequisites

- Gmail MCP integration connected (either direct Gmail MCP or Rube MCP with Gmail toolkit)
- For Rube MCP: call `RUBE_SEARCH_TOOLS` first, then verify Gmail connection is ACTIVE via `RUBE_MANAGE_CONNECTIONS` with toolkit `gmail`

## How It Works

Think of it like a filing assistant: it goes through your entire inbox for a specific month, pulls out anything that looks like a receipt, invoice, payment confirmation, or financial transaction, and drops them all into one folder (Gmail label) so you can review and forward to your accountant.

## Workflow

### Step 1: Determine Target Month

- If user specifies a month/year, use that
- If user says "last month", calculate the previous month from today's date
- If no month specified, default to the previous month
- Format: `YYYY/MM/DD` for Gmail search queries

### Step 2: Search for Receipts

Run multiple Gmail searches to catch all receipt types. Use these search queries for the target month (replace dates accordingly):

**Query 1 — Direct receipt keywords:**
```
subject:(receipt OR invoice OR "order confirmation" OR "payment confirmation" OR "your order" OR "purchase" OR "billing statement") after:YYYY/MM/01 before:YYYY/MM+1/01
```

**Query 2 — Transaction emails from known senders:**
```
from:(uber.com OR lyft.com OR doordash.com OR grubhub.com OR instacart.com OR amazon.com OR paypal.com OR venmo.com OR stripe.com OR square.com OR shopify.com OR google.com OR apple.com OR spotify.com OR netflix.com OR anthropic.com OR openai.com OR noreply@notify.cloudflare.com OR speedpay.com OR intakeq.com) after:YYYY/MM/01 before:YYYY/MM+1/01 -category:promotions
```

**Query 3 — Bank/payment alerts:**
```
from:(pncalerts@pnc.com OR chase.com OR capitalone.com OR wellsfargo.com OR bankofamerica.com OR citi.com OR amex.com OR discover.com) subject:(payment OR charge OR deducted OR "sent you" OR receipt OR statement) after:YYYY/MM/01 before:YYYY/MM+1/01
```

### Step 3: Filter Results

From all search results, keep ONLY emails that are actual financial transactions. Remove:
- Promotional emails (sales, coupons, marketing)
- Newsletter content
- Shipping updates (unless they contain order totals)
- Account security alerts
- Password resets
- General notifications

**Keep these types:**
- Payment receipts (Uber, DoorDash, subscriptions, etc.)
- Order confirmations with dollar amounts
- Invoice emails
- Bank payment alerts (Zelle sent/received, bill payments, pre-auth charges)
- Subscription renewal charges
- Service payment confirmations (medical, utilities, rent, etc.)

### Step 4: Create the Label

Create a Gmail label with this naming format:
```
Receipts/[Month Name] [Year]
```

Examples:
- `Receipts/March 2026`
- `Receipts/February 2026`
- `Receipts/January 2026`

The `/` creates a nested label — so "Receipts" becomes a parent folder with monthly sub-folders.

**Before creating:** List existing labels first to check if it already exists. If it does, skip creation and use the existing label.

### Step 5: Tag All Receipt Emails

Batch-apply the label to all filtered receipt message IDs.

- Use batch modify for efficiency (up to 1000 messages per call)
- If more than 1000 receipts, chunk into multiple batch calls

### Step 6: Report Results

Show the user a summary:

```
## Receipts Organized: [Month] [Year]

**Label created:** Receipts/[Month] [Year]
**Total receipts found:** [count]

### Receipt Summary:
| # | Date | From | Subject | Amount (if visible) |
|---|------|------|---------|---------------------|
| 1 | ... | ... | ... | ... |
| 2 | ... | ... | ... | ... |

### How to forward to your accountant:
1. Open Gmail
2. Click the "Receipts/[Month] [Year]" label in the left sidebar
3. Select all emails (checkbox at top)
4. Forward or download as needed
```

## Rube MCP Tool Sequence

If using Rube MCP (Composio):

```
1. RUBE_SEARCH_TOOLS → find Gmail tools
2. RUBE_MANAGE_CONNECTIONS → verify Gmail is ACTIVE
3. GMAIL_FETCH_EMAILS → search with receipt queries (run 3x for each query)
4. GMAIL_LIST_LABELS → check if label exists
5. GMAIL_CREATE_LABEL → create "Receipts/[Month] [Year]"
6. GMAIL_BATCH_MODIFY_MESSAGES → tag all receipt IDs with the new label
```

## Direct Gmail MCP Tool Sequence

If using direct Gmail MCP:

```
1. search_emails → search with receipt queries (run 3x for each query)
2. list_labels → check if label exists
3. create_label → create "Receipts/[Month] [Year]"
4. batch_modify → tag all receipt IDs with the new label
```

## Claude AI Gmail MCP Tool Sequence

If using Claude AI's Gmail integration (claude.ai):

```
1. gmail_search_messages → search with receipt queries (run 3x for each query)
2. gmail_list_labels → check if label exists
3. gmail_create_draft → create a draft email listing all receipts (fallback if no label tools)
```

Note: Claude AI's Gmail MCP may not support label creation. In that case, generate a Gmail search query the user can paste to view all receipts, plus create a summary draft.

## Edge Cases

- **Duplicate results across queries:** Deduplicate by message ID before tagging
- **Empty month:** Report "No receipts found for [Month] [Year]"
- **Label already exists:** Use existing label, report how many NEW emails were tagged
- **Rate limits:** If batch modify fails with 429, wait and retry with smaller chunks

## When to Use

Run this skill when the user says any of:
- "organize my receipts"
- "find my receipts for [month]"
- "receipt folder"
- "get my receipts ready for my accountant"
- "monthly receipts"
- "/receipt-organizer"
