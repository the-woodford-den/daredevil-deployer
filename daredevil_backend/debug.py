import asyncio
import debugpy

debugpy.listen(("127.0.0.1", 5678))
print("Waiting for debugger to attach on port 5678...")
debugpy.wait_for_client()
print("Debugger attached.")

from hypercorn.asyncio import serve
from hypercorn.config import Config
from main import app

config = Config.from_toml("hypercorn.toml")
asyncio.run(serve(app, config))
