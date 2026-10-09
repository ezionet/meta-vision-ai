import SwiftUI
import AVFoundation

// Prototype integration screen: wire captured JPEG data from Meta CameraAccess sample.
struct AnalysisScreen: View {
    let jpegData: Data
    let client: AnalysisClient
    @State private var question = "Che cosa vedi? Indicami una diagnosi tecnica."
    @State private var answer = ""
    @State private var busy = false
    private let synthesizer = AVSpeechSynthesizer()

    var body: some View {
        VStack(spacing: 18) {
            TextField("Domanda", text: $question)
                .textFieldStyle(.roundedBorder)
            Button(busy ? "Analisi in corso" : "Analizza fotografia") {
                Task {
                    busy = true
                    defer { busy = false }
                    do {
                        answer = try await client.analyze(jpegData: jpegData, question: question)
                        let utterance = AVSpeechUtterance(string: answer)
                        utterance.voice = AVSpeechSynthesisVoice(language: "it-IT")
                        synthesizer.speak(utterance)
                    } catch { answer = "Errore: \(error.localizedDescription)" }
                }
            }.disabled(busy)
            ScrollView { Text(answer).frame(maxWidth: .infinity, alignment: .leading) }
        }.padding().navigationTitle("Meta Vision AI")
    }
}
