import urllib.request
import json
import cv2
import numpy as np

# 1. Login
login_data = json.dumps({'email': 'demo@foodguard.com', 'password': 'Password1234!'}).encode('utf-8')
req = urllib.request.Request('http://127.0.0.1:8000/api/auth/login/', data=login_data, headers={'Content-Type': 'application/json'})
with urllib.request.urlopen(req) as resp:
    token = json.loads(resp.read().decode('utf-8'))['access']
print("1. Logged in successfully. Token length:", len(token))

# 2. Test Registration auto-activation
reg_data = json.dumps({'email': 'newuser123@foodguard.com', 'first_name': 'New', 'password': 'Password1234!'}).encode('utf-8')
req_reg = urllib.request.Request('http://127.0.0.1:8000/api/auth/register/', data=reg_data, headers={'Content-Type': 'application/json'})
try:
    with urllib.request.urlopen(req_reg) as resp_reg:
        reg_result = json.loads(resp_reg.read().decode('utf-8'))
        print("2. Register API returned 201 with access token:", 'access' in reg_result, "Message:", reg_result.get('message'))
except Exception as e:
    print("2. Register test:", e)

# 3. Test Freshness detection
img = np.full((250, 250, 3), (30, 200, 40), dtype=np.uint8)
_, img_encoded = cv2.imencode('.jpg', img)

boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
body = (
    f'--{boundary}\r\n'
    'Content-Disposition: form-data; name="image"; filename="fresh_apple.jpg"\r\n'
    'Content-Type: image/jpeg\r\n\r\n'
).encode('utf-8') + img_encoded.tobytes() + f'\r\n--{boundary}--\r\n'.encode('utf-8')

req_fresh = urllib.request.Request(
    'http://127.0.0.1:8000/api/inventory/freshness-detect/',
    data=body,
    headers={
        'Authorization': f'Bearer {token}',
        'Content-Type': f'multipart/form-data; boundary={boundary}'
    }
)
with urllib.request.urlopen(req_fresh) as resp_fresh:
    print("3. Freshness API Status:", resp_fresh.status)
    fresh_json = json.loads(resp_fresh.read().decode('utf-8'))
    print("3. Prediction:", fresh_json['status'], "Confidence:", fresh_json['confidence'], "%")
    print("   Metrics:", fresh_json['metrics'])

# 4. Test Analytics overview
req_analytics = urllib.request.Request(
    'http://127.0.0.1:8000/api/analytics/overview/',
    headers={'Authorization': f'Bearer {token}'}
)
with urllib.request.urlopen(req_analytics) as resp_analytics:
    print("4. Analytics API Status:", resp_analytics.status)
    analytics_json = json.loads(resp_analytics.read().decode('utf-8'))
    print("   Total Products:", analytics_json['stats']['total_products'])
    print("   Categories count:", len(analytics_json['categories']))
