# OAuth 2.0 vs OAuth 2.0 + PKCE (A Practical Comparison)

## Introduction

OAuth 2.0 is an authorization framework used to delegate access to user resources without sharing passwords. It is commonly used for “Login with Google”, “Login with GitHub”, and similar flows.

However, the basic Authorization Code Flow has a security gap in certain client types (who cannot store secrets securely). PKCE (Proof Key for Code Exchange) was introduced to close that gap.

This article compares the standard OAuth Authorization Code Flow with the PKCE-enhanced version from a practical implementation perspective.

---

# 1. OAuth 2.0 Authorization Code Flow (Basic)

## Flow Overview

```
User → Client App → Authorization Server → Redirect → Authorization Code → Token Exchange → Access Token
```

## Step-by-step

### 1. Authorization Request

The client redirects the user to the authorization server:

```python
client_id
response_type=code
redirect_uri
scope
state
```

---

### 2. User Login

The provider authenticates the user and asks for consent.

---

### 3. Authorization Code Returned

Redirect back to the application:

```
/callback?code=AUTH_CODE&state=XYZ
```

---

### 4. Token Exchange

Backend exchanges the authorization code:

```python
client_id
client_secret
code
redirect_uri
grant_type=authorization_code
```

---

### 5. Access Token Received

```json
{
  "access_token": "...",
  "expires_in": 3600,
  "token_type": "Bearer"
}
```

The client can now access protected APIs.

---

## Security Model

The security relies on:

- Client secret (for confidential clients)
- Short-lived authorization code
- Redirect URI validation
- State parameter (CSRF protection)

---

## Weakness

If an authorization code is intercepted before exchange, it may be usable by an attacker in certain scenarios, especially for public clients (mobile apps, SPAs).

---

# 2. OAuth 2.0 + PKCE Flow

PKCE extends the Authorization Code Flow with a cryptographic binding between the authorization request and the token exchange.

---

## Flow Overview

```
User → Client → Authorization Server → Code + Challenge → Code Verifier → Token Exchange → Access Token
```

---

## Step 1: Create Code Verifier

A random high-entropy string:

```python
import secrets

code_verifier = secrets.token_urlsafe(64)
```

Stored temporarily by the client.

---

## Step 2: Create Code Challenge

```python
import hashlib
import base64

digest = hashlib.sha256(code_verifier.encode()).digest()

code_challenge = (
    base64.urlsafe_b64encode(digest)
    .rstrip(b"=")
    .decode()
)
```

---

## Step 3: Authorization Request

Same as OAuth, plus:

```
code_challenge
code_challenge_method=S256
```

---

## Step 4: Token Exchange

Instead of relying only on a client secret:

```python
client_id
code
redirect_uri
grant_type=authorization_code
code_verifier
```

---

## Step 5: Verification

The authorization server verifies:

```
SHA256(code_verifier) == code_challenge
```

Only then is the token issued.

---

# 3. Key Differences

## Authorization Request

| Feature | OAuth 2.0 | OAuth + PKCE |
|--------|------------|---------------|
| client_id | Yes | Yes |
| state | Yes | Yes |
| code_challenge | No | Yes |
| code_challenge_method | No | Yes |

---

## Token Exchange

| Feature | OAuth 2.0 | OAuth + PKCE |
|--------|------------|---------------|
| client_secret | Required (confidential clients) | Optional |
| code_verifier | No | Yes |

---

# 4. Security Comparison

## OAuth (Basic)

Relies on:

- Client secret
- Redirect URI validation
- Authorization code short lifetime

Risks:

- Authorization code interception
- Secret leakage in insecure environments

---

## OAuth + PKCE

Adds:

- Proof that the token redeemer is the same entity that started the flow

Protects against:

- Intercepted authorization codes
- Public client attacks (SPAs, mobile apps)
- Malicious token exchange attempts

---

# 5. When to Use Each

## Use OAuth + PKCE when:

- Mobile applications
- Single Page Applications (React/Vue)
- Desktop applications
- Public clients (cannot safely store secrets)

## Use OAuth + Client Secret when:

- Server-side web applications (Django, Spring, etc.)
- Confidential backend systems

## Best Practice Today

Use both when possible:

- PKCE adds defense-in-depth
- Client secret still authenticates the application

---

# 6. Django Perspective

## Basic OAuth

- Store `state`
- Exchange code using `client_secret`

## OAuth + PKCE

- Store `state`
- Store `code_verifier`
- Add `code_challenge` to auth request
- Send `code_verifier` during token exchange

No changes required to:

- User model
- Session handling
- Callback view structure

---

# 7. Mental Model

## OAuth

```
"Do you know the client secret?"
```

## PKCE

```
"Did you initiate this authorization request?"
```

---

# Conclusion

OAuth 2.0 with PKCE is not a replacement for OAuth but an extension that strengthens the Authorization Code Flow, especially for public clients. Modern systems often combine PKCE with client secrets to achieve layered security.