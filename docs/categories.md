# Category registry

Category identifiers are part of the dataset interface. Do not silently rename or repurpose them. A category addition requires a category suggestion issue, maintainer review, and coordinated changes to the YAML registry, JSON Schema, generator, tests, and documentation.

| ID | Description |
| --- | --- |
| `ai-soc-vendor` | AI SOC and SecOps vendors from the SecOps Unpacked directory. |
| `threat-news` | Security news outlets. |
| `threat-research` | Vendor and independent threat research labs. |
| `government-cert` | Government and CERT advisories. |
| `vulnerability-exploit` | Vulnerability, exploit and ransomware trackers. |

A source can belong to multiple categories. Use the narrowest useful set; do not add categories merely for discoverability.
