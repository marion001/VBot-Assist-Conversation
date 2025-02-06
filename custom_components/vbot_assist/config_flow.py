from homeassistant.helpers import config_validation as cv
from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
from .const import DOMAIN, VBot_URL_API, VBot_PROCESSING_MODE
from typing import Optional
import voluptuous as vol
import logging
import aiohttp

_LOGGER = logging.getLogger(__name__)

# Schema chứa cả URL API và Mode
STEP_USER_DATA_SCHEMA = vol.Schema({
    vol.Optional(VBot_URL_API, default="http://192.168.14.113:5002"): str,
    vol.Required(VBot_PROCESSING_MODE, default="chatbot"): vol.In(
        {"chatbot": "Luồng Chatbot", "processing": "Luồng Xử Lý Chính"}
    ),
})

Msg_API_Error = "Vui lòng kiểm tra lại địa chỉ API, cổng Port hoặc VBot không hoạt động" 

# Xử lý, Kiểm tra cấu hình khi nhập URL
class VBotAssistantConversationConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input: Optional[dict[str, str]] = None) -> FlowResult:
        errors = {}

        if user_input is None:
            return self.async_show_form(step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors)

        try:
            base_url = user_input[VBot_URL_API]
            vbot_mode = user_input[VBot_PROCESSING_MODE]

            if not base_url:
                errors["base"] = "Cần phải nhập URL API hợp lệ gồm cả cổng PORT"
                return self.async_show_form(step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors)

            response = await self.fetch_conversation_response(base_url, "bạn tên là gì")

            if response:
                _LOGGER.info(f"[VBot Assist] Chế độ được chọn: {vbot_mode}")
                return self.async_create_entry(title="VBot Assistant", data=user_input)  
            else:
                errors["base"] = f"Không kiểm tra được dữ liệu {Msg_API_Error}"
        except ValueError as e:
            errors["base"] = str(e)
            _LOGGER.error("[VBot Assist] Lỗi xác thực API: %s", e)

        return self.async_show_form(step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors)

    async def fetch_conversation_response(self, base_url: str, user_input: str) -> str:
        url = f"{base_url}/"
        payload = {
            "type": 3,
            "data": "main_processing",
            "action": "processing",
            "value": user_input
        }
        headers = {"Content-Type": "application/json"}
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        if "success" in data and data["success"]:
                            _LOGGER.info(f"[VBot Assist] Cấu hình API thành công: {data.get('message')}")
                            return True
                        else:
                            _LOGGER.error(f"[VBot Assist] Lỗi Cấu Hình API, {Msg_API_Error}: {data}")
                            return None
                    else:
                        _LOGGER.error(f"[VBot Assist] Lỗi kết nối API VBot, {Msg_API_Error}: {await response.text()}")
                        return None
        except aiohttp.ClientError as e:
            _LOGGER.error(f"[VBot Assist] Lỗi gửi yêu cầu tới API: {e}")
            return None
        except Exception as e:
            _LOGGER.error(f"[VBot Assist] Lỗi khi gọi API: {e}")
            return None
