import SwiftUI

struct SignInView: View {
    @Environment(AppSession.self) private var session
    @State private var email = "lila@example.com"

    var body: some View {
        VStack(spacing: 22) {
            VStack(alignment: .leading, spacing: 10) {
                Text("Thrifty")
                    .font(.system(size: 44, weight: .bold, design: .rounded))
                    .foregroundStyle(ThriftyTheme.ink)
                Text("Catch trials and renewals before they charge.")
                    .font(.title3)
                    .foregroundStyle(ThriftyTheme.muted)
            }
            .frame(maxWidth: 520, alignment: .leading)

            VStack(alignment: .leading, spacing: 16) {
                Text("Sign in")
                    .font(.headline)

                TextField("Email address", text: $email)
                    .textInputAutocapitalization(.never)
                    .keyboardType(.emailAddress)
                    .textFieldStyle(.roundedBorder)
                    .accessibilityIdentifier("email-field")

                Button {
                    Task { await session.signIn(email: email) }
                } label: {
                    HStack {
                        if session.isLoading {
                            ProgressView()
                        }
                        Text("Continue")
                            .fontWeight(.semibold)
                    }
                    .frame(maxWidth: .infinity)
                }
                .buttonStyle(.borderedProminent)
                .controlSize(.large)
                .disabled(session.isLoading || email.isEmpty)
                .accessibilityIdentifier("continue-button")

                Text("Continue with your email to start tracking upcoming charges.")
                    .font(.footnote)
                    .foregroundStyle(ThriftyTheme.muted)
            }
            .thriftyPanel()
            .frame(maxWidth: 520)

            if let errorMessage = session.errorMessage {
                Text(errorMessage)
                    .font(.footnote)
                    .foregroundStyle(.red)
                    .frame(maxWidth: 520, alignment: .leading)
            }
        }
        .padding(28)
        .frame(maxWidth: .infinity, maxHeight: .infinity)
        .background(ThriftyTheme.background)
    }
}
