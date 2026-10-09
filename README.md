# Meta Vision AI — prototype v0.1

Personal iPhone assistant for Meta AI glasses. This is a **starter integration**, not yet an installable iOS application.

## Verified base

Meta's official CameraAccess sample supports pairing, device sessions, camera preview and photo capture:
https://github.com/facebook/meta-wearables-dat-ios/tree/main/samples/CameraAccess

Requirements per sample: iOS 17.2+, Xcode 26.4+, Swift 6.3+, Developer Mode enabled in Meta AI app.

## Components

- `backend/server.py`: OpenAI Responses API image analysis. API key stays server-side.
- `ios/AnalysisClient.swift`: iOS HTTPS client for the analysis endpoint.
- `ios/AnalysisScreen.swift`: SwiftUI analysis screen with Italian speech synthesis.
- `docs/INTEGRATION.md`: next integration and deployment steps.

## Local backend on Windows

```powershell
cd backend
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:OPENAI_API_KEY="YOUR_KEY"
uvicorn server:app --host 127.0.0.1 --port 8000
```

Do not expose the unauthenticated API to the public internet. Before deployment, add user authentication, request quotas, rate limiting and HTTPS. Never embed the OpenAI key in iOS code.

## Current limitations

- Swift files are prepared integration components, not a full Xcode project.
- The Meta sample's camera capture callback must be wired to `AnalysisScreen` using captured JPEG bytes.
- iOS build/signing and physical-glasses testing have **not** been executed.
- Voice wake-up without touching the phone is not claimed.
