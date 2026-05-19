import Foundation

enum APIError: LocalizedError {
    case badURL
    case badStatus(Int, String)
    case missingSession

    var errorDescription: String? {
        switch self {
        case .badURL:
            return "The API address is invalid."
        case .badStatus(let status, let body):
            return "The API returned \(status). \(body)"
        case .missingSession:
            return "Sign in again."
        }
    }
}

struct APIClient {
    var baseURL: URL
    var usesLocalTestToken: Bool

    static let localDevelopment = APIClient(
        baseURL: URL(string: "http://127.0.0.1:8000")!,
        usesLocalTestToken: true
    )

    private var decoder: JSONDecoder {
        let decoder = JSONDecoder()
        decoder.dateDecodingStrategy = .custom(FlexibleDecoding.decodeDate)
        return decoder
    }

    private var encoder: JSONEncoder {
        let encoder = JSONEncoder()
        encoder.dateEncodingStrategy = .iso8601
        return encoder
    }

    func signIn(email: String) async throws -> AuthVerifyResponse {
        _ = try await post(path: "/v1/auth/start", body: ["email": email], response: AuthStartResponse.self)
        let token: String
        if usesLocalTestToken {
            let response = try await post(
                path: "/v1/auth/test-token",
                body: ["email": email],
                response: AuthTestTokenResponse.self
            )
            token = response.token
        } else {
            throw APIError.missingSession
        }
        return try await post(path: "/v1/auth/verify", body: ["token": token], response: AuthVerifyResponse.self)
    }

    func logout(sessionToken: String) async throws {
        var request = try request(path: "/v1/auth/logout", method: "POST", sessionToken: sessionToken)
        request.httpBody = Data()
        _ = try await send(request: request, response: EmptyResponse.self)
    }

    func subscriptions(sessionToken: String) async throws -> [Subscription] {
        let response = try await get(
            path: "/v1/subscriptions",
            sessionToken: sessionToken,
            response: SubscriptionListResponse.self
        )
        return response.subscriptions
    }

    func createSubscription(
        sessionToken: String,
        payload: SubscriptionCreate
    ) async throws -> Subscription {
        try await post(
            path: "/v1/subscriptions",
            body: payload,
            sessionToken: sessionToken,
            response: Subscription.self
        )
    }

    private func get<T: Decodable>(
        path: String,
        sessionToken: String,
        response: T.Type
    ) async throws -> T {
        let request = try request(path: path, method: "GET", sessionToken: sessionToken)
        return try await send(request: request, response: response)
    }

    private func post<Body: Encodable, T: Decodable>(
        path: String,
        body: Body,
        sessionToken: String? = nil,
        response: T.Type
    ) async throws -> T {
        var request = try request(path: path, method: "POST", sessionToken: sessionToken)
        request.httpBody = try encoder.encode(body)
        return try await send(request: request, response: response)
    }

    private func request(
        path: String,
        method: String,
        sessionToken: String?
    ) throws -> URLRequest {
        guard let url = URL(string: path, relativeTo: baseURL) else { throw APIError.badURL }
        var request = URLRequest(url: url)
        request.httpMethod = method
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        if let sessionToken {
            request.setValue("Bearer \(sessionToken)", forHTTPHeaderField: "Authorization")
        }
        return request
    }

    private func send<T: Decodable>(request: URLRequest, response: T.Type) async throws -> T {
        let (data, urlResponse) = try await URLSession.shared.data(for: request)
        guard let httpResponse = urlResponse as? HTTPURLResponse else {
            throw APIError.badStatus(-1, "No HTTP response.")
        }
        guard (200..<300).contains(httpResponse.statusCode) else {
            throw APIError.badStatus(httpResponse.statusCode, String(data: data, encoding: .utf8) ?? "")
        }
        if response == EmptyResponse.self {
            return EmptyResponse() as! T
        }
        return try decoder.decode(T.self, from: data)
    }
}

struct EmptyResponse: Decodable {}
