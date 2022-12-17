import os, requests

def token(request):
    if not "Authorization" in request.headers:
        return None, ("missing credentia;s", 401)

    token = request.headers["Authorization"]

    if not token:
        return None, ("Missing credentials", 401)

    response = requests.post(
        
    )