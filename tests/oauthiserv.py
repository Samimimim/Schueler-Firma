from flask import Flask, redirect, request, session
import secrets
import hashlib
import base64
import requests
from urllib.parse import urlencode

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

CLIENT_ID = "13_s1m6dzyg76s44gw08wk8ws8gggks4cgwg8c8wk04440000ssk"
CLIENT_SECRET = "1w3x8ba6rnfowsogo84g0wcoo0gwo08kkggkg444k0sc840c4s"

REDIRECT_URI = "http://localhost:5000/callback"

AUTH_ENDPOINT = "https://messelbergschule.de/iserv/auth/auth"
TOKEN_ENDPOINT = "https://messelbergschule.de/iserv/auth/public/token"
USERINFO_ENDPOINT = "https://messelbergschule.de/iserv/auth/userinfo"


def create_pkce():
    verifier = secrets.token_urlsafe(64)

    challenge = hashlib.sha256(
        verifier.encode()
    ).digest()

    challenge = base64.urlsafe_b64encode(
        challenge
    ).decode().rstrip("=")

    return verifier, challenge


@app.route("/")
def home():
    return '<a href="/login">Login mit IServ</a>'


@app.route("/login")
def login():

    state = secrets.token_urlsafe(32)

    verifier, challenge = create_pkce()

    session["state"] = state
    session["verifier"] = verifier

    params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": "openid profile email",
        "state": state,
        "code_challenge": challenge,
        "code_challenge_method": "S256"
    }

    return redirect(
        AUTH_ENDPOINT + "?" + urlencode(params)
    )


@app.route("/callback")
def callback():

    if request.args.get("state") != session["state"]:
        return "State ungültig", 400

    code = request.args.get("code")

    token_response = requests.post(
        TOKEN_ENDPOINT,
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "code_verifier": session["verifier"]
        }
    )

    token_response.raise_for_status()

    token_data = token_response.json()

    access_token = token_data["access_token"]

    user_response = requests.get(
        USERINFO_ENDPOINT,
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    user_response.raise_for_status()

    return user_response.json()


if __name__ == "__main__":
    app.run(debug=True)