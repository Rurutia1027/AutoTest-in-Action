# API Testing Strategy: Functional Layers vs Integration Layer

## Purpose of This Document

This document formalizes the **testing philosophy and architecture** used for validating the observability stack
components (Prometheus, AlertManager, Grafana) at the **functional layer**, and clearly delineates what is intentionally
deferred to the **integration (BDD)** layer.

The primary goals are:

- Establish a **repeatable, automation-friendly testing mindest**
- Avoid premature coupling of multi-step business flows
- Ensure each component's API contract is verified in isolation before composing end-to-end scenarios

## Layered Testing Model (High-Level)

We explicitly divide testinng into two major layers:

### Functional Layer (Current Focus)

**Question answered**:
> "Does this API behave correctly in isolation, given valid or invalid inputs and permissions?"

**Characteristics**:

- Single-component scope (Grafana or Alertmanager or Prometheus)
- Stateless or minimally stateful per test
- Focus on **API correctness**, **contracts**, and **boundaries**
- No cross-component assumptions

### Integration Layer (Future Phase)

**Question answered**:
> "Do multiple components work together correctly to fulfill a business or operational scenario?"

**Characteristics**:

- Multi-component scope
- Multi-step workflows (chains of actions)
- Use **BDD** to express intent and behavior
- Validates side effects across systems

## What the Functional Layer Explicitly Covers

At the functional layer, we test **atomic capabilities** of each system

### Scope Definition

Functional tests:

- Validate **individual API endpoints**
- Assert HTTP semantics (status codes, payload shape)
- Validate authentication and authorization behavior
- Verify minimal state transitions when unavoidable

Functional tests **do not**

- Chain multiple APIs to represent a business flow
- Assert notification delivery, UI behavior, or external callbacks
- Validate timing-dependent or asynchronous orchestration

## Core Design Principles

### Fixture = Bootstrap + Environment Preparation

Fixtures are responsible for:

- Bootstrapping authentication (e.g., token generation)
- Preparing reusable runtime context
- Isolating system-level setup from test intent

Fixtures **must not**:

- Contain assertions
- Encode business logic
- Implicitly validate workflows

### Context Object = Identity + Runtime State

Each test operates through a **Context** object the encapsulates:

- Base URL
- Authentication token
- Organization / role / permissions

This ensures:

- No global mutable state
- Clear identitiy boundaries per test
- Natural support for RBAC testing

### One Test = One Responsibility

Each functional test should:

- Exercise one endpoint or one capability
- Validate **one expected behavior**

If a test requires:

- Creating -> updating -> querying -> deleting as a required chain

Then it is not **functional test layer** and belongs to the integration test layer.

### Example: AlertManager vs Integration Boundary

#### Functional Layer (Allowed)

- GET `/api/v2/status`
- POST `/api/v2/silences` (validate schema + response)
- Permission checks on silence creation

#### Integration Layer (Deferred)

- Alert fired -> silence supresses alert -> notification not sent
- Alert lifecycle involving Prometheus -> Alertmanager -> receiver
  The latter requires **ordering and cross-system validation**, which is out of scope for functional testing.

### Grafana-Specific Functional Testing Philosophy

Grafana functional tests focus on:

- Health and readiness APIs
- Authentication and token behavior
- Organization and RBAC boundaries
- CRUD correctness of individual resources

They intentionally **exclude**:

- UI validation
- Dashboard rendering correctness
- Alert rule execution chains

### Why We Defer Cover Chains to Integration

Core chains typically involve:

- Multiple APIs across components
- Temporal dependencies
- Side effects (alerts, metrics, notifications)

BDD provides:

- Clear narrative of behavior
- Human-readable intent
- Stable abstraction over changing APIs

Functional tests, by contrast, must remain:

- Fast
- Deterministic
- Isolated

### Expected Outcome of this Approach

By enforcing this separation, we gain:

- High signal-to-noise ratio in test failures
- Easier debugging and ownership
- Safe refactoring of integration flows
- Reusable building blocks for BDD scenarios

### Next Steps (Planned)

- Finalize functional test coverage for **Grafana core APIs**
- Extract reusable cotnexts into shared fixtures
- Define BDD feature files for integration scenarios
- Compose full observability workflows at the integration layer 