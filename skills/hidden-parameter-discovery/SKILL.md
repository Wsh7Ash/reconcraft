---
name: hidden-parameter-discovery
description: "Find request parameters the interface does not expose, using response-difference observation rather than assumption. Use when an endpoint accepts parameters you can enumerate and you suspect debug, feature or role fields exist beyond the visible form"
pack: reconcraft
version: 1.0.0
category: bug-bounty-tooling
tags: [parameters, discovery, http]
---

# Hidden Parameter Discovery

> Find request parameters the interface does not expose, using response-difference observation rather than assumption

**Use when:** an endpoint accepts parameters you can enumerate and you suspect debug, feature or role fields exist beyond the visible form

**Avoid when:** the endpoint is rate-limited or state-changing, where parameter guessing could alter data you do not own

## Procedure

1. Establish a stable baseline request and repeat it to confirm status, length and body hash are constant before testing anything.
2. Test candidate parameter names one at a time on the baseline request, keeping method, body type and value constant.
3. Detect real parameters by any stable deviation: length, status, redirect, content type or a field that echoes back.
4. Confirm each hit by toggling the value and observing the response follow the toggle, which separates real handling from noise.
5. Group discovered parameters by endpoint and note their type so later testing can use the correct encoding and position.
6. Record parameters in your endpoint inventory with the evidence for each, keeping rate discipline throughout.

## Signals

- Adding a candidate name changes the response length consistently across several repeats, which is real handling rather than jitter.
- A parameter toggles behaviour such as verbose output, extra fields or a changed role context.
- The response echoes the parameter name itself, suggesting template or reflection handling worth noting.
- Dynamic values such as timestamps make lengths vary; your baseline must account for that before any verdict.

## Patterns

**1. Baseline stability**

```text
3 identical GETs -> 200, len=48210, hash=11bc (stable)
then add debug=true -> 200, len=51877, hash=cc03  DIFF -> candidate
```

**2. Toggle confirm**

```text
debug=true  -> verbose payload, fields +7
debug=false -> baseline payload
consistent flip across 3 alternations = real parameter
```

**3. Result row**

```text
GET /api/orders param=debug position=query type=bool evidence=length+field-delta
```

## Pitfalls

- Running the test once and calling a random length change a discovery, when dynamic content moves every response.
- Testing parameters on endpoints that write data, where a parameter such as overwrite could change state.
- Ignoring ordering: some servers reject bodies with unknown fields, hiding the parameter you are looking for.

## Done when

- Each reported parameter reproduces a stable baseline deviation and responds to value toggling.
- Parameters are recorded in inventory with evidence and method, and no state-changing endpoint was probed.

## References

- [PortSwigger - web parameter handling](https://portswigger.net/web-security)
- [RFC 9110 - request semantics](https://www.rfc-editor.org/rfc/rfc9110)
