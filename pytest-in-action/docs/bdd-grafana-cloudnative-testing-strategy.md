# BDD × Grafana × Cloud-Native Testing Strategy

## Purpose and Context

This document defines a long-term testing strategy built around **Grafana**, **BDD (Behavior-Driven Development)**, and
**cloud-native platforms (Kubernetes and Istio)**. The objective is not only to validate Grafana's native authorization
and permission system, but also to use Grafana as a _reference_ system for designing and practicing scalable,
production-grade testing methodologies that can later be transferred to a custom IDM platform built with Spring Security
and Spring Cloud.

Grafana is deliberately chosen because it is:

- API-first and cloud-native by design
- Stable and production-proven
- Rich in RBAC, multi-tenancy, and permission semantics
- Independent from Prometheus and other observability backends for testing purposes

This allows us to focus purely on **authentication**, **authorization**, **permissions**, **tokens**, and **tenant
isolation**.

## Why BDD in a Grafana-Centered Architecture

BDD is introduced **not as a replacement** for functional or integrating testing, but as a demantic connector across
layers.

In this architecture:

- **Functional tests** validate correctness of a single API, role and resource
- **Integration tests** validate cross-resource, cross-organization, and lifecycle behavior
- **BDD scenarios** system invariants and business-level guarantees

BDD also answers the question:
> Does the system still behave the way we fundamentally expect, regardless of internal changes ?

## Testing Pyramid: BDD * Grafana * Cloud-Native

The testing strategy follows a strict pyramid to maintain stability and cost-efficiency.

### Layers (Bottom -> Top)

Low-Level API & Utility Tests

- Context objects
- HTTP wrappers
- Error normalization

Functional API Tests

- Single role
- Single organization
- Single resource CRUD validation
- Example: Admin folder CRUD, Editor read/update constraints

Integration Tests (Primary Focus)

- Multi-organization isolation
- Token lifecycle (creation, revocation, expiration)
- RBAC matrix validation across resources
- Deployment-aware behavior (Docker / Kubernetes)

BDD Scenarios (Few but Critical)

- Business-critical security invariants
- Cross-role and cross-org guarantees
- Human-readable acceptance criteria

BDD scenarios must remain few, stable, and expressive.

## What BDD Is -- and Is Not

### BDD Is NOT:

- A different syntax for API tests
- UI-only automation
- A substitute for integraiton testing

### BDD IS:

- A contract describing **security** and **permission guarantees**.
- A documentation-driven verification of system behavior.
- A safety net during refactoring, platform migration, or architectural evolution.

BDD scenarios should survive:

- Database changes (SQLite -> Postgres)
- Deployments changes (VM -> Kubernetes)
- Infrastructure changes (no mesh -> Istio)

## Criteria: What Is Worth Writing as BDD (and What Is NOT)

### Worth Writing as BDD

BDD scenarios should satisfy **at least one** of the following:

#### Cross-boundary behavior

- Multiple roles
- Multiple organizaitons
- Multiple resources

#### Security invariants

- Permission boundaries must never regress
- Tenant isolation must never break

#### Lifecycle semantics

- Token revocation takes effect immediately
- Deleted resources cannot be accessed again

#### Architectural guarantees

- Deployment method does not alter authorization semantics
- Service mesh does not weaken identity boundaries

### NOT Worth Writing as BDD

- Simple CRUD success cases
- Single API parameter validation
- Error code mapping for a single endpoint
- Highly volatile or implementation-specific behavior
  These belong to functional or integration tests.

## Grafana Permission Model as a BDD Reference System

Grafana provides a rare combination of:

- Organization-level isolation
- Role-based permissions (Admin / Editor / Viewer)
- Resource-scoped authorization (Folder, Dashboard, Datasource)
- Token-based API

This makes it an ideal reference when designing:

- Fine-grained API authorization
- Role-to-resource matrics
- Long-lived service tokens vs human users

BDD scenarios should express _intent_, not mechanics, such as:

- An Editor must never delete a Folder
- A token scoped to Org A cannot read Org B resources

## Kubernetes and Its Role in the Testing Strategy

Kubernetes is treated as the **execution environment**, not the authorization authority:
Responsibilities:

- Process isolation
- Network boundaries
- Configuration injection

BDD does not test Kubernetes primitives directly. Instead, it validates that:

- Authorization behavior remains consistent when deployed on Kubernetes
- Scaling, restarts, and rescheduling do not affect permission guarantees

Kubernetes failures should never cause authorization bypass.

## Istio: Complementary, Not Replacing Authorization

Istio introduces:

- mTLS for service-to-service communication
- Identity at the workload level
- Traffic-level enforcement

However:

- Istio does NOT repalce Grafana's RBAC
- Istio does NOT understand business permissions semantics

Example invariant:
> Even if two services can communicate via mTLS, authorization rules are still enforced at the application level.

### Why Grafana Is an Ideal Long-Term Testbed

Grafana's strengths make it uniquely suitable for sustained testing practice:

- Rich and stable API surface
- Cloud-native design philosophy
- Mature permission and multi-tenant model
- Predictable frontend behavior

This allows future expansion into:

- Playwright / Selenium UI testing
- Login and redirection flows
- Page-level authorization checks
- Performance and load testing

All without introducing unnecessary instability.

### Strategic Outcome

By using Grafana as reference platform and BDD as a semantic connector:

- We gain deep understanding of real-world authorization systems
- We build transferable testing skills across API, integration, and E2E layers
- We create the blueprint for designing a future **Spring-Based IDM platform**

BDD comes the **architectural memory** of the system -- ensuring security, permissions, and tenant isolation remain
correct as the platform evolves. 







