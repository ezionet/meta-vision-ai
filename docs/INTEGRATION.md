# Integration plan

1. Create private GitHub repository and import the official Meta `samples/CameraAccess` Xcode project, preserving upstream license notices.
2. Add `AnalysisClient.swift` and `AnalysisScreen.swift` to the Xcode target.
3. On photo capture, convert the SDK photo bytes to JPEG if needed; open AnalysisScreen with the captured data.
4. Host backend on a secured HTTPS service; add authenticated requests and rate limits before using outside localhost.
5. Configure the backend endpoint in the iOS app without storing the OpenAI API key on the phone.
6. Enable Meta Developer Mode on the iPhone companion app; verify device firmware and SDK registration.
7. Once Apple Developer enrollment is active, set signing team, bundle identifier and App Store Connect credentials.
8. Add a macOS GitHub Actions Xcode build with an appropriate Xcode version; configure signing privately; publish TestFlight only after a successful signed archive.
9. Test pairing, capture, image analysis and Bluetooth audio on the actual glasses.

Security: captured photos may include private infrastructure or personal information. Review images before upload; minimize retention; do not log image bodies.

Important: Meta's experimental standalone high-quality photo capture API may have release-channel restrictions; use the officially supported CameraAccess streaming-photo flow for the first prototype.
