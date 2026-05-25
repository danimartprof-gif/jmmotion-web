"""Screenshot the local preview at desktop + mobile."""
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

URL = "http://127.0.0.1:8910/"
OUT = Path(__file__).parent / "preview"
OUT.mkdir(exist_ok=True)


async def shoot(p, vp, name, full=True):
    browser = await p.chromium.launch()
    ctx = await browser.new_context(viewport=vp, device_scale_factor=1)
    page = await ctx.new_page()
    await page.goto(URL, wait_until="networkidle", timeout=45000)
    # wait extra for fonts / lazy
    await page.wait_for_timeout(1500)
    out = OUT / f"{name}.png"
    await page.screenshot(path=str(out), full_page=full)
    print(f"  -> {out} ({out.stat().st_size//1024} KB)")
    await browser.close()


async def main():
    async with async_playwright() as p:
        print("Desktop full-page…");  await shoot(p, {"width":1440,"height":900}, "desktop-full")
        print("Desktop above-fold…"); await shoot(p, {"width":1440,"height":900}, "desktop-fold", full=False)
        print("Mobile full-page…");   await shoot(p, {"width":390,"height":844}, "mobile-full")
        print("Mobile above-fold…");  await shoot(p, {"width":390,"height":844}, "mobile-fold", full=False)


asyncio.run(main())
