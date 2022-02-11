from aiohttp import web
import asyncio
from ubot.vars import Var
from pyrogram import idle
from ubot import app
from ubot.bot2 import bot2

routes = web.RouteTableDef()
loop = asyncio.get_event_loop()


async def web_server():
    web_app = web.Application(client_max_size=30000000)
    web_app.add_routes(routes)
    return web_app


@routes.get("/", allow_head=True)
async def root_route_handler(request):
    return web.json_response({
        "server_status": "running",
    })


async def start_services():
    print("----------------------------- DONE -----------------------------")
    print()
    appx = web.AppRunner(await web_server())
    await appx.setup()
    bind_address = "0.0.0.0" if Var.ON_HEROKU else Var.BIND_ADDRESS

    await web.TCPSite(appx, bind_address, Var.PORT).start()
    #await app.start()
    await bot2.start()
    await idle()


if __name__ == "__main__":
    try:
        loop.run_until_complete(start_services())
    except KeyboardInterrupt:
        print(
            "----------------------- Service Stopped -----------------------")
