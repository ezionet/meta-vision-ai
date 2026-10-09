import Foundation

struct AnalysisResult: Decodable { let answer: String }

struct AnalysisClient {
    let endpoint: URL
    func analyze(jpegData: Data, question: String) async throws -> String {
        var request = URLRequest(url: endpoint.appendingPathComponent("analyze"))
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.timeoutInterval = 60
        request.httpBody = try JSONSerialization.data(withJSONObject: [
            "image_base64": jpegData.base64EncodedString(), "question": question
        ])
        let (data, response) = try await URLSession.shared.data(for: request)
        guard let http = response as? HTTPURLResponse, (200...299).contains(http.statusCode) else {
            throw URLError(.badServerResponse)
        }
        return try JSONDecoder().decode(AnalysisResult.self, from: data).answer
    }
}
