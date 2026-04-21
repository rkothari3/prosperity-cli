# IMC Prosperity API Notes

## Attempted Discovery

Automated probing returned 404s for all standard endpoints:
- `/api/auth/login`, `/api/login`, `/api/user/login`
- `/api/auth/signin`, `/api/v1/login`
- `/auth/login`, `/login`

The site uses Next.js App Router (evidenced by `x-nextjs-prerender`, `Vary: rsc` headers).

## Requested: Manual API Capture

Please capture API calls using browser DevTools:

1. Go to https://prosperity.imc.com
2. Open DevTools (F12) → Network tab
3. Login with credentials:
   - Email: `rkothari40@gatech.edu`
   - Password: `Internships_123$`
4. After logging in, make a submission (if possible)
5. Right-click requests → "Copy as cURL"
6. Share the cURL commands

Key endpoints to find:
- Authentication (login) endpoint + request/response format
- Algorithm submission endpoint
- Status polling endpoint  
- Log download endpoint

## Expected Behavior

Once authenticated:
1. Upload `trader.py` or similar algorithm file
2. Poll for status until complete
3. Download result log
4. Open visualizer

## Placeholder Constants (until endpoints found)

```python
BASE_URL = "https://prosperity.imc.com"
AUTH_ENDPOINT = "/api/???"  # TBD
SUBMIT_ENDPOINT = "/api/???"  # TBD
STATUS_ENDPOINT = "/api/???"  # TBD
LOG_ENDPOINT = "/api/???"  # TBD
```