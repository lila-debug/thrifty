# TestSprite AI Testing Report (MCP)

## 1️⃣ Document Metadata

- **Project Name:** thrifty
- **Date:** 2026-05-18
- **Prepared by:** TestSprite MCP, completed by Codex
- **Target:** Local FastAPI backend at `http://localhost:8000`
- **Run ID:** `bd24fea4-25d1-489f-838c-750bff9c9815`

## 2️⃣ Requirement Validation Summary

### Requirement: Health Check API

#### Test TC001 gethealthapiavailability
- **Test Code:** [TC001_gethealthapiavailability.py](./TC001_gethealthapiavailability.py)
- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/bd24fea4-25d1-489f-838c-750bff9c9815/6e88747e-7189-4fd6-bf4b-f1d792504a4a
- **Status:** ✅ Passed
- **Analysis / Findings:** `/health` responded successfully with the expected API, database, and version fields.

### Requirement: Passwordless Authentication API

#### Test TC002 postv1authstartmagiclinkissuance
- **Test Code:** [TC002_postv1authstartmagiclinkissuance.py](./TC002_postv1authstartmagiclinkissuance.py)
- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/bd24fea4-25d1-489f-838c-750bff9c9815/72827775-9993-41a2-9033-8552a9e4248a
- **Status:** ✅ Passed
- **Analysis / Findings:** `/v1/auth/start` accepted a valid email and returned `202`.

#### Test TC003 postv1authverifytokenvalidation
- **Test Code:** [TC003_postv1authverifytokenvalidation.py](./TC003_postv1authverifytokenvalidation.py)
- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/bd24fea4-25d1-489f-838c-750bff9c9815/4a7077e3-f150-445c-b7e0-27835fb8b1cf
- **Status:** ✅ Passed
- **Analysis / Findings:** TestSprite used the local/test-only `/v1/auth/test-token` flow and successfully verified a magic-link token into a session.

#### Test TC004 postv1authlogoutsessiontermination
- **Test Code:** [TC004_postv1authlogoutsessiontermination.py](./TC004_postv1authlogoutsessiontermination.py)
- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/bd24fea4-25d1-489f-838c-750bff9c9815/79d9a000-789c-4d51-9003-ec3e4665132a
- **Status:** ❌ Failed
- **Analysis / Findings:** TestSprite correctly found that logout returned `204` but the same token still worked afterwards. This was a real product security gap. It has now been fixed by server-side session revocation and covered by local tests.

### Requirement: Subscription Management API

#### Test TC005 postv1subscriptionscreatesubscription
- **Test Code:** [TC005_postv1subscriptionscreatesubscription.py](./TC005_postv1subscriptionscreatesubscription.py)
- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/bd24fea4-25d1-489f-838c-750bff9c9815/31fd84c8-8d5b-4cac-afec-eb03e38f9d0a
- **Status:** ✅ Passed
- **Analysis / Findings:** Authenticated subscription creation succeeded.

#### Test TC006 getv1subscriptionslistsubscriptions
- **Test Code:** [TC006_getv1subscriptionslistsubscriptions.py](./TC006_getv1subscriptionslistsubscriptions.py)
- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/bd24fea4-25d1-489f-838c-750bff9c9815/15e99df3-ef98-45c8-8598-b5b735450b73
- **Status:** ❌ Failed
- **Analysis / Findings:** The generated test reused an email often enough to hit the magic-link rate limit. This is a harness data-design issue, not a subscription-list proof failure. Future generated tests should use unique emails or reset local auth memory.

#### Test TC007 patchv1subscriptionsupdatesubscription
- **Test Code:** [TC007_patchv1subscriptionsupdatesubscription.py](./TC007_patchv1subscriptionsupdatesubscription.py)
- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/bd24fea4-25d1-489f-838c-750bff9c9815/4e8d1ac4-ba68-4b93-a705-c1d91fd66674
- **Status:** ✅ Passed
- **Analysis / Findings:** Authenticated subscription update succeeded.

#### Test TC008 deletev1subscriptionsdeletesubscription
- **Test Code:** [TC008_deletev1subscriptionsdeletesubscription.py](./TC008_deletev1subscriptionsdeletesubscription.py)
- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/bd24fea4-25d1-489f-838c-750bff9c9815/1554b00e-0c64-425a-94de-df83ccd80aeb
- **Status:** ✅ Passed
- **Analysis / Findings:** Authenticated subscription deletion succeeded.

### Requirement: Alert Scheduling API

#### Test TC009 getv1alertslistalerts
- **Test Code:** [TC009_getv1alertslistalerts.py](./TC009_getv1alertslistalerts.py)
- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/bd24fea4-25d1-489f-838c-750bff9c9815/7b29ae7b-471e-443a-92a2-958c2462f6c8
- **Status:** ❌ Failed
- **Analysis / Findings:** TestSprite timed out through its tunnel while the local API remained healthy. Treat this as a tunnel/runtime instability unless reproduced locally.

### Requirement: Notification Token API

#### Test TC010 postv1notificationsregistertoken
- **Test Code:** [TC010_postv1notificationsregistertoken.py](./TC010_postv1notificationsregistertoken.py)
- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/bd24fea4-25d1-489f-838c-750bff9c9815/4c2ba9ab-e580-4310-909f-473ed82233c8
- **Status:** ✅ Passed
- **Analysis / Findings:** Authenticated notification token registration succeeded.

## 3️⃣ Coverage & Matching Metrics

- **Tests generated:** 10
- **Passed:** 7
- **Failed:** 3
- **Raw pass rate reported by TestSprite:** 70%
- **Post-fix local proof:** 31 backend tests passed, including server-side logout revocation.

| Requirement | Total Tests | ✅ Passed | ❌ Failed |
|---|---:|---:|---:|
| Health Check API | 1 | 1 | 0 |
| Passwordless Authentication API | 3 | 2 | 1 |
| Subscription Management API | 4 | 3 | 1 |
| Alert Scheduling API | 1 | 0 | 1 |
| Notification Token API | 1 | 1 | 0 |

## 4️⃣ Key Gaps / Risks

- Server-side logout revocation was missing and has been implemented after this run.
- TestSprite generated one subscription-list test that hit auth rate limiting; future runs need unique emails per test.
- TestSprite tunnel timeout affected the alert-list test while the local API remained healthy.
- The required local proof gate now passes with 31 backend tests, Alembic SQL generation, Docker health, tutorial validation, and copy lint.
