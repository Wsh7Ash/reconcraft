---
name: parameter-behavior-baselining
description: "Characterize how each endpoint treats its parameters so later anomalies are compared against a known-good response. Use when you are about to test an endpoint seriously and need to know what normal looks like before you change anything"
pack: reconcraft
version: 1.0.0
category: bug-bounty-tooling
tags: [parameters, baseline, http]
---

# Parameter Behavior Baselining

> Characterize how each endpoint treats its parameters so later anomalies are compared against a known-good response

**Use when:** you are about to test an endpoint seriously and need to know what normal looks like before you change anything

**Avoid when:** an endpoint returns fully dynamic content you cannot stabilize, where a baseline would be noise by construction

## Procedure

1. Send the endpoint's request unchanged several times and record status, length, headers and body hash to measure natural variance.
2. Identify which parts of the response are dynamic, such as timestamps or tokens, so variance can be excluded from comparisons.
3. Vary one parameter at a time with benign values and note the response delta for each, keeping everything else constant.
4. Group parameters by behaviour class: reflected, stored, structural, controlling pagination or selecting fields.
5. Write the baseline profile to your notes with the exact request used, so the same request can be replayed later.
6. Re-baseline whenever the application changes, because an old baseline manufactures false anomalies.

## Signals

- Natural variance in length means raw length comparison cannot be a reliable detector on this endpoint.
- One parameter changes response structure while others only affect values, which separates routing-like controls from data inputs.
- A reflected parameter appears in the same encoding context each time, which is context worth recording for later review.
- Removing a parameter entirely changes status, suggesting it is required and handled earlier in the pipeline.

## Patterns

**1. Variance**

```text
3 identical requests: len=48210, 48218, 48213 (dynamic +-8 bytes)
-> compare with tolerance, not exact equality
```

**2. Delta row**

```text
param=page      class=pagination   delta=structure
param=q          class=reflect      delta=value
param=fields     class=projection   delta=field-set
```

**3. Baseline record**

```text
GET /api/items?page=1&limit=20 status=200 len~48215 hash_var=dynamic-timestamp
```

## Pitfalls

- Building the baseline once and reusing it weeks later after the application has shipped several releases.
- Changing multiple parameters at once, which makes attribution of the response delta impossible.
- Comparing raw bytes when the response embeds a changing token, producing endless false differences.

## Done when

- Natural variance is measured and excluded, and every parameter has a behaviour class with its delta recorded.
- The exact baseline request is stored so future sessions compare against the same known-good state.

## References

- [PortSwigger - web parameter behavior](https://portswigger.net/web-security)
- [RFC 9110 - request semantics](https://www.rfc-editor.org/rfc/rfc9110)
