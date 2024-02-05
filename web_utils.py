import asyncio,logging,traceback, aiohttp, datetime
from aiohttp import web
from config import Config

async def create_server():
    app = web.AppRunner(await web_server())
    await app.setup()
    await web.TCPSite(app, "0.0.0.0", Config.PORT).start()
    asyncio.create_task(ping_server())

async def ping_server():
    sleep_time = Config.PING_INTERVAL
    while True:
        await asyncio.sleep(sleep_time)
        try:
            async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=10)
            ) as session:
                async with session.get(Config.APP_URL) as resp:
                    logging.info(f"Pinged server with response: {resp.status}")
        except TimeoutError:
            logging.warning("Couldn't connect to the site URL..!")
        except Exception:
            traceback.print_exc()

async def web_server():
    web_app = web.Application(client_max_size=30000000)
    web_app.add_routes(routes)
    return web_app


routes = web.RouteTableDef()

@routes.get("/", allow_head=True)
async def root_route_handler(request):
    runtime = datetime.datetime.now()
    t = runtime - Config.START_TIME
    runtime = str(datetime.timedelta(seconds=t.seconds))

    res = {
        "status": "running",
        "bot": Config.BOT_USERNAME,
        "runtime": runtime,
    }
    return aiohttp.web.json_response(res)