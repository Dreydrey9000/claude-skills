#!/usr/bin/env python3
"""
Swipe Lab — Carousel Renderer
Takes an HTML file with .slide elements and screenshots each one at 1080x1350.

Usage:
    python3 scripts/render_carousel.py --input carousels/my_carousel/slides.html --output carousels/my_carousel/
    python3 scripts/render_carousel.py --input /tmp/new_carousel.html --output /tmp/output/
"""

import argparse
import asyncio
import os


async def render(html_path, output_dir):
    from playwright.async_api import async_playwright

    os.makedirs(output_dir, exist_ok=True)
    abs_path = os.path.abspath(html_path)

    print(f"Rendering: {html_path}")
    print(f"Output:    {output_dir}")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1080, "height": 1350})

        await page.goto(f"file://{abs_path}", wait_until="domcontentloaded")
        await page.wait_for_timeout(2000)

        slides = await page.query_selector_all(".slide")
        print(f"Found {len(slides)} slides")

        for i, slide in enumerate(slides, 1):
            await page.set_viewport_size({"width": 1080, "height": 1350})
            await slide.scroll_into_view_if_needed()
            await page.wait_for_timeout(300)
            path = f"{output_dir}/slide_{i}.png"
            await slide.screenshot(path=path)
            print(f"  Slide {i} → {path}")

        await browser.close()

    print(f"\nDone! {len(slides)} slides saved to {output_dir}/")


def main():
    parser = argparse.ArgumentParser(description="Render carousel HTML to 1080x1350 PNGs")
    parser.add_argument("--input", required=True, help="Path to slides.html")
    parser.add_argument("--output", required=True, help="Output directory for PNGs")
    args = parser.parse_args()

    asyncio.run(render(args.input, args.output))


if __name__ == "__main__":
    main()
