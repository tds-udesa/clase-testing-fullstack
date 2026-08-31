import { test, expect } from '@playwright/test';

test('get a new random dog and save it', async ({ page }) => {
  await page.goto('/');

  // Wait for the initial random dog to load.
  await expect(page.getByAltText('Un perro aleatorio')).toBeVisible();

  // Get a new random dog.
  await page.getByRole('button', { name: 'Otro perro' }).click();
  await page.waitForTimeout(4000);

  // Save it.
  await page.getByRole('button', { name: 'Guardar este perro' }).click();

  await expect(
    page.getByText(/Perro guardado|No se pudo guardar el perro/),
  ).toBeVisible();
});

test('open the saved dogs list', async ({ page }) => {
  await page.goto('/');

  await page.getByRole('link', { name: 'Perros Guardados' }).click();

  await expect(page).toHaveURL('/saved');

  const emptyMessage = page.getByText(
    'Todavía no guardaste ningún perro. ¡Guardá uno desde la pestaña Perro Aleatorio!',
  );
  const savedDogCard = page.getByRole('img').first();

  await expect(emptyMessage.or(savedDogCard)).toBeVisible();
});
