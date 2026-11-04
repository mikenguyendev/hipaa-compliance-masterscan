# Component - Web Frontend

Applies to any browser-delivered surface that displays, collects, or infers health
data: patient portals, telehealth UIs, intake forms, symptom quizzes, appointment
booking, and marketing pages with health-related forms.

## Tracking technologies - the highest-enforcement area
- [ ] **No advertising or attribution pixels on authenticated pages** (Meta Pixel, Google Ads tags, TikTok, LinkedIn Insight, and similar). HHS treats identifiers sent from authenticated pages as PHI disclosures; the FTC treats them as unauthorized disclosures for non-HIPAA apps. [Block]
- [ ] **Unauthenticated health pages** (condition pages, provider search, symptom checkers, appointment scheduling): no ad-tech that receives page URL plus a persistent identifier **unless** reviewed and documented by counsel. Court decisions have narrowed HHS's position on IP addresses alone; treat anything beyond IP as high risk. [Fix, Block if the page reveals a condition or treatment interest]
- [ ] **Analytics** (GA4, Mixpanel, Amplitude, PostHog, and similar) on PHI pages only under a BAA **or** configured so no identifiers or health-revealing URLs/events are sent. Self-hosted or BAA-covered analytics is the safe path. [Fix]
- [ ] **Session replay and heatmaps** (Hotjar, FullStory, LogRocket, Microsoft Clarity): off on any page with health data, or under BAA with field masking verified. [Block without BAA]
- [ ] **Chat widgets, support widgets, and embedded forms** from third parties: contract status checked; they see everything typed. [Fix]
- [ ] **Tag managers**: anyone with GTM access can add a pixel after review. Access restricted, container versions reviewed, change log kept. [Fix]
- [ ] A **runtime check** exists (CSP connect-src allowlist or a periodic crawler) so new trackers cannot appear silently. [Track]

## Browser storage and caching
- [ ] **No PHI in localStorage, sessionStorage, IndexedDB, or cookies** beyond an opaque session token. [Fix]
- [ ] `Cache-Control: no-store` on responses carrying PHI; no PHI in service-worker caches. [Fix]
- [ ] Autocomplete disabled on sensitive fields; no PHI prefilled into shared-device scenarios. [Track]
- [ ] Browser back-button and bfcache do not expose a prior user's PHI after logout. [Fix]

## Session and screen
- [ ] **Automatic logoff** after inactivity, with a warning; shorter for shared clinical workstations. (§164.312(a)(2)(iii)) [Fix]
- [ ] Logout clears all client state and invalidates the server session. [Fix]
- [ ] Masking of sensitive fields by default where the context is public-facing (kiosk, waiting-room display). [Track]

## Transport and platform security
- [ ] HTTPS everywhere, HSTS, no mixed content. [Block if PHI over HTTP]
- [ ] **Content Security Policy** with explicit `connect-src`, `script-src`, and `frame-src` allowlists; this doubles as the tracker control. [Fix]
- [ ] Third-party scripts pinned with Subresource Integrity where possible. [Track]
- [ ] No PHI in page titles, URLs, referrer headers, or `document.title` (which leak to analytics and browser history). `Referrer-Policy: no-referrer` or `strict-origin` set. [Fix]
- [ ] XSS protection: framework escaping used; any `dangerouslySetInnerHTML` / `innerHTML` with user content reviewed. [Block if demonstrable XSS on a PHI page]
- [ ] Embedded in iframes only where intended (`frame-ancestors`). [Track]

## Forms and consent UX
- [ ] Health-related forms state who receives the data and link to the privacy notice; consent is **affirmative, specific, and separate** where state consumer health data laws require it. [Fix]
- [ ] No pre-checked boxes for data sharing; no dark patterns in decline paths (FTC). [Fix]
- [ ] Consent and NPP acknowledgment are recorded with timestamp and version. [Fix]
- [ ] Minors: age gating and parental consent flow where COPPA or state law applies. [Fix]

## Accessibility (often a customer gate)
- [ ] WCAG 2.1 AA for patient-facing surfaces; required for Section 1557-covered entities and most public-sector contracts. [Track, Fix if contractually required]

## Evidence to request
- Network capture (HAR) of an authenticated session and of key unauthenticated health pages, listing every third-party host.
- Tag manager container export.
- CSP header as served.
- Logout and idle-timeout behavior demonstrated.
- Privacy notice and consent screens as rendered.
