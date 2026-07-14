from fastapi import FastAPI,Request,WebSocket,Cookie,status,Form
from fastapi.responses import RedirectResponse,HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import chat_process
from urllib.parse import unquote
import asyncio
import json

app = FastAPI()
c = chat_process.req()

pp="개인정보 처리방침\n\n[가상여친](이하 '가상여친 서비스')는 이용자의 개인정보를 중요시하며, \"개인정보 보호법\" 등 관련 법령을 준수하고 있습니다. 본 방침은 이용자가 제공하는 개인정보가 어떠한 용도와 방식으로 이용되고 있으며, 개인정보 보호를 위해 어떠한 조치가 취해지고 있는지 알려드립니다.\n\n1. 수집하는 개인정보의 항목 및 수집목적\n본 서비스는 이용자 식별 및 서비스 제공을 위해 아래와 같은 개인정보를 수집하고 있습니다.\n\n* 수집 항목: IP 주소, 쿠키(Cookie), 사용자 대화 내역\n* 수집 목적: \n  - 서비스 이용에 따른 본인 식별 및 부정 이용 방지\n  - 대화 맥락 유지를 통한 LLM 채팅 서비스 제공 및 서비스 품질 개선\n  - 시스템 안정성 확보 및 보안 미비점 점검\n\n2. 개인정보의 수집 방법\n* 이용자가 서비스를 이용하는 과정에서 자동 생성되어 수집되거나 대화 창 입력 등을 통해 수집됩니다.\n\n3. 개인정보의 보유 및 이용기간\n이용자 식별 및 서비스 제공 목적이 달성된 후에는 해당 정보를 지체 없이 파기합니다. 단, 관계법령의 규정에 의하여 보존할 필요가 있는 경우 아래와 같이 관계법령에서 정한 일정한 기간 동안 정보를 보관합니다.\n\n* 보존 항목: IP 주소, 서비스 이용 기록\n* 보존 근거: 통신비밀보호법 (웹사이트 방문기록: 3개월)\n* 기타 대화 내역 및 쿠키: 목적 달성 시 즉시 파기\n\n4. 개인정보의 파기절차 및 방법\n원칙적으로 개인정보 수집 및 이용목적이 달성된 후에는 해당 정보를 지체 없이 파기합니다. 파기절차 및 방법은 다음과 같습니다.\n\n* 파기절차: 목적 달성 후 내부 방침 및 기타 관련 법령에 의한 정보보호 사유에 따라 일정 기간 저장된 후 파기됩니다.\n* 파기방법: 전자적 파일형태로 저장된 개인정보는 기록을 재생할 수 없는 기술적 방법을 사용하여 삭제합니다.\n\n5. 이용자의 권리와 그 행사방법\n* 이용자는 언제든지 등록되어 있는 자신의 개인정보를 조회하거나 수정할 수 있으며 동의철회(서비스 이용 중단 등)를 요청할 수 있습니다.\n* 이용자가 개인정보의 오류에 대한 정정을 요청하신 경우에는 정정을 완료하기 전까지 당해 개인정보를 이용 또는 제공하지 않습니다.\n\n6. 쿠키(Cookie)의 설치·운영 및 거부에 관한 사항\n본 서비스는 이용자의 정보를 수시로 저장하고 찾아내는 ‘쿠키(cookie)’ 등을 운용합니다. 쿠키란 웹사이트를 운영하는데 이용되는 서버가 이용자의 브라우저에 보내는 아주 작은 텍스트 파일로서 이용자의 컴퓨터 하드디스크에 저장되기도 합니다.\n\n* 쿠키 사용 목적: 이용자의 접속 빈도나 방문 시간 등을 분석 및 이용자 식별 기반 서비스 제공\n* 쿠키 설치 거부 방법: 이용자는 쿠키 설치에 대한 선택권을 가지고 있습니다. 웹브라우저에서 옵션을 설정함으로써 모든 쿠키를 허용하거나, 쿠키가 저장될 때마다 확인을 거치거나, 모든 쿠키의 저장을 거부할 수도 있습니다. 단, 쿠키 설치를 거부하였을 경우 서비스 제공(로그인 및 대화 유지 등)에 어려움이 있을 수 있습니다.\n\n7. 개인정보 보호책임자 및 상담·신고\n본 서비스는 이용자의 개인정보를 보호하고 관련 불만을 처리하기 위하여 아래와 같이 개인정보 보호책임자를 지정하고 있습니다.\n\n* 개인정보 보호책임자: 유연우\n* 문의처: yuyeonwoo0812@gmail.com\n\n이용자는 본 서비스를 이용하시며 발생하는 모든 개인정보 보호 관련 민원을 개인정보 보호책임자에게 신고하실 수 있습니다. 신속하게 답변을 드릴 수 있도록 노력하겠습니다.\n\n본 방침은 2026.7.12부터 시행됩니다."

user_data={}

app.mount("/static",StaticFiles(directory="static"),name="static")

t = Jinja2Templates("templates")

@app.get('/',response_class=HTMLResponse)
async def read(request: Request, udata: str=Cookie(None),user_data: str=Cookie(None)):
    if user_data is None:
        return RedirectResponse("/signup",status.HTTP_303_SEE_OTHER)
    elif udata is None:
        return t.TemplateResponse(request=request,name="privacy_policy.html",context={"privacy_policy":pp})
    else:
        ud = json.loads(user_data)
        uname=ud[0]
        usdata=ud[1]
        print(ud)
        return t.TemplateResponse(request=request,name="index.html",context={"uname":uname})


@app.websocket('/ws')
async def read(websocket:WebSocket):
    await websocket.accept()
    raw_cookie = websocket.cookies.get("user_data")
    user_data = json.loads(unquote(raw_cookie)) if raw_cookie else ["guest", ["", []]]
    uname=user_data[0]
    pwd = user_data[1][0]
    mem = user_data[1][1]
    while True:
        cmd = await websocket.receive_text()
        try:
            cmd_json = json.loads(cmd)
            if cmd_json['type']=='modelcg':
                print(f"모델변경 : {cmd_json['model']}")

        except:
            if cmd=="/test":
                response="Hello world!"
            elif cmd=="/reset_conv":
                mem.clear()
                response="대화 내역이 초기화됨."
            elif cmd=="/clear":
                response="clear-chat"
            else:
                if len(mem)<10:
                    mem.append({
                        "role": "user",
                        "content": cmd
                        })
                else:
                    mem.pop(0)
                    mem.append({
                        "role": "user",
                        "content": cmd
                        })
                c.memory=mem
                response=c.request()
                if len(mem)<10:
                    mem.append({
                        "role": "assistant",
                        "content": response
                        })
                else:
                    mem.pop(0)
                    mem.append({
                        "role": "assistant",
                        "content": response
                        })
        
            await websocket.send_json({"msg":response,"mem":mem,"uname":uname,"pwd":pwd})

@app.get("/privacy_policy",response_class=HTMLResponse)
async def read(request:Request):
    return t.TemplateResponse(request=request,name="privacy_policy.html",context={"privacy_policy":pp})


@app.get("/ck")
async def cookie():
    rd = RedirectResponse("/",status.HTTP_303_SEE_OTHER)
    rd.set_cookie(key="udata",value="True",httponly=True,secure=True,max_age=60*60*24*7)
    return rd

@app.get("/signup",response_class=HTMLResponse)
async def read(request:Request):
    return t.TemplateResponse(request=request,name="signup.html")

@app.post("/add_db",response_class=HTMLResponse)
async def read(request:Request, uname=Form(None), pwd=Form(None)):
    if not uname or not pwd:
        return t.TemplateResponse(request=request,name="signup.html",context={"err":"아이디랑 비번은 필수임"})
    elif len(pwd)<10:
        return t.TemplateResponse(request=request,name="signup.html",context={"err":"비번 길이는 10자리 이상"})
    else:
        user_data[uname]=(pwd,[])
        print(user_data)
        return t.TemplateResponse(request=request,name="login.html")

@app.get("/login",response_class=HTMLResponse)
async def read(request:Request):
    return t.TemplateResponse(request=request,name="login.html")



@app.post("/login_try",response_class=HTMLResponse)
async def read(request:Request, uname=Form(None), pwd=Form(None),udata: str=Cookie(None)):
    print(user_data)
    if not uname in user_data.keys():
        return t.TemplateResponse(request=request,name="login.html",context={'err':'그런 아이디는 없는데요ㅠ'})
    elif user_data[uname][0]!=pwd:
        return t.TemplateResponse(request=request,name="login.html",context={'err':'비번 틀림 ㅋ'})
    else:
        if udata is None:
            res = t.TemplateResponse(request=request,name="privacy_policy.html",context={"privacy_policy":pp})
            res.set_cookie(key="user_data",value=json.dumps((uname,user_data[uname])),httponly=True,secure=True)
            return res
        else:
            res=t.TemplateResponse(request=request,name="index.html")
            res = t.TemplateResponse(request=request,name="privacy_policy.html",context={"privacy_policy":pp})
            res.set_cookie(key="user_data",value=json.dumps((uname,user_data[uname])),httponly=True,secure=True)
            return res

@app.get("/logout",response_class=HTMLResponse)
async def read(request:Request):
    res = t.TemplateResponse(request=request,name="logout.html")
    res.delete_cookie("user_data")
    return res