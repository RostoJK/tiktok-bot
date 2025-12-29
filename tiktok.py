import aiohttp

async def get_tiktok_video(url: str):
    api = f"https://www.tikwm.com/api/?url={url}"

    async with aiohttp.ClientSession() as session:
        async with session.get(api) as resp:
            if resp.status != 200:
                return None

            data = await resp.json()

            try:
                return "https://www.tikwm.com" + data["data"]["play"]
            except:
                return None