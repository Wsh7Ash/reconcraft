# Recon plan - example-bounty.demo
Assets: api, web
Skills selected: 50 of 50

## scope
1. `program-scope-parsing` - Program Scope Parsing
   Turn a bug-bounty program's prose scope rules into an explicit allow, deny and unlisted asset list that can be checked before every request
2. `asset-inventory-baselining` - Asset Inventory Baselining
   Build a stable inventory of hosts, applications and interfaces for a program so later recon output can be diffed against a known starting point
3. `authorization-proof-checklist` - Authorization Proof Checklist
   Assemble and keep the written permission, program rules and target mapping that prove every test you run is authorized
4. `testing-window-and-rate-discipline` - Testing Window and Rate Discipline
   Keep scanning and crawling inside the program's stated rate limits and business hours so your recon never degrades the target

## enumerate
5. `passive-subdomain-discovery` - Passive Subdomain Discovery
   Grow a subdomain list from public datasets, certificate logs and archives without sending a single packet to the target
6. `active-subdomain-bruteforce` - Active Subdomain Bruteforce
   Confirm which candidate hostnames really exist by resolving them against authorized infrastructure while handling wildcard answers correctly
7. `subdomain-permutation-enumeration` - Subdomain Permutation Enumeration
   Derive likely sibling hostnames from known ones using wordlists and mutators, then verify each candidate instead of guessing blindly
8. `wildcard-dns-handling` - Wildcard DNS Handling
   Detect wildcard and catch-all DNS responses early and filter them out so enumeration results stay honest
9. `dns-record-triage` - DNS Record Triage
   Read the full record set of every in-scope zone to learn where mail, redirects and services actually point before any HTTP work begins
10. `dangling-cname-candidates` - Dangling CNAME Candidates
   Identify hostnames that still point at decommissioned third-party resources so you can report a takeover risk without touching anyone else's tenant
11. `shared-hosting-and-ip-attribution` - Shared Hosting and IP Attribution
   Decide whether an address genuinely belongs to the program before you scan it, avoiding shared CDNs, clouds and reverse proxies
12. `asn-netblock-attribution` - ASN and Netblock Attribution
   Map the vendor's autonomous systems and announced prefixes to find infrastructure that never appears in DNS or on the scope page
13. `virtual-host-enumeration` - Virtual Host Enumeration
   Discover web applications that share one address by varying Host headers and hostname routing within your authorized scope
14. `alternate-port-service-discovery` - Alternate Port Service Discovery
   Find additional services on vendor-owned addresses using careful, rate-limited probes that stay inside the authorized range
15. `passive-osint-chaining` - Passive OSINT Chaining
   Combine public sources into one picture of the target organization without ever contacting the vendor's systems

## discover
16. `content-discovery-with-wordlists` - Content Discovery with Wordlists
   Find undisclosed paths and endpoints with a controlled wordlist crawl that filters noise and respects your rate ceiling
17. `js-bundle-endpoint-mining` - JavaScript Bundle Endpoint Mining
   Pull API routes, hidden parameters and environment values out of the application's own JavaScript bundles
18. `source-map-recovery` - Source Map Recovery
   Locate and read published source maps and build artifacts to recover original file structure, comments and build configuration
19. `openapi-and-schema-discovery` - OpenAPI and Schema Discovery
   Find API description documents and derive the real endpoint, parameter and model surface from them
20. `robots-sitemap-wellknown-review` - Robots, Sitemap and Well-Known Review
   Read the machine-readable files the application publishes, since they routinely advertise administrative paths and registered capabilities
21. `hidden-parameter-discovery` - Hidden Parameter Discovery
   Find request parameters the interface does not expose, using response-difference observation rather than assumption
22. `legacy-backup-file-discovery` - Legacy Backup File Discovery
   Check whether the application serves exposed copies, archives or editor leftovers of its own files within your authorized scope
23. `deep-crawl-strategy` - Deep Crawl Strategy
   Crawl a modern application exhaustively with a frontier you control, so dynamic rendering and infinite loops do not decide your coverage
24. `authenticated-crawl-workflows` - Authenticated Crawl Workflows
   Crawl behind login using your own test accounts so role-gated surfaces appear in your inventory instead of hiding behind a redirect
25. `shadow-api-version-discovery` - Shadow API Version Discovery
   Find API versions and base paths the application still answers on but no longer advertises in its current client
26. `mobile-backend-endpoint-extraction` - Mobile Backend Endpoint Extraction
   Recover API hosts, headers and feature flags from a mobile application package you are authorized to analyze

## fingerprint
27. `technology-fingerprinting` - Technology Fingerprinting
   Identify the frameworks, servers and services behind a host from many weak signals so you know which behaviour to expect
28. `cms-framework-version-detection` - CMS and Framework Version Detection
   Pin down a content platform's exact version from public artifacts to compare against known advisories you are authorized to assess
29. `middleware-header-analysis` - Middleware Header Analysis
   Read response headers as a map of the middleware chain in front of the application, from cache layers to security controls
30. `cdn-waf-origin-attribution` - CDN and WAF Origin Attribution
   Work out whether you are talking to an edge or to the origin, without probing infrastructure that is not yours
31. `third-party-service-fingerprinting` - Third-Party Service Fingerprinting
   Identify the external services an application depends on so you know what is yours to test and what belongs to someone else
32. `certificate-transparency-recon` - Certificate Transparency Recon
   Mine public certificate logs for hostnames, issuers and renewal patterns that reveal infrastructure you have not seen elsewhere
33. `favicon-hash-infra-fingerprint` - Favicon and Asset Hash Fingerprinting
   Use stable asset hashes to cluster hosts that run the same application across your inventory and public datasets
34. `waf-presence-detection` - WAF Presence Detection
   Determine whether a web application firewall is filtering your traffic, and what that means for coverage and false results
35. `error-page-stacktrace-fingerprinting` - Error Page and Stacktrace Fingerprinting
   Read application error responses for framework, component and path details that normal pages never expose
36. `client-dependency-inventory` - Client Dependency Inventory
   Inventory the libraries, frameworks and components a browser loads, then assess each for known weakness and upgrade lag

## validate
37. `canonical-host-and-aliasing-checks` - Canonical Host and Aliasing Checks
   Establish which hostname is canonical for each application and which aliases reach it, so your results stay attributable
38. `parameter-behavior-baselining` - Parameter Behavior Baselining
   Characterize how each endpoint treats its parameters so later anomalies are compared against a known-good response
39. `status-code-response-size-baselining` - Status Code and Response Size Baselining
   Learn what each status code and response size means in this application so scanner output can be triaged instead of trusted
40. `object-id-surface-mapping` - Object ID Surface Mapping
   Map where the application exposes object identifiers, which is the first step toward reviewing object-level authorization
41. `redirect-chain-mapping` - Redirect Chain Mapping
   Trace every redirect hop, including client-side and protocol-level redirects, to see where navigation actually ends
42. `authentication-boundary-mapping` - Authentication Boundary Mapping
   Chart which routes, methods and operations require which credential, so public and protected surfaces are unambiguous
43. `mail-infrastructure-mapping` - Mail Infrastructure Mapping
   Map the mail systems a domain uses, including third-party senders, to understand account recovery and spoofing defens
44. `cloud-asset-discovery` - Cloud Asset Discovery
   Identify cloud services the application depends on from public naming, headers and configuration, and keep them scope-separated

## document
45. `recon-snapshot-capture` - Recon Snapshot Capture
   Capture a reproducible snapshot of everything you found so later runs can diff against it instead of starting from zero
46. `attack-surface-change-review` - Attack Surface Change Review
   Diff two recon snapshots and turn the differences into a short, prioritized list of what to test next
47. `duplicate-hypothesis-checking` - Duplicate Hypothesis Checking
   Before writing a report, check whether your finding is already known, already fixed, or already reported by someone else
48. `evidence-capture-hygiene` - Evidence Capture Hygiene
   Collect request and response evidence that proves your finding while keeping secrets, cookies and personal data out of it
49. `test-prioritization-handoff` - Test Prioritization Handoff
   Convert recon output into an ordered test plan that states what to test, in what order, and why each item ranks where it does
50. `recon-gap-audit` - Recon Gap Audit
   Audit your own recon for what is missing, biased or unverified, before you claim coverage to anyone else

Coverage by phase:
  scope         4 skills
  enumerate    11 skills
  discover     11 skills
  fingerprint  10 skills
  validate      8 skills
  document      6 skills
