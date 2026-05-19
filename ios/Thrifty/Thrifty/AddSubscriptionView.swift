import SwiftUI

struct AddSubscriptionView: View {
    @Environment(AppSession.self) private var session
    @Environment(\.dismiss) private var dismiss

    @State private var serviceName = ""
    @State private var amount = ""
    @State private var currency = "CAD"
    @State private var nextEventAt = Date().addingTimeInterval(60 * 60 * 24 * 7)
    @State private var hasKnownDate = true
    @State private var isTrial = true
    @State private var notes = ""

    var body: some View {
        NavigationStack {
            Form {
                Section("What might charge?") {
                    TextField("Service name", text: $serviceName)
                        .accessibilityIdentifier("service-name-field")
                    TextField("Amount", text: $amount)
                        .keyboardType(.decimalPad)
                    TextField("Currency", text: $currency)
                        .textInputAutocapitalization(.characters)
                }

                Section("When should Thrifty warn you?") {
                    Toggle("I know the date", isOn: $hasKnownDate)
                    if hasKnownDate {
                        DatePicker("Next event", selection: $nextEventAt, displayedComponents: [.date, .hourAndMinute])
                    }
                    Picker("Event type", selection: $isTrial) {
                        Text("Trial conversion").tag(true)
                        Text("Renewal").tag(false)
                    }
                }

                Section("Notes") {
                    TextField("Cancellation steps, account owner, anything useful", text: $notes, axis: .vertical)
                        .lineLimit(3, reservesSpace: true)
                }
            }
            .navigationTitle("Add subscription")
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Cancel") {
                        dismiss()
                    }
                }
                ToolbarItem(placement: .confirmationAction) {
                    Button("Save") {
                        Task {
                            await session.createSubscription(payload)
                            if session.errorMessage == nil {
                                dismiss()
                            }
                        }
                    }
                    .disabled(serviceName.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty || session.isLoading)
                    .accessibilityIdentifier("save-subscription-button")
                }
            }
        }
    }

    private var payload: SubscriptionCreate {
        SubscriptionCreate(
            serviceName: serviceName.trimmingCharacters(in: .whitespacesAndNewlines),
            amount: Decimal(string: amount.trimmingCharacters(in: .whitespacesAndNewlines)),
            currency: currency.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty ? nil : currency.uppercased(),
            cadence: nil,
            nextEventAt: hasKnownDate ? nextEventAt : nil,
            nextEventKind: isTrial ? "trial_conversion" : "renewal",
            precision: hasKnownDate ? "exact" : "unknown",
            notes: notes.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty ? nil : notes
        )
    }
}
