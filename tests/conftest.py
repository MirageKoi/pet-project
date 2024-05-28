from user_manager.main import init_app

import pytest
from aiohttp import web
from user_manager.controllers.users_controller import UsersController

index = UsersController.hello_world

@pytest.fixture
async def cli(aiohttp_client, db):
    app = await init_app()
    return await aiohttp_client(app)