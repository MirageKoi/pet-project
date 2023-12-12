from aiohttp import web
from aiohttp.web import Request, Response
from models.user import UserCreateValidation, UserList
from pydantic.dataclasses import dataclass
from services.users_service import UsersService


@dataclass
class UsersController(object):
    users_service: UsersService

    async def hello_world(self, request: Request) -> Response:
        return web.Response(text="Hello world")

    async def user_list(self, request: Request) -> Response:
        records = await self.users_service.all()
        response = UserList(users=records)
        return web.Response(body=response.model_dump_json(), content_type="application/json")

    async def user_detail(self, request: Request) -> Response:
        user_id = int(request.match_info.get("id"))
        record = await self.users_service.get(user_id=user_id)
        return web.Response(body=record.model_dump_json(), content_type="application/json")

    async def user_create(self, request: Request) -> Response:
        body = await request.post()
        new_user = UserCreateValidation(email=body.get("email", None), age=body.get("age", None))
        record = await self.users_service.create(new_user=new_user)
        return web.Response(body=record.model_dump_json(), content_type="applicaiton/json")

    async def user_update(self, request: Request) -> Response:
        user_id = int(request.match_info.get("id"))
        body = await request.post()
        updated_user = await self.users_service.update(user_id=user_id, **body)
        return web.Response(body=updated_user.model_dump_json(), content_type="applicatoin/json")

    async def user_delete(self, request: Request) -> Response:
        user_id = int(request.match_info.get("id"))
        await self.users_service.delete(user_id=user_id)
        return web.json_response(data={"text": "User has been deleted"}, status=200)
