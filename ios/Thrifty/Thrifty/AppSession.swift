import Foundation
import Observation

@MainActor
@Observable
final class AppSession {
    private let apiClient: APIClient

    var user: AuthUser?
    var sessionToken: String?
    var subscriptions: [Subscription] = []
    var selectedSubscription: Subscription?
    var isLoading = false
    var errorMessage: String?
    private var handledLaunchArguments = false

    init(apiClient: APIClient) {
        self.apiClient = apiClient
    }

    var isSignedIn: Bool {
        sessionToken != nil
    }

    func signIn(email: String) async {
        await run {
            let response = try await apiClient.signIn(email: email)
            user = response.user
            sessionToken = response.sessionToken
            try await refreshSubscriptions()
        }
    }

    func refreshSubscriptions() async throws {
        guard let sessionToken else { throw APIError.missingSession }
        subscriptions = try await apiClient.subscriptions(sessionToken: sessionToken)
        if selectedSubscription == nil {
            selectedSubscription = subscriptions.first
        } else if let selectedSubscription {
            self.selectedSubscription = subscriptions.first { $0.id == selectedSubscription.id }
        }
    }

    func createSubscription(_ payload: SubscriptionCreate) async {
        await run {
            guard let sessionToken else { throw APIError.missingSession }
            let created = try await apiClient.createSubscription(
                sessionToken: sessionToken,
                payload: payload
            )
            try await refreshSubscriptions()
            selectedSubscription = created
        }
    }

    func logout() async {
        await run {
            if let sessionToken {
                try await apiClient.logout(sessionToken: sessionToken)
            }
            user = nil
            self.sessionToken = nil
            subscriptions = []
            selectedSubscription = nil
        }
    }

    func handleLaunchArguments(_ arguments: [String]) async {
        guard apiClient.usesLocalTestToken, !handledLaunchArguments else { return }
        handledLaunchArguments = true

        guard arguments.contains("--thrifty-debug-add-sample") else { return }
        let suffix = UUID().uuidString.prefix(8).lowercased()
        await addDebugSample(email: "lila+sim-\(suffix)@example.com")
    }

    func handleDebugURL(_ url: URL) async {
        guard apiClient.usesLocalTestToken else { return }
        guard url.scheme == "thrifty", url.host == "debug" else { return }

        let components = URLComponents(url: url, resolvingAgainstBaseURL: false)
        let query = Dictionary(
            uniqueKeysWithValues: (components?.queryItems ?? []).compactMap { item in
                item.value.map { (item.name, $0) }
            }
        )
        let email = query["email"] ?? "lila@example.com"

        switch url.path {
        case "/sign-in":
            await signIn(email: email)
        case "/add-sample":
            await addDebugSample(
                email: email,
                serviceName: query["service"] ?? "Canva Pro Trial",
                amount: query["amount"] ?? "14.99",
                currency: query["currency"] ?? "CAD",
                cadence: query["cadence"] ?? "monthly",
                kind: query["kind"] ?? "trial_conversion",
                notes: query["notes"] ?? "Simulator smoke test entry."
            )
        case "/refresh":
            await run {
                try await refreshSubscriptions()
            }
        default:
            return
        }
    }

    private func addDebugSample(
        email: String,
        serviceName: String = "Canva Pro Trial",
        amount: String = "14.99",
        currency: String = "CAD",
        cadence: String = "monthly",
        kind: String = "trial_conversion",
        notes: String = "Cancel before the trial converts."
    ) async {
        if !isSignedIn {
            await signIn(email: email)
        }
        guard isSignedIn else { return }
        await createSubscription(
            SubscriptionCreate(
                serviceName: serviceName,
                amount: Decimal(string: amount),
                currency: currency,
                cadence: cadence,
                nextEventAt: Date().addingTimeInterval(60 * 60 * 24 * 6),
                nextEventKind: kind,
                precision: "exact",
                notes: notes
            )
        )
    }

    private func run(_ action: () async throws -> Void) async {
        isLoading = true
        errorMessage = nil
        do {
            try await action()
        } catch {
            errorMessage = error.localizedDescription
        }
        isLoading = false
    }
}
