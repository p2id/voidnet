# Repository Map

## Source inventory

| Source path | Role | Wiki destination |
|---|---|---|
| `README.md` | Entry point and links to canonical documents. | This wiki and [System overview](01-system-overview.md). |
| `manifesto/MANIFESTO.md` | Problem statement, identity, and desired outcome. | [System overview](01-system-overview.md). |
| `principles/PRINCIPLES.md` | Eighteen principles governing compatible implementations. | [Protocol model](03-protocol-model.md), [Governance and safety](06-governance-safety.md). |
| `protocol/PROTOCOL.md` | Protocol v0.1, actors, participation, governance, safety, and conformance. | [Architecture](02-architecture.md), [Protocol model](03-protocol-model.md). |
| `challenge/CHALLENGE.md` | Four entry actions and the invitation to act. | [Operational flows](04-operational-flows.md). |
| `launch/LAUNCH_KIT.md` | Copyable community introduction and participation templates. | [Community launch kit](05-community-launch-kit.md). |
| `examples/README.md` | Rules for documenting real examples. | [Community launch kit](05-community-launch-kit.md). |
| `CONTRIBUTING.md` | Contribution modes and fork-friendly repository norms. | [Governance and safety](06-governance-safety.md). |
| `CODE_OF_CONDUCT.md` | Repository-specific conduct and reporting. | [Governance and safety](06-governance-safety.md). |
| `LICENSE` | Public-domain dedication under the Unlicense. | [Wiki home](README.md). |
| Root `VOID — *.md` files | Expanded convenience copies of core documents. | Treat canonical subdirectory files as the maintainable source paths. |

## Canonical versus convenience files

The repository stores canonical versions under named directories such as `manifesto/`, `principles/`, `challenge/`, `launch/`, and `protocol/`. The root `VOID — ...` documents are longer convenience copies. If the documents diverge, maintainers should decide explicitly which version is authoritative before updating the wiki.

## Change impact guide

- A principle change affects the protocol model, architecture boundaries, and governance pages.
- A launch-template change affects operational flows and the launch kit page.
- A conduct or safety change affects the governance page and any implementation guidance.
- A new example should be checked for consent, privacy, and factuality before it is summarized here.

## Maintenance status

This wiki is a generated interpretation of the repository’s documentation snapshot. It should be regenerated or reviewed after substantial changes to the canonical source documents.

## References

[1]: https://github.com/p2id/Void_Protocols "VOID Protocols source repository"
