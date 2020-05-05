from starlette.applications import Starlette
from starlette.responses import UJSONResponse, PlainTextResponse
from starlette.routing import Route, Mount
from starlette.background import BackgroundTask


async def homepage(request):
    return PlainTextResponse("200 UwU")

def new_screen(username, token):
    os.system(f"cp -r login users/{username}")
    os.system(f'echo -n "{token}" > users/{username}/authToken.txt')
    os.system(f"screen -dmS {username}")
    os.system(f'screen -r {username} -X stuff "cd users/{username} && python3 main.py \n"')

def remove_screen(username):
    os.system(f"screen -S {username} -X quit")
    os.system(f"rm -rf users/{username}")

async def selfbot_login(request):
    username = request.path_params['username']
    token = request.path_params['token']

    task = BackgroundTask(new_screen, username=username, token=token)
    message = {'status': 'success'}

    return UJSONResponse(message, background=task)
    

async def selfbot_logout(request):
    username = request.path_params['username']
    task = BackgroundTask(remove_screen, username=username)
    message = {'status': 'failed'}

    return UJSONResponse(message, background=task)


routes = [
    Route('/', endpoint=homepage).
    Mount('/api', routes=[
        Mount('/v1', routes=[
            Mount('/selfbot', routes=[
                Route('/login', endpoint=selfbot_login, methods=['POST']),
                Route('/logout', endpoint=selfbot_logout, methods=['POST']),
            ]),
        ]),
    ]),
]


app = Starlette(debug=True, routes=routes)
