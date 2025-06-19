from fastapi import APIRouter, HTTPException
import httpx

from ..config import settings
from ..schemas import SendForm

router = APIRouter()


@router.post("/send-form")
async def send_form(
    request: SendForm,
):

    try:
        bot_token = settings.TELEGRAM_BOT_TOKEN
        chat_id = settings.TELEGRAM_CHAT_ID

        if not bot_token:
            raise HTTPException(
                status_code=500,
                detail="Telegram bot token is not configured"
            )
        
        # Construct the message
        def escape_markdown(text: str) -> str:
            escape_chars = r"_*[]()~`>#+-=|{}.!"
            return ''.join(f"\\{c}" if c in escape_chars else c for c in text)

        text = (
            f"🔔 *New message*:\n\n"
            f"*Name*: {escape_markdown(request.name)}\n"
            f"*Email*: {escape_markdown(request.email)}\n"
            f"*Message*:\n{escape_markdown(request.message)}"
        )

       # Send message to Telegram
        async with httpx.AsyncClient() as client:
            telegram_response = await client.post(
                f"https://api.telegram.org/bot{bot_token}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": text,
                    "parse_mode": "MarkdownV2"
                }
            )

        telegram_data = telegram_response.json()

        if not telegram_response.is_success:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "Failed to send message",
                    "details": telegram_data
                }
            )

        return {
            "success": True,
            "result": telegram_data.get("result")
        }

    except httpx.RequestError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Network error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )
