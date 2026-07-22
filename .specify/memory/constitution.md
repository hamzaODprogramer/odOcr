<!--
  ================================================================
  SYNC IMPACT REPORT
  ================================================================
  Version change: (template) 0.0.0 → 1.0.0
  Modified principles: N/A (first-time fill from template)
  Added sections:
    - I. Code Quality First (NON-NEGOTIABLE)
    - II. Lightweight & Storage-Conscious
    - III. OCR Accuracy & Reliability
    - IV. CLI-First Modular Architecture
    - V. Simplicity & YAGNI
    - Storage & Performance Constraints
    - Development Workflow & Quality Gates
    - Governance (with versioning, amendment procedure, compliance)
  Removed sections: N/A
  Templates requiring updates:
    - .specify/templates/plan-template.md — ✅ no changes needed (generic Constitution Check placeholder)
    - .specify/templates/spec-template.md — ✅ no changes needed
    - .specify/templates/tasks-template.md — ✅ no changes needed
  Guidance files requiring updates:
    - README.md — ⚠ pending (no README exists yet; create one referencing these principles)
  Follow-up TODOs: None
  ================================================================
-->

# odOcr Constitution

## Core Principles

### I. Code Quality First (NON-NEGOTIABLE)

Code quality is the primary constraint. Every contribution MUST:

- Be reviewed for clarity, correctness, and maintainability before merging.
- Follow consistent formatting and linting rules defined in the project toolchain.
- Include tests for all new logic — unit tests for isolated functions, integration tests for cross-component behavior.
- Avoid dead code, commented-out blocks, and untested error paths.
- Pass all quality gates (linter, type checker, tests) before submission.

Rationale: In a resource-constrained environment, high code quality reduces debugging overhead, simplifies maintenance, and keeps the codebase lean.

### II. Lightweight & Storage-Conscious

The application MUST minimize its disk and memory footprint at all times.

- All dependencies MUST be justified — every added library MUST demonstrate clear value exceeding its size cost.
- Prefer standard-library solutions over third-party packages when feasible.
- Temporary files and caches MUST be cleaned up after use.
- Model files, language data, and assets MUST be stored efficiently (compressed, pruned, or streamed).
- Document the storage budget for each major component.
- Regularly audit and remove unused assets and dependencies.

Rationale: User explicitly cites insufficient storage. OCR tools often bundle large models and data files — every kilobyte counts.

### III. OCR Accuracy & Reliability

The core OCR pipeline MUST meet measurable accuracy standards.

- Define explicit accuracy targets (e.g., CER/WER rates) for supported languages and document types.
- Regression tests MUST be added for every detected failure mode.
- Pre-processing (deskew, binarization, denoising) MUST be configurable and tested.
- Post-processing (spell-check, layout reconstruction) MUST be optional and independently verifiable.
- OCR engine selection MUST favor accuracy-to-size ratio given storage constraints.

Rationale: OCR is the product's reason for existence. Quality drives user trust.

### IV. CLI-First Modular Architecture

Every major capability MUST be exposed as a standalone, testable unit with a CLI interface.

- Text in/out protocol: stdin/args → stdout, errors → stderr.
- Support JSON output for programmatic consumption and human-readable for interactive use.
- Modules MUST be independently runnable and testable without a GUI.
- Shared logic MUST be extracted into libraries, not duplicated across modules.
- The CLI MUST be the primary integration point; any future GUI MUST call the same CLI layer.

Rationale: Modular CLI architecture enables lightweight deployment (no GUI overhead), easy scripting, and independent testing of each OCR stage.

### V. Simplicity & YAGNI

Start simple. Do not build for hypothetical future needs.

- Implement only what the current feature specification requires.
- If a simpler solution meets requirements, prefer it — no "we might need this later" additions.
- Complexity MUST be justified in the implementation plan and approved during review.
- Prefer flat structures over deep hierarchies; prefer direct logic over abstraction layers.
- When a component grows beyond one clear responsibility, split it — not before.

Rationale: Every unnecessary abstraction or future-proofing adds code, tests, docs, and cognitive load — all of which consume storage and maintainability budget.

## Storage & Performance Constraints

The following resource limits MUST be respected unless explicitly waived in a feature plan:

- **Application total disk footprint**: MUST NOT exceed 100 MB.
- **Peak memory usage**: MUST NOT exceed 256 MB per OCR operation.
- **Dependency budget**: Every new dependency MUST be documented with its installed size and purpose in the feature plan.
- **Model storage**: OCR models MUST be fetched on-demand or bundled in a minimal default set; full model packs MUST be optional installs.
- **Cleanup**: All processing pipelines MUST implement explicit cleanup of intermediate artifacts.
- **Monitoring**: Every feature plan MUST include a storage/memory impact assessment.

Rationale: Storage is the binding constraint. Without explicit budgets, cumulative bloat will exceed available space.

## Development Workflow & Quality Gates

### Workflow Stages

1. **Specification**: Feature spec written and approved before any implementation begins.
2. **Planning**: Implementation plan created, including Constitution Check, complexity tracking, and storage impact assessment.
3. **Implementation**: Code written following TDD discipline (test → fail → implement → pass → refactor).
4. **Review**: Code review MUST verify constitution compliance — especially code quality and lightweight principles.
5. **Audit**: Every release MUST include a storage footprint audit comparing against the previous release.

### Quality Gates

- **Gate 1 (Pre-Plan)**: Constitution compliance check — feature MUST NOT violate any principle without documented justification and approval.
- **Gate 2 (Pre-Merge)**: All tests pass, linter clean, type checker clean, no size regressions without justification.
- **Gate 3 (Release)**: Storage audit complete, all known regressions documented or resolved.

### Commitment

Every team member is responsible for upholding these standards. Violations of the Code Quality principle or unchecked storage bloat MUST be flagged during review and addressed before merging.

## Governance

- This constitution supersedes all informal practices. Any conflict MUST be resolved by amending the constitution.
- **Amendment procedure**: Propose changes via a feature spec, get approval, update this document, update the version, and propagate to affected templates.
- **Versioning policy**: MAJOR for incompatible principle changes, MINOR for new principles or materially expanded guidance, PATCH for clarifications and typo fixes.
- **Compliance review**: Every feature plan MUST include a Constitution Check section. Plans that violate principles without documented justification MUST be rejected.
- **Runtime guidance**: Development workflow details are maintained in `.opencode/commands/speckit.constitution.md`.

**Version**: 1.1.0 | **Ratified**: 2026-07-22 | **Last Amended**: 2026-07-22
