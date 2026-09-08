import { test, expect } from '@playwright/test';

test('Customer can sign in, inspect a defect, save a decision and see persistent history', async ({page})=>{
  await page.goto('/');
  await page.getByRole('button',{name:'Sign in to workspace'}).click();
  await expect(page.getByRole('heading',{name:'Production overview'})).toBeVisible();
  await page.getByRole('button',{name:'Simulate inspection'}).click();
  await expect(page.getByRole('status')).toContainText('New simulated inspection');
  await page.getByRole('button',{name:/Review queue/}).click();
  await page.getByRole('button',{name:/Open AX-MB/}).first().click();
  await expect(page.getByRole('heading',{name:'Human review'})).toBeVisible();
  await page.getByRole('button',{name:'Zoom in',exact:true}).click();
  await page.getByRole('button',{name:'Reset view'}).click();
  await page.getByLabel('Decision reason').fill('Confirmed solder bridge on illustrated power controller evidence.');
  await page.getByRole('button',{name:'Save review decision'}).click();
  await page.getByRole('button',{name:'Confirm decision',exact:true}).click();
  await expect(page.getByRole('status')).toContainText('Review decision saved');
  await page.getByRole('button',{name:/Decision history/}).click();
  await expect(page.getByText('Human decision: FAIL',{exact:true})).toBeVisible();
  await page.reload();
  await page.getByRole('button',{name:/Decision history/}).click();
  await expect(page.getByText('Human decision: FAIL',{exact:true})).toBeVisible();
  await page.getByRole('button',{name:'Back to workspace'}).click();
  await page.getByLabel('Search inspections').fill('no-board-matches-this');
  await expect(page.getByRole('heading',{name:'No matching inspections'})).toBeVisible();
  await page.getByRole('button',{name:'Sign out',exact:true}).click();
  await expect(page.getByRole('button',{name:'Sign in to workspace'})).toBeVisible();
});

test('Mobile dashboard and detail stay within viewport with usable navigation',async({page})=>{
  await page.setViewportSize({width:390,height:844});
  await page.goto('/');
  await page.getByRole('button',{name:'Sign in to workspace'}).click();
  await expect(page.getByRole('heading',{name:'Production overview'})).toBeVisible();
  expect(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth)).toBe(true);
  await page.getByRole('button',{name:'Open navigation'}).click();
  await page.getByRole('button',{name:/Review queue/}).click();
  await page.getByRole('button',{name:/Open AX-MB/}).first().click();
  await expect(page.getByRole('heading',{name:'Human review'})).toBeVisible();
  expect(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth)).toBe(true);
});
