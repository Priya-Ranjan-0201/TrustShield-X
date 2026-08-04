import { test, expect } from '@playwright/test';

test.describe('TruthShield X Authentication & Dashboard E2E Flow', () => {
  test('unauthenticated access to /dashboard redirects to /login', async ({ page }) => {
    await page.goto('/dashboard');
    await expect(page).toHaveURL(/.*login/);
  });

  test('login -> dashboard -> logout flow', async ({ page }) => {
    await page.goto('/login');
    await expect(page.getByText('Sign In to TruthShield X')).toBeVisible();

    // Fill login form
    await page.fill('input[type="email"]', 'citizen@truthshield.gov.in');
    await page.fill('input[type="password"]', 'Password123!');
    await page.click('button[type="submit"]');

    // Verify redirect to dashboard
    await expect(page).toHaveURL(/.*dashboard/);
    await expect(page.getByText('National Digital Trust Index')).toBeVisible();

    // Logout
    await page.click('button[aria-label="User menu"]');
    await page.click('text=Sign Out');
    await expect(page).toHaveURL(/.*login/);
  });
});
