import Foundation

enum FlexibleDecoding {
    private static func iso8601() -> ISO8601DateFormatter {
        let formatter = ISO8601DateFormatter()
        formatter.formatOptions = [.withInternetDateTime]
        return formatter
    }

    private static func iso8601WithFractionalSeconds() -> ISO8601DateFormatter {
        let formatter = ISO8601DateFormatter()
        formatter.formatOptions = [.withInternetDateTime, .withFractionalSeconds]
        return formatter
    }

    private static func localTimestamp() -> DateFormatter {
        let formatter = DateFormatter()
        formatter.locale = Locale(identifier: "en_US_POSIX")
        formatter.timeZone = TimeZone(secondsFromGMT: 0)
        formatter.dateFormat = "yyyy-MM-dd'T'HH:mm:ss"
        return formatter
    }

    static func decodeDate(from decoder: Decoder) throws -> Date {
        let container = try decoder.singleValueContainer()
        let value = try container.decode(String.self)

        if let date = iso8601WithFractionalSeconds().date(from: value) {
            return date
        }
        if let date = iso8601().date(from: value) {
            return date
        }
        if let date = localTimestamp().date(from: value) {
            return date
        }

        throw DecodingError.dataCorruptedError(
            in: container,
            debugDescription: "Date string is not ISO-8601 compatible: \(value)"
        )
    }
}

struct AuthStartResponse: Decodable {
    let status: String
}

struct AuthTestTokenResponse: Decodable {
    let token: String
}

struct AuthVerifyResponse: Decodable {
    let sessionToken: String
    let user: AuthUser

    enum CodingKeys: String, CodingKey {
        case sessionToken = "session_token"
        case user
    }
}

struct AuthUser: Decodable, Identifiable {
    let id: String
    let email: String
    let tier: String
}

struct SubscriptionListResponse: Decodable {
    let subscriptions: [Subscription]
}

struct Subscription: Decodable, Identifiable, Hashable {
    let id: String
    let serviceName: String
    let source: String
    let sourceProductId: String?
    let amount: Decimal?
    let currency: String?
    let cadence: String?
    let status: String
    let trialEndsAt: Date?
    let nextEventAt: Date?
    let nextEventKind: String?
    let precision: String
    let cancelByAt: Date?
    let cancelUrl: String?
    let termsPlain: String?
    let notes: String?

    enum CodingKeys: String, CodingKey {
        case id
        case serviceName = "service_name"
        case source
        case sourceProductId = "source_product_id"
        case amount
        case currency
        case cadence
        case status
        case trialEndsAt = "trial_ends_at"
        case nextEventAt = "next_event_at"
        case nextEventKind = "next_event_kind"
        case precision
        case cancelByAt = "cancel_by_at"
        case cancelUrl = "cancel_url"
        case termsPlain = "terms_plain"
        case notes
    }

    init(from decoder: Decoder) throws {
        let container = try decoder.container(keyedBy: CodingKeys.self)

        id = try container.decode(String.self, forKey: .id)
        serviceName = try container.decode(String.self, forKey: .serviceName)
        source = try container.decode(String.self, forKey: .source)
        sourceProductId = try container.decodeIfPresent(String.self, forKey: .sourceProductId)
        amount = Self.decodeDecimalIfPresent(from: container, forKey: .amount)
        currency = try container.decodeIfPresent(String.self, forKey: .currency)
        cadence = try container.decodeIfPresent(String.self, forKey: .cadence)
        status = try container.decode(String.self, forKey: .status)
        trialEndsAt = try container.decodeIfPresent(Date.self, forKey: .trialEndsAt)
        nextEventAt = try container.decodeIfPresent(Date.self, forKey: .nextEventAt)
        nextEventKind = try container.decodeIfPresent(String.self, forKey: .nextEventKind)
        precision = try container.decode(String.self, forKey: .precision)
        cancelByAt = try container.decodeIfPresent(Date.self, forKey: .cancelByAt)
        cancelUrl = try container.decodeIfPresent(String.self, forKey: .cancelUrl)
        termsPlain = try container.decodeIfPresent(String.self, forKey: .termsPlain)
        notes = try container.decodeIfPresent(String.self, forKey: .notes)
    }

    private static func decodeDecimalIfPresent(
        from container: KeyedDecodingContainer<CodingKeys>,
        forKey key: CodingKeys
    ) -> Decimal? {
        if let value = try? container.decodeIfPresent(Decimal.self, forKey: key) {
            return value
        }
        if let value = try? container.decodeIfPresent(String.self, forKey: key) {
            return Decimal(string: value)
        }
        return nil
    }
}

struct SubscriptionCreate: Encodable {
    var serviceName: String
    var amount: Decimal?
    var currency: String?
    var cadence: String?
    var nextEventAt: Date?
    var nextEventKind: String?
    var precision: String?
    var notes: String?

    enum CodingKeys: String, CodingKey {
        case serviceName = "service_name"
        case amount
        case currency
        case cadence
        case nextEventAt = "next_event_at"
        case nextEventKind = "next_event_kind"
        case precision
        case notes
    }
}

extension Subscription {
    var displayAmount: String {
        guard let amount, let currency else { return "Amount unknown" }
        return "\(currency) \(amount)"
    }

    var eventLabel: String {
        switch nextEventKind {
        case "trial_conversion":
            return "Trial converts"
        case "renewal":
            return "Renews"
        default:
            return "Next charge"
        }
    }

    var urgencyLabel: String {
        guard let nextEventAt else { return "Date unknown" }
        let days = Calendar.current.dateComponents([.day], from: Date(), to: nextEventAt).day ?? 0
        if days < 0 { return "Past" }
        if days == 0 { return "Today" }
        if days == 1 { return "Tomorrow" }
        return "In \(days) days"
    }
}
