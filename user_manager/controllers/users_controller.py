from dataclasses import dataclass

from aiohttp import web
from aiohttp.web import Request, Response
from models.posts import Post, PostList
from models.user import User, UserList
from services.posts_service import PostsService
from services.users_service import UsersService


@dataclass
class UsersController:
    users_service: UsersService

    async def hello_world(self, request: Request) -> Response:
        return web.Response(text="Hello world")

    async def get_user_list(self, request: Request) -> Response:
        records = await self.users_service.all()
        response = UserList(users=records)
        users_data = response.model_dump_json(indent=2)
        return web.Response(body=users_data, content_type="application/json")

    async def get_user_detail(self, request: Request) -> Response:
        user_id = int(request.match_info.get("id"))
        record = await self.users_service.get(user_id=user_id)
        return web.Response(body=record.model_dump_json(), content_type="application/json")

    async def create_user(self, request: Request) -> Response:
        request_body = await request.post()
        record = await self.users_service.create(item=request_body)
        response = record.model_dump_json(indent=2)
        return web.Response(body=response, content_type="application/json")

    async def update_user(self, request: Request) -> Response:
        user_id = int(request.match_info.get("id"))
        request_body = await request.post()
        updated_user = await self.users_service.update(user_id=user_id, item=request_body)
        return web.Response(body=updated_user.model_dump_json(), content_type="application/json")

    async def delete_user(self, request: Request) -> Response:
        user_id = int(request.match_info.get("id"))
        await self.users_service.delete(user_id=user_id)
        return web.json_response(data={"text": "User has been deleted"}, status=200)


@dataclass
class PostController:
    post_service: PostsService

    async def get_post_list(self, request: Request):
        result = await self.post_service.get_post_all()
        response = PostList(posts=result).model_dump_json(indent=2)
        return Response(body=response, content_type="application/json")

    async def create_post(self, request: Request):
        request_body = await request.post()
        result = await self.post_service.create_post(request_body)
        response = result.model_dump_json(indent=2)
        return Response(body=response, content_type="application/json")

    async def get_post_detail(self, request: Request):
        post_id = int(request.match_info["post_id"])
        record = await self.post_service.get_post_detail(post_id=post_id)
        response = record.model_dump_json(indent=2)
        return Response(body=response, content_type="application/json")

    async def update_post(self, request: Request):
        post_id = int(request.match_info["post_id"])
        request_body = dict(await request.post())
        record = await self.post_service.update_post(post_id=post_id, item=request_body)
        response = record.model_dump_json(indent=2)
        return Response(body=response, content_type="application/json")

    async def delete_post(self, request: Request):
        post_id = int(request.match_info["post_id"])
        await self.post_service.delete_post(post_id=post_id)
        return Response(text="post with id {id} has been deleted".format(id=post_id))
