## Cài Đặt
1. Cài đặt bằng cách đăng ký làm kho lưu trữ tùy chỉnh của HACS hoặc bằng cách sao chép thư mục `vbot_assist` vào trong thư mục `custom_comComponents` của bạn
2. Khởi động lại Home Assistant
3. Đi tới: Settings > Devices & Services (Đi tới: Cài đặt > Thiết bị & Dịch vụ)
4. In the bottom right corner, select the Add Integration button (Ở góc dưới cùng bên phải, chọn nút Thêm tích hợp.)
5. Follow the instructions on screen to complete the setup (API Key is required).
    - [Generating an API Key](https://www.home-assistant.io/integrations/openai_conversation/#generate-an-api-key)
    - Specify "Base Url" if using OpenAI compatible servers like Azure OpenAI (also with APIM), LocalAI, otherwise leave as it is.
6. Go to Settings > [Voice Assistants](https://my.home-assistant.io/redirect/voice_assistants/).
7. Click to edit Assistant (named "Home Assistant" by default).
8. Select "Extended OpenAI Conversation" from "Conversation agent" tab.
