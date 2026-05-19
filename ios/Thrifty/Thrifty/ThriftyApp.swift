import SwiftUI

@main
struct ThriftyApp: App {
    @State private var session = AppSession(apiClient: .localDevelopment)

    var body: some Scene {
        WindowGroup {
            RootView()
                .environment(session)
                .task {
                    await session.handleLaunchArguments(ProcessInfo.processInfo.arguments)
                }
                .onOpenURL { url in
                    Task { await session.handleDebugURL(url) }
                }
        }
    }
}
