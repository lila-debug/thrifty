import SwiftUI

struct SubscriptionDetailView: View {
    let subscription: Subscription

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 18) {
                VStack(alignment: .leading, spacing: 8) {
                    Text(subscription.serviceName)
                        .font(.largeTitle.bold())
                    Text(subscription.eventLabel)
                        .font(.title3)
                        .foregroundStyle(ThriftyTheme.muted)
                }

                LazyVGrid(columns: [GridItem(.adaptive(minimum: 220), spacing: 12)], spacing: 12) {
                    DetailMetric(title: "Amount", value: subscription.displayAmount)
                    DetailMetric(title: "When", value: formattedDate(subscription.nextEventAt))
                    DetailMetric(title: "Cancel by", value: formattedDate(subscription.cancelByAt))
                    DetailMetric(title: "Certainty", value: subscription.precision.capitalized)
                }

                if let termsEnglish = subscription.termsEnglish, !termsEnglish.isEmpty {
                    DetailBlock(title: "English terms", bodyText: termsEnglish)
                }

                if let notes = subscription.notes, !notes.isEmpty {
                    DetailBlock(title: "Notes", bodyText: notes)
                }

                DetailBlock(
                    title: "Unknowns",
                    bodyText: unknownText
                )
            }
            .padding(24)
            .frame(maxWidth: 860, alignment: .leading)
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity, alignment: .topLeading)
        .background(ThriftyTheme.background)
        .navigationTitle(subscription.serviceName)
    }

    private var unknownText: String {
        var missing: [String] = []
        if subscription.amount == nil { missing.append("amount") }
        if subscription.nextEventAt == nil { missing.append("next charge date") }
        if subscription.cancelByAt == nil { missing.append("cancel-by deadline") }
        if missing.isEmpty { return "No major unknowns recorded for this subscription." }
        return "Still unknown: \(missing.joined(separator: ", ")). Thrifty will not invent these values."
    }

    private func formattedDate(_ date: Date?) -> String {
        guard let date else { return "Unknown" }
        return date.formatted(date: .abbreviated, time: .shortened)
    }
}

struct DetailMetric: View {
    let title: String
    let value: String

    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text(title)
                .font(.caption.weight(.semibold))
                .textCase(.uppercase)
                .foregroundStyle(ThriftyTheme.muted)
            Text(value)
                .font(.title3.weight(.semibold))
                .foregroundStyle(ThriftyTheme.ink)
        }
        .frame(maxWidth: .infinity, alignment: .leading)
        .thriftyPanel()
    }
}

struct DetailBlock: View {
    let title: String
    let bodyText: String

    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text(title)
                .font(.headline)
            Text(bodyText)
                .foregroundStyle(ThriftyTheme.muted)
        }
        .frame(maxWidth: .infinity, alignment: .leading)
        .thriftyPanel()
    }
}
