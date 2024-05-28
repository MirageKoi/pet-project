import asyncio

from aiohttp import web
from asyncpg import Pool
from controllers.users_controller import PostController, UsersController
from repositories.users_repository import UsersRepository
from services.users_service import UsersService
from utils.db import init_db

from repositories.posts_repository import PostsRepository
from services.posts_service import PostsService


async def init_repositories(pool: Pool) -> UsersRepository:
    return UsersRepository(pool)


async def init_services(users_repository: UsersRepository) -> UsersService:
    return UsersService(users_repository)


async def init_controllers(users_service: UsersService) -> UsersController:
    return UsersController(users_service)


@web.middleware
async def error_middleware(request, handler):
    try:
        return await handler(request)
    except web.HTTPException:
        raise
    except asyncio.CancelledError:
        raise
    except Exception as e:
        return web.json_response({"status": "failed", "reason": str(e)}, status=400)


async def init_app():
    """Initialize the application server."""
    app = web.Application(middlewares=[error_middleware])
    # app = web.Application()
    # Create a database context
    pool = await init_db({})
    posts_repository = PostsRepository(pool=pool)
    post_service = PostsService(posts_repository=posts_repository)
    repositories = await init_repositories(pool=pool)
    services = await init_services(users_repository=repositories)
    controllers = await init_controllers(users_service=services)
    post_controller = PostController(post_service=post_service)

    app.router.add_get("/", controllers.hello_world)
    app.router.add_get("/users", controllers.get_user_list)
    app.router.add_get("/users/{id}", controllers.get_user_detail)
    app.router.add_post("/users", controllers.create_user)
    app.router.add_delete("/users/{id}", controllers.delete_user)
    app.router.add_put("/users/{id}", controllers.update_user)

    app.router.add_get("/posts", post_controller.get_post_list)
    app.router.add_post("/posts", post_controller.create_post)
    app.router.add_get("/posts/{post_id}", post_controller.get_post_detail)
    app.router.add_put("/posts/{post_id}", post_controller.update_post)
    app.router.add_delete("/posts/{post_id}", post_controller.delete_post)

    return app


if __name__ == "__main__":
    app = init_app()
    web.run_app(app)
