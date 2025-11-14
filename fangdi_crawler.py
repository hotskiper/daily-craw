import asyncio
from playwright.async_api import async_playwright
import random
import csv
import os
from datetime import datetime

async def human_delay(a=200, b=800):
    await asyncio.sleep(random.uniform(a/1000, b/1000))

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False,
                                          args=["--disable-blink-features=AutomationControlled"])
        context = await browser.new_context(
            viewport={"width": 1400, "height": 900},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Safari/537.36",
            locale="zh-CN",
            timezone_id="Asia/Shanghai"
        )
        page = await context.new_page()

        # 模拟人类移动鼠标
        # await page.mouse.move(200, 300)
        # await human_delay()
        # await page.mouse.move(400, 500)
        await human_delay()

        await page.goto("https://www.fangdi.com.cn/old_house/old_house.html", timeout=60000)

        # 模拟滚动
        # for _ in range(5):
        #     await page.mouse.wheel(0, random.randint(200, 600))
        #     await human_delay()

        # 等页面 JS 渲染完成
        await page.wait_for_selector(".today_sign", timeout=60000)

        # 获取昨日成交量
        data1 = await page.evaluate("""
            () => {
                const t = document.querySelector('#z_sell_num_p');
                return t ? t.innerText.slice(0,-1) : "empty";
            }
        """)
        data2 = await page.evaluate("""
            () => {
                const t = document.querySelector('#z_sell_area_p');
                return t ? t.innerText.slice(0,-1) : "empty";
            }
        """)
        print(data1)

        await page.goto("https://www.fangdi.com.cn/index.html", timeout=60000)
        await human_delay()
        # 等页面 JS 渲染完成
        await page.wait_for_selector("#all_housingSupply", timeout=60000)

        data3 = await page.evaluate("""
            () => {
                const t = document.querySelector('#all_housingSupply > span:nth-child(3) i:nth-child(1)');                                   
                return t ? t.innerText : "empty";
            }
        """)

        data4 = await page.evaluate("""
            () => {
                const t = document.querySelector('#all_housingSupply > span:nth-child(3) i:nth-child(2)');                                   
                return t ? t.innerText : "empty";
            }
        """)

        data5 = await page.evaluate("""
            () => {
                const t = document.querySelector('#all_housingSupply > span:nth-child(4) i:nth-child(1)');                                   
                return t ? t.innerText : "empty";
            }
        """)

        data6 = await page.evaluate("""
            () => {
                const t = document.querySelector('#all_housingSupply > span:nth-child(4) i:nth-child(2)');                                   
                return t ? t.innerText : "empty";
            }
        """)

        # ----------- 写入 CSV（每天追加） ------------
        csv_file = "fangdi_data.csv"
        today = datetime.now().strftime("%Y-%m-%d")

        file_exists = os.path.exists(csv_file)

        with open(csv_file, "a", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)

            # 如果文件不存在，先写标题
            if not file_exists:
                writer.writerow(["日期", "昨日二手房成交套数", "昨日二手房成交面积", "二手房住宅挂牌量", "二手房住宅挂牌面积（万㎡）", "一手房普通住宅套数", "一手房普通住宅面积（万㎡）"])

            writer.writerow([today, data1, data2, data5, data6, data3, data4])

        print(f"保存成功：{csv_file}")

        await browser.close()

asyncio.run(run())
