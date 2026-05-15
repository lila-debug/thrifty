export const copy = {
  signIn: {
    title: "Sign in to Thrifty",
    subtitle: "We will send a secure link to your inbox. No secret phrase required, ever.",
    emailLabel: "Email address",
    emailPlaceholder: "you@example.com",
    submit: "Send me a link",
    sent: "Right, that is away to you. Check your inbox.",
    sentSubtitle: "The link expires in 15 minutes.",
    error: {
      invalidEmail: "That does not look like a valid email address.",
      rateLimited: "You have requested a few links already. Try again in an hour.",
      generic: "Something went sideways. Try again in a moment.",
    },
  },
  list: {
    title: "Charges incoming",
    empty: {
      title: "Nothing on the horizon.",
      subtitle: "Add a subscription or trial to intercept charges before they happen.",
      cta: "Add a subscription",
    },
    headerSubtitle: "Cancel before money leaves.",
    pullToRefresh: "Pull to refresh",
    add: "Add",
  },
  add: {
    title: "Add a subscription",
    editTitle: "Edit subscription",
    fields: {
      serviceName: "Service name",
      serviceNamePlaceholder: "e.g. Netflix, Spotify, Disney+",
      amount: "Amount",
      currency: "Currency",
      cadence: "How often",
      nextEvent: "Next charge or trial end",
      kind: "What happens next",
      notes: "Notes",
    },
    options: {
      weekly: "Weekly",
      monthly: "Monthly",
      quarterly: "Every three months",
      semi_annual: "Every six months",
      annual: "Yearly",
      custom: "Custom",
      renewal: "It renews",
      trial_conversion: "Trial becomes paid",
      unknown: "I am not sure",
    },
    submit: "Save",
    cancel: "Cancel",
    validation: {
      serviceNameRequired: "Service name is required.",
      amountInvalid: "Amount must be a positive number.",
    },
  },
  detail: {
    title: "Subscription detail",
    edit: "Edit",
    remove: "Remove",
  },
  unknown: {
    badge: "unknown",
    reasons: {
      amount: "The provider did not share the amount.",
      nextEvent: "We do not know when the next charge happens.",
      cancelBy: "We do not know the exact cancellation deadline.",
      terms: "The provider did not share readable terms.",
    },
  },
  alerts: {
    leadLabels: {
      sevenDays: "in 7 days",
      threeDays: "in 3 days",
      oneDay: "tomorrow",
      twoHours: "in 2 hours",
    },
    push: {
      renewal: (service: string, when: string, amount: string) =>
        `${service} renews ${when}. ${amount} will be charged. Cancel now if you do not want it.`,
      trialConversion: (service: string, when: string, amount: string) =>
        `${service} trial ends ${when}. You will be charged ${amount} unless you cancel before then.`,
      renewalUnknownAmount: (service: string, when: string) =>
        `${service} renews ${when}. The amount is unknown. Check before it charges.`,
      trialConversionUnknownAmount: (service: string, when: string) =>
        `${service} trial ends ${when}. The amount is unknown. Check before then.`,
    },
  },
  terms: {
    templates: {
      monthlyRenewal: (amount: string, day: string) =>
        `Renews monthly at ${amount} on the ${day} of every month. Cancel before then to avoid the charge.`,
      annualRenewal: (amount: string, date: string) =>
        `Renews once a year on ${date} at ${amount}. Cancel before then to avoid being charged.`,
      trialThenMonthly: (trialEnd: string, amount: string) =>
        `Free until ${trialEnd}. After that it becomes monthly at ${amount}. Cancel before ${trialEnd} to avoid the charge.`,
      trialThenAnnual: (trialEnd: string, amount: string) =>
        `Free until ${trialEnd}. After that it becomes yearly at ${amount}. Cancel before ${trialEnd} to avoid the charge.`,
      unknown: "We could not read the terms. Check with the provider before the next event.",
    },
  },
  errors: {
    network: "No connection. Check your internet and try again.",
    server: "Something is not right on our end. Try again shortly.",
    notFound: "We cannot find that.",
    forbidden: "That does not belong to you.",
    unauthorised: "You will need to sign in again.",
  },
  permissions: {
    notifications: {
      title: "Let Thrifty warn you in time.",
      body: "We need permission to send notifications. Without them, alerts may be delayed.",
      grant: "Allow notifications",
      decline: "Not now",
    },
  },
  legal: {
    footer:
      "Based on true events. Sadly.\nCanadian Kind, Scottish Strong.\n© 2024–2026 Lila Olufemi Abegunrin · Thrifty™ · Trademarks and Patents Pending (CIPO) · REVOLUTIONISING LIFE SINCE 1982™",
  },
} as const;

export type Copy = typeof copy;
