import SwiftUI

struct UpcomingChargesView: View {
    let subscriptions: [Subscription]
    @Binding var selectedSubscription: Subscription?

    var sortedSubscriptions: [Subscription] {
        subscriptions.sorted {
            switch ($0.nextEventAt, $1.nextEventAt) {
            case let (left?, right?):
                return left < right
            case (_?, nil):
                return true
            case (nil, _?):
                return false
            case (nil, nil):
                return $0.serviceName < $1.serviceName
            }
        }
    }

    var body: some View {
        List(selection: $selectedSubscription) {
            Section {
                if sortedSubscriptions.isEmpty {
                    VStack(alignment: .leading, spacing: 8) {
                        Text("Nothing tracked yet")
                            .font(.headline)
                        Text("Add free trials and subscriptions as soon as you start them.")
                            .foregroundStyle(ThriftyTheme.muted)
                    }
                    .padding(.vertical, 8)
                } else {
                    ForEach(sortedSubscriptions) { subscription in
                        SubscriptionRow(
                            subscription: subscription,
                            isSelected: selectedSubscription?.id == subscription.id
                        )
                            .tag(subscription)
                    }
                }
            } header: {
                Text("Charges coming up")
            } footer: {
                Text("Thrifty is built around future events, not receipts after the damage is done.")
            }
        }
        .listStyle(.insetGrouped)
        .background(ThriftyTheme.background)
        .refreshable {
        }
    }
}

struct SubscriptionRow: View {
    let subscription: Subscription
    let isSelected: Bool

    var body: some View {
        HStack(alignment: .firstTextBaseline, spacing: 12) {
            VStack(alignment: .leading, spacing: 4) {
                Text(subscription.serviceName)
                    .font(.headline)
                    .foregroundStyle(isSelected ? .white : ThriftyTheme.ink)
                Text("\(subscription.eventLabel) · \(subscription.displayAmount)")
                    .font(.subheadline)
                    .foregroundStyle(isSelected ? .white.opacity(0.82) : ThriftyTheme.muted)
            }

            Spacer()

            Text(subscription.urgencyLabel)
                .font(.caption.weight(.semibold))
                .foregroundStyle(subscription.nextEventAt == nil ? ThriftyTheme.muted : ThriftyTheme.warning)
                .padding(.horizontal, 10)
                .padding(.vertical, 6)
                .background(isSelected ? .white.opacity(0.95) : ThriftyTheme.background)
                .clipShape(Capsule())
        }
        .padding(.vertical, 6)
        .accessibilityElement(children: .combine)
    }
}
