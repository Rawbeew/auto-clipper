# 🔒 Cloudflare Zero Trust Access Integration Guide

**Cloudflare Access** (Zero Trust Network Access) secures your **ClipPulse AI Dashboard** and API endpoints (`https://auto-clipper.pages.dev`) behind single sign-on (SSO) or multi-factor authentication (MFA) without writing custom authentication servers.

---

## 🛡️ Architecture & How It Protects Your App

```
[User / Browser] ──► [Cloudflare Edge Proxy]
                             │
                             ▼
               ┌───────────────────────────┐
               │  Cloudflare Access (SSO)  │
               │  Google / GitHub / OTP    │
               └─────────────┬─────────────┘
                             │ (Authenticated JWT Assertion)
                             ▼
               ┌───────────────────────────┐
               │ Cloudflare Pages Frontend │
               │   + Middleware Gatekeeper │
               └─────────────┬─────────────┘
                             │
                             ▼
               ┌───────────────────────────┐
               │ GitHub Actions Runner /   │
               │ Social Auto-Post Pipeline │
               └───────────────────────────┘
```

When a user visits your Cloudflare Pages dashboard, Cloudflare Access verifies their identity via your configured Identity Provider (Google, GitHub, One-time PIN, Okta, Azure AD) **before** allowing them to view the page or invoke short generation APIs.

---

## 🛠️ Step-by-Step Configuration in Cloudflare Dashboard

### Step 1: Create an Access Application in Cloudflare Zero Trust
1. Log in to the [Cloudflare Zero Trust Dashboard](https://one.dash.cloudflare.com/).
2. In the left navigation menu, go to **Access** -> **Applications**.
3. Click **Add an Application** -> Select **Self-Hosted** or **Pages**.
4. Configure application details:
   - **Application Name**: `AutoClipper Dashboard`
   - **Session Duration**: `24 hours` (or your preferred timeout)
   - **Domain / Subdomain**: Enter your Pages domain (e.g. `auto-clipper.pages.dev` or custom domain `shorts.yourdomain.com`).
5. Click **Next**.

---

### Step 2: Configure Access Policy (Who can log in?)
1. Create an Access Policy:
   - **Policy Name**: `Allow Admin Users`
   - **Action**: `Allow`
2. Define inclusion rules:
   - **Selector**: `Emails` -> **Value**: `your-email@example.com`
   - *(Optional)* **Selector**: `Emails ending in` -> **Value**: `@yourdomain.com`
   - *(Optional)* **Selector**: `GitHub Organization` or `Google Group`
3. Click **Next** -> **Add Application**.

---

### Step 3: Configure Identity Providers (SSO)
1. In Zero Trust, go to **Settings** -> **Authentication** -> **Identity Providers**.
2. Add your preferred login method:
   - **Google OAuth**: One-click login with Google accounts.
   - **GitHub OAuth**: Single sign-on with GitHub handles.
   - **One-time PIN (OTP)**: Passwordless email login codes (zero external configuration required!).

---

### Step 4: Configure Service Tokens for Automated API Access
If you want to trigger short generation programmatically via CLI or external webhooks while Cloudflare Access is enabled:

1. In Zero Trust, go to **Access** -> **Service Tokens** -> **Create Service Token**.
2. Set Token Name: `AutoClipper CLI Token`.
3. Save the generated credentials:
   - `Client ID`: `xxxxxxxx.access`
   - `Client Secret`: `xxxxxxxxxxxxxxxxxxxxxxxx`
4. Create an Access Policy in your Application:
   - **Action**: `Non Identity` / `Service Token`
   - **Include**: `Service Token` -> Select `AutoClipper CLI Token`.
5. Now external scripts can pass these two HTTP headers to bypass interactive browser login:
   ```bash
   curl -X POST https://auto-clipper.pages.dev/api/clip \
     -H "CF-Access-Client-Id: YOUR_CLIENT_ID" \
     -H "CF-Access-Client-Secret: YOUR_CLIENT_SECRET" \
     -H "Content-Type: application/json" \
     -d '{"videoUrl": "https://youtube.com/watch?v=...", "maxClips": 3}'
   ```

---

## ⚙️ Middleware Enforcement in Code (`functions/_middleware.js`)

Your repository includes `functions/_middleware.js` which automatically validates Cloudflare Access headers on all requests.

To configure strict JWT / Token verification in your code:

1. Open Cloudflare Dashboard -> **Pages** -> **auto-clipper** -> **Settings** -> **Environment variables**.
2. Add environment variables:
   - `CF_ACCESS_TEAM_NAME`: Your Cloudflare Zero Trust team name (e.g., `myteam`).
   - `CF_ACCESS_CLIENT_ID`: Your Service Token Client ID.
   - `CF_ACCESS_CLIENT_SECRET`: Your Service Token Client Secret.
3. Redeploy your Pages application:
   ```bash
   wrangler pages deploy public --project-name=auto-clipper
   ```

Your dashboard and short creation pipeline are now protected with zero-trust security!
