#!/usr/bin/env python3
"""Integrate Meta Vision AI into a locally imported CameraAccess sample.

Run from repository root after copying the official sample to ios/MetaVisionAI.
This script is idempotent and aborts if the expected upstream source has changed.
"""
from pathlib import Path

root = Path(__file__).resolve().parents[1]
sample = root / "ios/MetaVisionAI/CameraAccess"
vm = sample / "ViewModels/CameraViewModel.swift"
view = sample / "Views/CameraView.swift"
assert vm.exists() and view.exists(), "Import official CameraAccess sample first"

def replace_once(path, old, new):
    source = path.read_text()
    if new in source:
        return
    if source.count(old) != 1:
        raise SystemExit(f"Unexpected upstream structure in {path}: {old[:70]!r}")
    path.write_text(source.replace(old, new, 1))

replace_once(vm,
    "  var activePreview: CapturePreview?\n",
    "  var activePreview: CapturePreview?\n  var capturedJPEGData: Data?\n")
replace_once(vm,
    "    if let image = UIImage(data: data.data) {\n      activePreview = .photo(image)\n    }",
    "    if let image = UIImage(data: data.data) {\n      capturedJPEGData = data.data\n      activePreview = .photo(image)\n    }")
replace_once(view,
    "  @State private var isLaunchingUpdate: Bool = false",
    "  @State private var isLaunchingUpdate: Bool = false\n  @State private var showAIAnalysis = false")
replace_once(view,
    "          onDismiss: { viewModel.dismissCapturePreview() }\n        )",
    """          onDismiss: { viewModel.dismissCapturePreview() }
        )
        .overlay(alignment: .bottom) {
          if viewModel.capturedJPEGData != nil {
            Button("Analizza con AI") { showAIAnalysis = true }
              .buttonStyle(.borderedProminent)
              .padding(.bottom, 32)
          }
        }""")
replace_once(view,
    "    .navigationBarHidden(true)",
    """    .sheet(isPresented: $showAIAnalysis) {
      if let jpeg = viewModel.capturedJPEGData {
        NavigationStack {
          AnalysisScreen(
            jpegData: jpeg,
            client: AnalysisClient(endpoint: URL(string: "https://REPLACE_WITH_YOUR_BACKEND.example")!)
          )
        }
      }
    }
    .navigationBarHidden(true)""")
for name in ("AnalysisClient.swift", "AnalysisScreen.swift"):
    dest = sample / name
    if not dest.exists():
        dest.write_bytes((root / "ios" / name).read_bytes())
print("Integration source files prepared. Add the two Swift files to the Xcode target if needed.")
print("Configure a real HTTPS backend URL before running. Do not publish an unauthenticated backend.")
