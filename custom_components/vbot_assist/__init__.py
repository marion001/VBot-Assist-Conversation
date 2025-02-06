from __future__ import annotations
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers import config_validation as cv
from homeassistant.components import conversation
from homeassistant.helpers import intent
#from .config_flow import VBotAssistantConversationConfigFlow
from .const import DOMAIN, VBot_URL_API, VBot_PROCESSING_MODE, VBot_LANGUAGES
import logging
import aiohttp

_LOGGER = logging.getLogger(__name__)
CONFIG_SCHEMA = cv.config_entry_only_config_schema("vbot_assist")

#async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    #hass.config_entries.async_register(DOMAIN, VBotAssistantConversationConfigFlow)
    #return True

#Thiết lập hội thoại
async def async_setup_entry(hass: HomeAssistant, entry: config_entries.ConfigEntry) -> bool:
    try:
        base_url = entry.data.get(VBot_URL_API)
        # Lấy giá trị của vbot_mode
        vbot_mode = entry.data.get(VBot_PROCESSING_MODE, "chatbot")
        if not base_url or not vbot_mode:
            raise ValueError("[VBot Assist] API không được cung cấp. Vui lòng nhập API")
        #Gắn base_url khi tạo agent
        agent = VBotAssistantConversationAgent(hass, entry, base_url, vbot_mode)
        conversation.async_set_agent(hass, entry, agent)
        hass.data.setdefault("vbot_assist", {})[entry.entry_id] = {
            "base_url": base_url,
            "agent": agent,
            "vbot_mode": vbot_mode,
        }
    except Exception as e:
        _LOGGER.error("[VBot Assist] Không thiết lập được mục nhập API URL: %s", e)
        raise ConfigEntryNotReady from e
    return True

async def async_unload_entry(hass: HomeAssistant, entry: config_entries.ConfigEntry) -> bool:
    conversation.async_unset_agent(hass, entry)
    hass.data["vbot_assist"].pop(entry.entry_id, None)
    return True

class VBotAssistantConversationAgent(conversation.AbstractConversationAgent):

    @property
    def supported_languages(self) -> list[str]:
        return VBot_LANGUAGES

    def __init__(self, hass: HomeAssistant, entry: config_entries.ConfigEntry, base_url: str, vbot_mode: str) -> None:
        self.hass = hass
        self.entry = entry
        self.base_url = base_url
        self.vbot_mode = vbot_mode

    #Xử lý dữ liệu và phản hồi
    async def async_process(self, user_input: conversation.ConversationInput) -> conversation.ConversationResult:
        try:
            if not user_input.text:
                raise ValueError("Không có đầu vào văn bản từ người dùng")

            response_text = await self.fetch_conversation_response(user_input.text)
            #_LOGGER.error(f"[VBot Assist] VBot Test Logs: {response_text}")

            if not response_text:
                response_text = "Xin lỗi, tôi không hiểu yêu cầu của bạn."

        except ValueError as e:
            _LOGGER.error(f"[VBot Assist] Đầu vào không hợp lệ: {str(e)}")
            response_text = "Đầu vào không hợp lệ. Vui lòng thử lại."

        except Exception as e:
            _LOGGER.error(f"[VBot Assist] Lỗi không mong đợi khi nhận diện ý định: {str(e)}")
            response_text = "Đã xảy ra lỗi không mong đợi. Vui lòng thử lại."

        #Trả về cho Assist
        intent_response = intent.IntentResponse(language=user_input.language)
        intent_response.async_set_speech(response_text)
        return conversation.ConversationResult(
            response=intent_response,
            conversation_id=user_input.conversation_id
        )

    async def fetch_conversation_response(self, user_input: str) -> str:
        url = f"{self.base_url}/"
        payload = {
            "type": 3,
            "data": "main_processing",
            "action": f"{self.vbot_mode}",
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
                        if data.get("success") and "message" in data:
                            return data["message"]
                        else:
                            _LOGGER.error(f"[VBot Assist] Lỗi định dạng phản hồi API: {data}")
                            return f"Không có dữ liệu phản hồi {data.get('message')}"
                    else:
                        _LOGGER.error(f"[VBot Assist] Không thể lấy phản hồi từ API: {await response.text()}")
                        return "Lỗi khi lấy phản hồi"
        except aiohttp.ClientError as e:
            _LOGGER.error(f"[VBot Assist] Yêu cầu API thất bại: {e}")
            return "Yêu cầu API thất bại"
        except Exception as e:
            _LOGGER.error(f"[VBot Assist] Lỗi không mong đợi khi gọi API: {e}")
            return "Lỗi không mong đợi khi gọi API"
            
