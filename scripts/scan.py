#!/usr/bin/env python3
"""
Heuristic triage scanner for health-software release reviews.

Finds LEADS, not conclusions. Every hit must be checked against the relevant
component checklist. A clean run clears nothing.

Usage:
    python3 -I scan.py <path-to-repo> [--json] [--max-hits N]

Categories reported:
    tracker      advertising / analytics / session-replay SDKs and tags
    llm          hosted model SDKs and endpoints
    storage      browser or device storage that may hold health data
    url-phi      health-looking identifiers in URL/query construction
    secret       hardcoded credential patterns
    logging      logging calls that may carry patient data
    mobile       mobile-specific leak surfaces (push payloads, backups, FLAG_SECURE)
    crypto       disabled TLS verification or weak crypto
"""
import argparse
import json
import os
import re
import sys

SKIP_DIRS = {
    ".git", "node_modules", "vendor", "dist", "build", ".next", ".nuxt", "target",
    "Pods", "DerivedData", ".gradle", "__pycache__", ".venv", "venv", "coverage",
}
TEXT_EXT = {
    ".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".vue", ".svelte", ".html", ".htm",
    ".py", ".rb", ".go", ".java", ".kt", ".kts", ".swift", ".m", ".mm", ".cs", ".php",
    ".rs", ".scala", ".dart", ".json", ".yml", ".yaml", ".toml", ".xml", ".plist",
    ".gradle", ".env", ".tf", ".hcl", ".sh", ".cfg", ".ini", ".properties", ".md",
    ".txt", ".lock", ".pbxproj",
}
MAX_FILE_BYTES = 2_000_000

# (category, label, regex, hint)
PATTERNS = [
    # Trackers / ad-tech / analytics / session replay
    ("tracker", "Meta Pixel", r"fbq\(|connect\.facebook\.net|FacebookSDK|facebook-android-sdk|FBSDK", "web-frontend / mobile: ad pixel"),
    ("tracker", "Google Ads / gtag", r"googletagmanager\.com/gtag|gtag\(\s*['\"]config['\"]|AW-\d{6,}|googleads\.g\.doubleclick", "web-frontend: ads tag"),
    ("tracker", "Google Tag Manager", r"googletagmanager\.com/gtm\.js|GTM-[A-Z0-9]{5,}", "web-frontend: tag manager access control"),
    ("tracker", "Google Analytics", r"google-analytics\.com|G-[A-Z0-9]{8,}|UA-\d{4,}-\d|react-ga|@google-analytics", "web-frontend: analytics BAA or config"),
    ("tracker", "TikTok Pixel", r"analytics\.tiktok\.com|ttq\.(load|track)", "web-frontend: ad pixel"),
    ("tracker", "LinkedIn Insight", r"snap\.licdn\.com|_linkedin_partner_id", "web-frontend: ad pixel"),
    ("tracker", "Session replay", r"hotjar|fullstory|logrocket|clarity\.ms|smartlook|mouseflow|inspectlet|sessionstack", "web-frontend: session replay on health pages"),
    ("tracker", "Product analytics", r"mixpanel|amplitude|segment\.com|analytics\.js|posthog|heap\.io|heapanalytics|rudderstack|pendo", "web-frontend / backend: analytics BAA or PHI-free config"),
    ("tracker", "Mobile attribution", r"appsflyer|adjust\.com|AdjustSdk|branch\.io|io\.branch|singular\.net|kochava|tenjin", "mobile: attribution SDK with health events"),
    ("tracker", "Ad SDK", r"com\.google\.android\.gms:play-services-ads|GoogleMobileAds|AppLovin|ironsource|unity3d\.ads|Vungle|Chartboost", "mobile: ad SDK"),
    ("tracker", "Advertising identifier", r"ASIdentifierManager|advertisingIdentifier|AdvertisingIdClient|getAdvertisingIdInfo|ATTrackingManager", "mobile: IDFA/GAID collection"),
    # LLM / AI
    ("llm", "OpenAI SDK/endpoint", r"api\.openai\.com|from openai import|require\(['\"]openai['\"]\)|from ['\"]openai['\"]|new OpenAI\(", "ai-llm: BAA, retention, identifier stripping"),
    ("llm", "Anthropic SDK/endpoint", r"api\.anthropic\.com|from anthropic import|@anthropic-ai/sdk|from ['\"]anthropic['\"]|new Anthropic\(", "ai-llm: BAA, retention, identifier stripping"),
    ("llm", "Google AI / Vertex", r"generativelanguage\.googleapis\.com|aiplatform\.googleapis\.com|google\.generativeai|@google/generative-ai|VertexAI", "ai-llm: BAA tier"),
    ("llm", "Azure OpenAI", r"openai\.azure\.com|AzureOpenAI", "ai-llm: BAA tier"),
    ("llm", "AWS Bedrock", r"bedrock-runtime|BedrockRuntime|InvokeModel", "ai-llm: BAA-eligible service check"),
    ("llm", "Other model APIs", r"api\.cohere\.|api\.mistral\.ai|api\.together\.xyz|api\.groq\.com|openrouter\.ai|huggingface\.co/api|api-inference\.huggingface", "ai-llm: contract status"),
    ("llm", "Vector store", r"pinecone|weaviate|qdrant|chromadb|milvus|pgvector|vectorstore", "ai-llm: embeddings as PHI datastore; RAG authorization"),
    ("llm", "LLM observability", r"langsmith|langfuse|helicone|portkey|braintrust|arize|wandb", "ai-llm: prompt logs to third party"),
    # Browser / device storage
    ("storage", "localStorage/sessionStorage", r"localStorage\.setItem|sessionStorage\.setItem|localStorage\[", "web-frontend: no PHI in browser storage"),
    ("storage", "IndexedDB", r"indexedDB\.open|idb\.openDB|Dexie\(", "web-frontend: no PHI in browser storage"),
    ("storage", "Document cookie write", r"document\.cookie\s*=", "web-frontend: no PHI in cookies"),
    ("storage", "iOS UserDefaults", r"UserDefaults\.standard\.set|NSUserDefaults", "mobile: PHI must not be in UserDefaults"),
    ("storage", "Android SharedPreferences", r"getSharedPreferences\(|SharedPreferences\.Editor", "mobile: use EncryptedSharedPreferences"),
    ("storage", "Unencrypted SQLite", r"SQLiteOpenHelper|sqlite3_open|openDatabase\(|Room\.databaseBuilder", "mobile: encryption for local DB"),
    ("storage", "AsyncStorage (RN)", r"AsyncStorage\.setItem|@react-native-async-storage", "mobile: AsyncStorage is not encrypted"),
    # PHI in URLs
    ("url-phi", "Health identifiers in URL build", r"[?&](ssn|dob|date_of_birth|mrn|patient_name|patientName|diagnosis|dx|icd|medication|phone|email)=", "backend / web-frontend: PHI in query string"),
    ("url-phi", "Patient identifier in path template", r"/patients?/\$\{|/patients?/\{|/patients?/:(id|mrn)", "backend: verify object-level authorization on patient routes"),
    # Secrets
    ("secret", "AWS access key", r"AKIA[0-9A-Z]{16}", "infrastructure: credential in source"),
    ("secret", "Private key block", r"-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----", "infrastructure: credential in source"),
    ("secret", "Generic API key assignment", r"(?i)(api[_-]?key|secret|token|password)\s*[:=]\s*['\"][A-Za-z0-9_\-/+=]{16,}['\"]", "infrastructure: credential in source"),
    ("secret", "Provider key prefixes", r"sk-[A-Za-z0-9]{20,}|sk-ant-[A-Za-z0-9\-_]{20,}|xox[bp]-[0-9A-Za-z\-]{20,}|AIza[0-9A-Za-z\-_]{30,}", "infrastructure: credential in source"),
    # Logging
    ("logging", "Console/log of patient objects", r"(console\.(log|debug|info)|logger\.(info|debug)|print\(|Log\.[dive]\(|NSLog\()\s*\(?[^)]*(patient|phi|diagnos|medication|dob|ssn|mrn)", "backend / mobile: PHI in logs"),
    ("logging", "Error tracking SDK", r"sentry|bugsnag|rollbar|crashlytics|datadog|newrelic|honeybadger|airbrake", "infrastructure: BAA or PHI scrubbing"),
    # Mobile-specific
    ("mobile", "Push payload build", r"(notification|alert|body)\s*[:=].*(diagnos|medication|appointment|result|lab)", "mobile: PHI in push payload"),
    ("mobile", "Android backup allowed", r"android:allowBackup=\"true\"", "mobile: PHI in device backups"),
    ("mobile", "No FLAG_SECURE", r"FLAG_SECURE", "mobile: presence check only; absence in PHI screens is the issue"),
    ("mobile", "HealthKit / Health Connect", r"HKHealthStore|HealthKit|HealthConnectClient|androidx\.health\.connect", "mobile: platform health-data policy"),
    ("mobile", "iOS file protection", r"NSFileProtection|FileProtectionType", "mobile: presence check; verify Complete class on PHI files"),
    # Crypto / TLS
    ("crypto", "TLS verification disabled", r"rejectUnauthorized:\s*false|verify\s*=\s*False|InsecureSkipVerify:\s*true|NSAllowsArbitraryLoads.*true|allowsArbitraryLoads|trustAllCerts|ALLOW_ALL_HOSTNAME_VERIFIER|setHostnameVerifier", "infrastructure / mobile: certificate validation disabled"),
    ("crypto", "Weak algorithms", r"\b(MD5|SHA1|DES|RC4)\b|TLSv1\.0|TLSv1\.1|SSLv3", "backend: weak crypto"),
    ("crypto", "Plain HTTP endpoint", r"['\"]http://(?!localhost|127\.0\.0\.1|0\.0\.0\.0)[a-zA-Z0-9.\-]+\.(com|net|org|io|health|care)", "backend / mobile: plaintext transport"),
]
COMPILED = [(c, l, re.compile(p), h) for c, l, p, h in PATTERNS]


def iter_files(root):
    for dirpath, dirnames, filenames in os.walk(root):
        # skip vendored/build dirs and hidden dirs, but keep .github (workflows hold secrets and deploy config)
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and (not d.startswith(".") or d == ".github")]
        for fn in filenames:
            path = os.path.join(dirpath, fn)
            ext = os.path.splitext(fn)[1].lower()
            if ext in TEXT_EXT or fn.startswith(".env") or fn in ("Podfile", "Podfile.lock", "Dockerfile", "AndroidManifest.xml", "Info.plist"):
                try:
                    if os.path.getsize(path) <= MAX_FILE_BYTES:
                        yield path
                except OSError:
                    continue


def scan(root, max_hits):
    hits = []
    for path in iter_files(root):
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                for lineno, line in enumerate(f, 1):
                    for cat, label, rx, hint in COMPILED:
                        if rx.search(line):
                            hits.append({
                                "category": cat,
                                "label": label,
                                "file": os.path.relpath(path, root),
                                "line": lineno,
                                "hint": hint,
                                "snippet": line.strip()[:160],
                            })
                            if len(hits) >= max_hits:
                                return hits, True
        except OSError:
            continue
    return hits, False


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path")
    ap.add_argument("--json", action="store_true", help="emit JSON instead of text")
    ap.add_argument("--max-hits", type=int, default=2000)
    args = ap.parse_args()

    root = os.path.abspath(args.path)
    if not os.path.isdir(root):
        print(f"not a directory: {root}", file=sys.stderr)
        return 2

    hits, truncated = scan(root, args.max_hits)

    if args.json:
        json.dump({"root": root, "truncated": truncated, "hits": hits}, sys.stdout, indent=2)
        print()
        return 0

    by_cat = {}
    for h in hits:
        by_cat.setdefault(h["category"], []).append(h)

    print(f"health-release-review scan of {root}")
    print(f"{len(hits)} lead(s){' (truncated)' if truncated else ''}. Leads are not findings until checked.\n")
    order = ["secret", "crypto", "tracker", "llm", "url-phi", "storage", "logging", "mobile"]
    for cat in order:
        items = by_cat.get(cat)
        if not items:
            continue
        print(f"== {cat} ({len(items)}) ==")
        for h in items:
            print(f"  {h['file']}:{h['line']}  [{h['label']}]  {h['snippet']}")
            print(f"      -> {h['hint']}")
        print()
    if not hits:
        print("No leads matched. This does NOT mean the codebase is compliant; run the component checklists.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
