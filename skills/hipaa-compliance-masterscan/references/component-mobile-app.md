# Component - Mobile App (iOS / Android)

Applies to native and cross-platform apps that display, collect, or sync health data.
Mobile adds three surfaces a web review misses: **device storage**, **OS-level leaks**
(notifications, screenshots, clipboard, backups), and **SDKs** that run with full app
permissions.

## Device storage
- [ ] PHI stored only in encrypted, app-private storage: iOS Data Protection class `NSFileProtectionComplete` or `CompleteUnlessOpen`; Android EncryptedSharedPreferences / EncryptedFile or Keystore-backed keys for any database (SQLCipher or equivalent). [Block if PHI in plaintext files or unencrypted SQLite]
- [ ] Secrets and tokens in Keychain / Keystore, never in preferences, plist, or source. [Fix]
- [ ] **Backups**: PHI excluded from iCloud / Google backup (iOS `isExcludedFromBackup`, Android `allowBackup=false` or backup rules) **or** the backup path is documented as acceptable under the risk analysis. [Fix]
- [ ] Caches, temp files, and image caches holding PHI are cleared on logout and protected at rest. [Fix]
- [ ] Logout wipes local PHI; remote wipe or forced re-auth path exists for lost devices. [Fix]
- [ ] Device-level protection required: passcode or biometric, with an app-level lock for clinical apps. [Fix]

## OS-level leaks
- [ ] **Push notifications** never contain PHI in the visible payload (no diagnosis, medication, provider name, appointment reason). Use "You have a new message" plus in-app fetch. Push providers without a BAA see the whole payload. [Block if PHI in push via a non-BAA provider; Fix otherwise]
- [ ] **App switcher snapshot** is blurred or replaced when the app backgrounds. [Fix]
- [ ] **Screenshots and screen recording** blocked on PHI screens where the platform allows (Android `FLAG_SECURE`), or the risk documented. [Track]
- [ ] **Clipboard**: no automatic copy of PHI; sensitive fields not copyable where appropriate. [Track]
- [ ] **Keyboard**: third-party keyboards disabled on sensitive fields where feasible (iOS `secureTextEntry`, custom keyboard restrictions). [Track]
- [ ] **Siri / Spotlight / App Shortcuts / widgets** do not index or display PHI. [Fix]
- [ ] **Deep links / universal links** validate state and do not carry PHI in URL parameters. [Fix]
- [ ] **Crash reports** stripped of PHI (custom keys, breadcrumbs, screen names that reveal conditions). [Fix]

## SDKs and third parties
- [ ] Full **SDK inventory** (dependency lock file) reviewed: analytics, attribution, ads, crash, A/B testing, push, chat, session replay. Each one: what it collects, contract status, whether it can be disabled on PHI screens. [Block for ad or attribution SDKs with health signals; Fix otherwise]
- [ ] **Mobile attribution SDKs** (AppsFlyer, Adjust, Branch, Meta SDK, Firebase with ad features) receive device identifiers plus events. Health-revealing events (symptom logged, condition selected) must not be sent. [Block]
- [ ] Advertising identifier (IDFA / GAID) not collected unless there is a documented need; App Tracking Transparency prompt only if actually tracking. [Fix]
- [ ] Apple HealthKit and Google Health Connect data: used only for the stated purpose; **never for advertising or sold** (platform policy); not stored in iCloud via the app; HealthKit data not written to third parties. [Block on policy violation]

## Network
- [ ] TLS 1.2+; certificate validation not disabled in any build; certificate pinning considered for clinical apps. [Block if validation disabled in release]
- [ ] No PHI in URLs or query strings. [Fix]
- [ ] Offline mode: queued PHI encrypted at rest and purged after sync. [Fix]

## Authentication
- [ ] Biometric unlock is a **convenience layer** over a server-issued session, not a replacement for authentication. [Fix]
- [ ] Token refresh and revocation work; logout invalidates server-side. [Fix]
- [ ] Idle timeout and background timeout enforced. [Fix]

## Platform compliance (release blockers at the store level)
- [ ] **Apple App Privacy "nutrition label"** and **Google Play Data safety** section are accurate against the SDK inventory and backend behavior. Inaccurate labels are an FTC §5 risk and a store rejection risk. [Fix]
- [ ] **Google Play Health apps policy** declaration completed where the app handles health data. [Fix]
- [ ] Privacy policy URL live and matching behavior. [Fix]
- [ ] Account deletion available in-app (Apple and Google requirement) and actually deletes or anonymizes server data within the stated window, subject to record-retention duties. [Fix]
- [ ] Medical device claims in store listing consistent with the FDA determination. [Block if a cleared-device claim is made without clearance]

## Evidence to request
- Dependency manifest with each SDK's purpose and contract status.
- File-system dump of the app sandbox after login (jailbroken/rooted test device or emulator) showing storage protection.
- Sample push payloads.
- Store privacy label drafts.
- Network capture from a test session listing every host contacted.
