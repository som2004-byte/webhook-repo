# Dev Assessment - Webhook Receiver

Flask webhook receiver for GitHub events (Push, Pull Request, Merge). Stores events in MongoDB and serves a UI that polls every 15 seconds.

**Reference:** [techstax-dev/tsk-public-assignment-webhook-repo](https://github.com/techstax-dev/tsk-public-assignment-webhook-repo)

---

## Setup

### 1. Virtual environment

```bash
pip install virtualenv
virtualenv venv
```

**Activate:**

- Windows (PowerShell): `.\venv\Scripts\Activate.ps1`
- macOS/Linux: `source venv/bin/activate`

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

Minimum required: `Flask`, `pymongo`, `python-dotenv`.

### 3. Environment variables (optional)

Copy `.env.example` to `.env` and set MongoDB URI if needed:

```bash
copy .env.example .env
```

- **With MongoDB:** Set `MONGO_URI=mongodb://localhost:27017` (or your Atlas URI). Start MongoDB before running the app.
- **Without MongoDB:** Leave `MONGO_URI` unset or as placeholder; the app uses an in-memory fallback so it still runs and webhooks return 200.

### 4. Run the application

```bash
python run.py
```

Server runs at **http://127.0.0.1:5000**.

### 5. Webhook endpoint

Register this URL in your **action-repo** GitHub webhook (use ngrok for local testing):

```
POST http://127.0.0.1:5000/webhook/receiver
```

Content type: **application/json**. Events: **Pushes**, **Pull requests**.

---

## Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | UI: “Latest GitHub Activity” (polls `/events` every 15 seconds) |
| `/events` | GET | JSON list of stored events (latest first, max 20) |
| `/webhook/receiver` | POST | Receives GitHub webhook payloads; stores PUSH, PULL_REQUEST, MERGE |

---

## MongoDB schema

Events are stored with:

- `_id`: ObjectId (MongoDB default)
- `request_id`: string (commit hash for PUSH, PR id for PULL_REQUEST/MERGE)
- `author`: string (GitHub user)
- `action`: string — `"PUSH"` \| `"PULL_REQUEST"` \| `"MERGE"`
- `from_branch`: string \| null
- `to_branch`: string
- `timestamp`: string (UTC ISO datetime)

---

## UI display format

- **PUSH:** `{author} pushed to {to_branch} on {timestamp}`
- **PULL_REQUEST:** `{author} submitted a pull request from {from_branch} to {to_branch} on {timestamp}`
- **MERGE:** `{author} merged branch {from_branch} to {to_branch} on {timestamp}`

---

## Submission

- **Webhook receiver (this repo):** [GitHub – webhook-repo](https://github.com/som2004-byte/webhook-repo)
- **Action repo (triggers webhooks):** [GitHub – action-repo](https://github.com/som2004-byte/action-repo)

Both repositories are required for the assessment. Configure the webhook in **action-repo** to point to your deployed or ngrok-exposed `/webhook/receiver` URL.
