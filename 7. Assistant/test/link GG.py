import os
import grpc
import requests
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.assistant.embedded.v1alpha2 import embedded_assistant_pb2, embedded_assistant_pb2_grpc

SCOPES = ['https://www.googleapis.com/auth/assistant-sdk-prototype']

# Tải và xác thực credentials
def get_credentials():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'test/client_secret_502829913174-ene1v2mhk2ctan96cascpngah4nkjnug.apps.googleusercontent.com.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

# Thiết lập gRPC với Google Assistant Service
def create_grpc_channel():
    credentials = grpc.ssl_channel_credentials()
    channel = grpc.secure_channel('embeddedassistant.googleapis.com', credentials)
    return channel

# Gửi yêu cầu đến Google Assistant
def send_assistant_request(text, credentials):
    channel = create_grpc_channel()
    assistant = embedded_assistant_pb2_grpc.EmbeddedAssistantStub(channel)

    # Cấu hình yêu cầu, thiết lập ngôn ngữ là tiếng Việt
    request = embedded_assistant_pb2.AssistRequest(
        config=embedded_assistant_pb2.AssistConfig(
            text_query=text,
            audio_out_config=embedded_assistant_pb2.AudioOutConfig(
                encoding=embedded_assistant_pb2.AudioOutConfig.LINEAR16,
                sample_rate_hertz=16000,
            ),
            dialog_state_in=embedded_assistant_pb2.DialogStateIn(
                language_code='vi-VN',  # Ngôn ngữ tiếng Việt
            ),
        )
    )

    # Gửi yêu cầu và xử lý phản hồi
    response = assistant.Assist(request, credentials=credentials)
    for resp in response:
        print(resp)

# Sử dụng Google Assistant với tiếng Việt
credentials = get_credentials()
send_assistant_request("Bây giờ là mấy giờ?", credentials)
