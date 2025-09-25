import hashlib, hmac, base64, json, requests
from datetime import datetime, timezone

BASE_URL = "https://www.soliscloud.com:13333"
SECRET_KEY = b'9585365aa561413eaf2f4e13286864bd'
KEY_ID = "1300386381676526360"

def call_api(canonical_resource, body):
    # Serialize body
    body_bytes = json.dumps(body, separators=(",", ":")).encode("utf-8")

    # Compute headers
    date_str = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT")
    content_md5 = base64.b64encode(hashlib.md5(body_bytes).digest()).decode()
    to_sign = f"POST\n{content_md5}\napplication/json\n{date_str}\n{canonical_resource}"
    sig = base64.b64encode(hmac.new(SECRET_KEY, to_sign.encode(), hashlib.sha1).digest()).decode()
    auth = f"API {KEY_ID}:{sig}"

    headers = {
        "Content-MD5": content_md5,
        "Content-Type": "application/json",
        "Date": date_str,
        "Authorization": auth,
    }

    url = BASE_URL + canonical_resource
    r = requests.post(url, data=body_bytes, headers=headers, timeout=10)
    print("Status:", r.status_code)
    print("Response:", r.text)

# Example: list your stations
call_api("/v1/api/userStationList", {"userId": KEY_ID})
