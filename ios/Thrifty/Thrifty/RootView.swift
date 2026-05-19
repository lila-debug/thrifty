import SwiftUI

struct RootView: View {
    @Environment(AppSession.self) private var session

    var body: some View {
        Group {
            if session.isSignedIn {
                MainShellView()
            } else {
                SignInView()
            }
        }
        .tint(ThriftyTheme.action)
    }
}

struct MainShellView: View {
    @Environment(AppSession.self) private var session
    @State private var sheet: ActiveSheet?

    var body: some View {
        @Bindable var session = session

        NavigationSplitView {
            UpcomingChargesView(
                subscriptions: session.subscriptions,
                selectedSubscription: $session.selectedSubscription
            )
            .navigationTitle("Upcoming")
            .toolbar {
                ToolbarItem(placement: .topBarLeading) {
                    Button {
                        Task { await session.logout() }
                    } label: {
                        Label("Sign out", systemImage: "rectangle.portrait.and.arrow.right")
                    }
                    .accessibilityIdentifier("sign-out-button")
                }

                ToolbarItem(placement: .topBarTrailing) {
                    Button {
                        sheet = .addSubscription
                    } label: {
                        Label("Add", systemImage: "plus")
                    }
                    .accessibilityIdentifier("add-subscription-button")
                }
            }
        } detail: {
            if let selectedSubscription = session.selectedSubscription {
                SubscriptionDetailView(subscription: selectedSubscription)
            } else {
                EmptyStateView()
            }
        }
        .sheet(item: $sheet) { destination in
            switch destination {
            case .addSubscription:
                AddSubscriptionView()
            }
        }
        .task {
            do {
                try await session.refreshSubscriptions()
            } catch {
                session.errorMessage = error.localizedDescription
            }
        }
    }
}

enum ActiveSheet: Identifiable {
    case addSubscription

    var id: String {
        "addSubscription"
    }
}

struct EmptyStateView: View {
    var body: some View {
        VStack(spacing: 14) {
            Image(systemName: "bell.badge")
                .font(.system(size: 44))
                .foregroundStyle(ThriftyTheme.action)
            Text("No upcoming charge selected")
                .font(.title2.bold())
            Text("Add a trial or subscription so Thrifty can warn you before the money leaves.")
                .multilineTextAlignment(.center)
                .foregroundStyle(ThriftyTheme.muted)
                .frame(maxWidth: 360)
        }
        .padding()
        .frame(maxWidth: .infinity, maxHeight: .infinity)
        .background(ThriftyTheme.background)
    }
}
