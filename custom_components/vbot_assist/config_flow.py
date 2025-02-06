from homeassistant.helpers import config_validation as cv
from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
from .const import DOMAIN, VBot_URL_API
from typing import Optional
import voluptuous as vol
import logging
import aiohttp

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema({
    vol.Optional(VBot_URL_API, default="http://192.168.14.113:5002"): str,
})

Msg_API_Error = "Vui lòng kiểm tra lại địa chỉ API, cổng Port hoặc VBot không hoạt động" 

#Xử lý, Kiểm tra cấu hình khi nhập URL
class VeniceAIConversationConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    #async def async_step_user(self, user_input: dict[str, str] | None = None) -> FlowResult:
    async def async_step_user(self, user_input: Optional[dict[str, str]] = None) -> FlowResult:
        errors = {}
        """Xử lý bước đầu tiên của quá trình cấu hình.""" 
        errors["base"] ="Nhập URL API VBot để kết nối"
        if user_input is None:
            return self.async_show_form(step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors)
        errors = {}
        try:
            base_url = user_input[VBot_URL_API]
            if not base_url:
                errors["base"] = "Cần phải nhập URL API hợp lệ gồm cả cổng PORT"
                return self.async_show_form(step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors)
            response = await self.fetch_conversation_response(base_url, "bạn tên là gì")
            #Nếu phản hồi true, tạo entry
            if response:
                return self.async_create_entry(title="VBot Assistant", data=user_input)  
            else:
                errors["base"] = "Không thể lấy dữ liệu trò chuyện"
        except ValueError as e:
            errors["base"] = str(e)
            _LOGGER.error("[VBot Assist] Lỗi xác thực API: %s", e)
        #Nếu có lỗi, hiển thị lại form để người dùng nhập lại
        return self.async_show_form(step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors)

    async def fetch_conversation_response(self, base_url: str, user_input: str) -> str:
        url = f"{base_url}/"
        payload = {
            "type": 3,
            "data": "main_processing",
            "action": "processing",
            "value": user_input
        }
        headers = {
            "Content-Type": "application/json"
        }
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
