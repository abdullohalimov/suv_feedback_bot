import aiohttp
import asyncio

async def certificate_download(cert_id):
    url = "http://91.213.99.234:8000/api/request/certificate"
    payload = {
        "certificate_id": f"{cert_id}",
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as resp:
            if resp.content_type == "application/pdf":
                return await resp.read()
            elif resp.content_type == "text/html":
                return False


# asyncio.run(certificate_download('00053'))