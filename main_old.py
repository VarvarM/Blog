import uvicorn
from fastapi import FastAPI, Form, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from funcs import create_tables, insert_state, select_all_states, insert_basic, select_curr_state, update_state, \
    delete_curr_state, select_all_comments, insert_comment, delete_curr_comment, select_curr_user
from datetime import datetime
from fastapi.templating import Jinja2Templates

app = FastAPI(title='Blog')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
templates = Jinja2Templates(directory="templates")


@app.on_event("startup")
async def startup_event():
    redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


@app.get("/long_operation")
@cache(expire=30)
def get_long_op():
    return "Много много данных, которые вычислялись сто лет"


create_tables()
insert_basic()


@app.get('/')
def get_all_states():
    a = select_all_states().all()
    data = '''<h1 align='center'>Дневник</h1>
            <form action="new_state" method="get">
            <input type="submit" value="Новая статья" />
            </form>'''
    for val in a:
        data += f"<h2><a href='/state/{val[0]}'>{val[1]}</a></h2>"
        data += f'<h4>{f"{val[3]} {val[4]:%d.%m.%Y}"}</h4>'
        data += f"<p>{val[2]}</p>"
        data += f"💬{len(select_all_comments(val[0]).all())}"
    return HTMLResponse(content=data)


@app.get('/new_state')
def new():
    return FileResponse('templates/create.html')


@app.api_route('/postdata', methods=['GET', 'POST'])
def postdata(user=Form(min_length=2), name=Form(), text=Form()):
    new = [name, text, user, datetime.now()]
    insert_state(new)
    return RedirectResponse('/', status_code=303)


@app.get('/state/{state_id}')
def current_state(state_id: int):
    curr = select_curr_state(state_id).all()
    comm = select_all_comments(state_id).all()
    data = '''<h1 align='center'>Дневник</h1>
                <form action="../" method="get">
                <input type="submit" value="На главную" />
                </form>'''
    for val in curr:
        data += f"<h2>{val[1]}</h2>"
        data += f'<h4>{f"{val[3]} {val[4]:%d.%m.%Y}"}</h4>'
        data += f"<p>{val[2]}</p>"
    data += f'''<form action="/edit/{state_id}" method="get" style="display: inline; margin-right: 30px;">
                    <input type="submit" value="Изменить"/>
                </form>
                <form action="/delete/{state_id}" method="get" style="display: inline-block;">
                    <input type="submit" value="Удалить"/>
                </form>'''

    data += f'''<br><h2 style="display: inline; margin-right: 10px;">Комментарии</h2>
                <form action="/state/{state_id}/new_comment" method="get" style="display: inline;">
                    <input type="submit" value="Добавить"/>
                </form>'''

    for phrase in comm:
        data += f'<h4>{phrase[3]} {phrase[4]:%d.%m.%Y}</h4><p>{phrase[2]}</p>'
        data += f'''<form action="/state/{state_id}/delete/{phrase[0]}" method="get" style="display: inline;">
                    <input type="submit" value="Удалить"/>
                </form>'''
    return HTMLResponse(content=data)


@app.get('/edit/{state_id}', response_class=HTMLResponse)
def edit_state(req: Request, state_id: int):
    return templates.TemplateResponse('edit.html', {"request": req, "state_id": state_id})


@app.api_route('/putdata', methods=['GET', 'POST'])
def putdata(state_id: int = Form(), user=Form(min_length=2), name=Form(), text=Form()):
    new = [state_id, name, text, user, datetime.now()]
    update_state(new)
    return RedirectResponse('/', status_code=303)


@app.get('/delete/{state_id}', response_class=HTMLResponse)
def delete_state(req: Request, state_id: int):
    return templates.TemplateResponse('delete.html', {"request": req, "state_id": state_id})


@app.api_route('/deletedata', methods=['GET', 'POST'])
def delete_data(req: Request, state_id: int = Form(), user=Form(min_length=2)):
    if delete_curr_state(state_id, user).rowcount:
        return RedirectResponse('/', status_code=303)
    return templates.TemplateResponse('error_delete.html', {"request": req, "state_id": state_id})


@app.get('/state/{state_id}/new_comment', response_class=HTMLResponse)
def add_new_comment(req: Request, state_id: int):
    return templates.TemplateResponse('comm_create.html', {"request": req, "state_id": state_id})


@app.api_route('/add_comment', methods=['GET', 'POST'])
def add_comment(state_id: int = Form(), user=Form(min_length=2), text=Form()):
    new = [state_id, text, user, datetime.now()]
    insert_comment(new)
    return RedirectResponse(f'/state/{state_id}', status_code=303)


@app.get('/state/{state_id}/delete/{comment_id}', response_class=HTMLResponse)
def delete_comment(req: Request, state_id: int, comment_id: int):
    return templates.TemplateResponse('delete_comment.html',
                                      {"request": req, "state_id": state_id, "comment_id": comment_id})


@app.api_route('/delete_comm', methods=['GET', 'POST'])
def delete_comm(req: Request, state_id: int = Form(), comment_id: int = Form(), user=Form(min_length=2)):
    if delete_curr_comment(comment_id, user).rowcount:
        return RedirectResponse(f'/state/{state_id}', status_code=303)
    return templates.TemplateResponse('error_delete.html', {"request": req, "state_id": state_id})


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = select_curr_user(form_data.username, form_data.password)
    if user:
        return {"access_token": user[1], "token_type": "bearer"}
    else:
        raise HTTPException(status_code=400, detail="Неверный логин или пароль")


@app.get("/users/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    print(token)
    return {"user": "mikhail"}


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
