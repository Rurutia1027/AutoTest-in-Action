# Grafana Authorization -- Functional Test Case Design

**_Scope: AuthN / AuthZ / RBAC / API Permission_**

## Test Scope & Assumptions

### In Scope

- Grafana **authentication**
- Organization-scoped authorization
- User / Group / Role RBAC
- API permission enforcement
- UI behavior consistency with backend auth
- Token & session handling

### Out of Scope (for functional layer)

- Performance
- Penetration testing
- OAuth provider internals

--- 

## Role & Permission Matrix (Baseline)

#### Role: Admin

**Resource Operations**

- Dashboard: CRUD
- Data Source: CRUD
- Org Settings: CRUD
- User: CRUD
- API: Full

#### Role: Editor

**Resource Operations**

- Dashboard: CRUD
- Data Source: Read
- Org Settings: None
- Users: None
- API: Write

#### Role: Viewer

**Resource Operations**

- Dashboard: Read
- Data Source: Read
- Org Settings: None
- Users: None
- API: Read

The Role & Permission are our **ground truth** for all test assertions.

## Authentication Test Case (AuthN)

### TC-AUTH-01: Valid Login

**Given**

- Valid user credentials

**When**

- User logs via Grafana UI and API

**Then**

- Login succeeds
- Auth token/session is issued
- User is redirected to correct organization context

### TC-AUTH-02: Invalid Credentials

**Given**

- Invalid username or password

**When**

- Login attempts

**Then**

- Authentication fails
- HTTP 401 returned
- No session/token created

### TC-AUTH-03: Token Expiry

**Given**

- Expired token

**When**

- API request is made

**Then**

- HTTP 401 returned
- User is required to re-authentication

---

## Organization Authorization Test Cases

###  

# TODO here not finished here, the case above should be attributed to integraiton test scenarios driven by BDD
# for now we only stopped at functional layer 