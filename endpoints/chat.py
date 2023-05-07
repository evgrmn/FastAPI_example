from fastapi import APIRouter, Request, WebSocket, WebSocketDisconnect
from fastapi.templating import Jinja2Templates

from control.chat import ConnectionManager

TEMPLATES = Jinja2Templates(directory=str("templates"))

router = APIRouter()

manager = ConnectionManager()


@router.get("/chat", summary="Websocket chat")
async def chat(
    request: Request,
):
    """
    Websocket chat is available at http://localhost:8000/chat
    """

    return TEMPLATES.TemplateResponse(
        "index.html",
        {
            "request": request, 
            "variable": "Thus, variables can be passed to index.html, which must be enclosed in {{}}, e.g. {{variable}}"},
    )


@router.websocket("/api/v1/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    """
    Initializes a new websocket connection for each browser
    Handles messages
    Disconnects websocket
    """
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")