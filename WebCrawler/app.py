from api.request_handler import make_request

html_code: str = make_request('https://www.businessinsider.com/microsoft-doubles-down-quantum-computing-latest-reorg-2024-6')
print(html_code)
