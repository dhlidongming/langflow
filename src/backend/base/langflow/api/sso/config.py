from cas import CASClient

cas_client = CASClient(
    version=3,
    service_url='http://localhost:7860/callback',
    # server_url='https://sso.eos.dhgate.com/cas',
    # server_url='http://127.0.0.1:8000/cas/dhgate/application_python_example',
    server_url='http://172.21.80.24/cas',
)