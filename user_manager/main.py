from aiohttp import web
from asyncpg import Pool
from controllers.users_controller import UsersController
from repositories.users_repository import UsersRepository
from services.users_service import UsersService
from utils.db import init_db


async def init_repositories(pool: Pool) -> UsersRepository:
    return UsersRepository(pool)


async def init_services(users_repository: UsersRepository) -> UsersService:
    return UsersService(users_repository)


async def init_controllers(users_service: UsersService) -> UsersController:
    return UsersController(users_service)


@web.middleware
async def error_middleware(request, handler):
    try:
        response = await handler(request)

        return response

    except ValueError as e:
        return web.json_response({"error": str(e)}, status=404)

    except Exception as e:
        return web.json_response({"error": str(e)})


async def init_app():
    """Initialize the application server."""
    app = web.Application(middlewares=[error_middleware])
    # Create a database context
    pool = await init_db({})
    repositories = await init_repositories(pool=pool)
    services = await init_services(users_repository=repositories)
    controllers = await init_controllers(users_service=services)
    app.router.add_get("/", controllers.hello_world)
    app.router.add_get("/users", controllers.user_list)
    app.router.add_get("/users/{id}", controllers.user_detail)
    app.router.add_post("/users", controllers.user_create)
    app.router.add_delete("/users/{id}", controllers.user_delete)
    app.router.add_put("/users/{id}", controllers.user_update)

    return app


if __name__ == "__main__":
    app = init_app()
    web.run_app(app)
