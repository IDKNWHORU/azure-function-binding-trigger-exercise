import azure.functions as func
import logging

# .venv는 python의 가상 환경 디렉토리
# .vscode는 visual studio code 설정 파일들이 위치함.
# .functionignore는 Azure Function App을 배포할 때 업로드 하지 않을 파일이나 폴더를 지정함.
# .gitignore는 github에 업로드 하지 않을 파일이나 폴더를 지정함.
# function_app.py Azure Funtion App의 진입점 역할을 함. 여기서 트리거와 바인딩을 설정하거나 비즈니스 로직을 구현.
# host.json은 Function App의 설정을 담당함
# local.settings.json은 로컬 개발 환경에서 사용되는 환경 변수를 설정함.
# requirements.txt는 Function App에서 사용할 라이브러리(패키지)를 지정함. (pip install -r requirements.txt로 설치)

app = func.FunctionApp()

@app.event_hub_message_trigger(arg_name="azeventhub", event_hub_name="test-hub3",
                               connection="el31eventhub_RootManageSharedAccessKey_EVENTHUB") 
def eventhub_trigger(azeventhub: func.EventHubEvent):
    logging.info('Python EventHub trigger processed an event: %s',
                azeventhub.get_body().decode('utf-8'))

# Azure Portal에서 실습한 것: Event Hub에 데이터가 수신될 때마다 함수가 호출되는 방식
# VS Code에서 함수를 실행하는 것: 

@app.function_name(name="eventhub_output")
@app.route(route="eventhub_output", methods=["POST"])
@app.event_hub_output(arg_name="event", event_hub_name="test-hub3",
                      connection="el31eventhub_RootManageSharedAccessKey_EVENTHUB")
def eventhub_output(req: func.HttpRequest, event: func.Out[str]) -> func.HttpResponse:
    req_body = req.get_body().decode('utf-8')

    logging.info("HTTP trigger function received a request: %s", req_body)

    event.set(req_body)

    return func.HttpResponse("Event Hub output function executed successfully.", status_code=200)