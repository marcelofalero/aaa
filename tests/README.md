# Interface Tests

This directory contains automated interface tests using Playwright.

## Prerequisites
- Node.js and npm
- Playwright (installed via `npm install` in this directory)
- Hugo server running at `http://localhost:1313`

## Running Tests
To run the tests:
1. Ensure the Hugo site is running: `hugo serve`
2. Run the tests:
```bash
npx playwright test
```

## Available Tests
- `psionics.spec.js`: Verifies psionics data (attributes, terminology) and visual indicators for Trained Only skills.
- `debug.spec.js`: Simple debug script for checking page state.
