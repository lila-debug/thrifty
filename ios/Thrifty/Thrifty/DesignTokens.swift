import SwiftUI

enum ThriftyTheme {
    static let background = Color(red: 0.98, green: 0.98, blue: 0.96)
    static let panel = Color.white
    static let ink = Color(red: 0.10, green: 0.13, blue: 0.12)
    static let muted = Color(red: 0.42, green: 0.45, blue: 0.43)
    static let line = Color(red: 0.86, green: 0.88, blue: 0.84)
    static let action = Color(red: 0.00, green: 0.46, blue: 0.36)
    static let warning = Color(red: 0.77, green: 0.45, blue: 0.10)
}

extension View {
    func thriftyPanel() -> some View {
        padding(16)
            .background(ThriftyTheme.panel)
            .clipShape(RoundedRectangle(cornerRadius: 8, style: .continuous))
            .overlay(
                RoundedRectangle(cornerRadius: 8, style: .continuous)
                    .stroke(ThriftyTheme.line)
            )
    }
}
