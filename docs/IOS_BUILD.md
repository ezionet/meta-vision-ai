# iOS build status
The CameraAccess sample was imported locally into ios/MetaVisionAI but is not yet committed to GitHub. GitHub Actions cannot compile local-only files.

1. Confirm Meta sample license and retain attribution.
2. Commit ios/MetaVisionAI/ on the feature branch (avoid credentials, local user data, and .claude settings).
3. The workflow uses Ruby xcodeproj to register AnalysisClient.swift and AnalysisScreen.swift in the app target.
4. Verify the macOS runner has a compatible Xcode version. Select a runner/Xcode version matching the upstream sample requirements if necessary.
5. Review any compiler errors and resolve before signing.
6. The backend URL in CameraView.swift is a placeholder. Replace with a secure authenticated HTTPS endpoint before device testing.
7. No signing or TestFlight publishing is configured.

This is a build candidate, not a verified successful iOS build.
