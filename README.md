# Dev Assessment - Webhook Receiver

Flask app that receives GitHub webhooks (Push, Pull Request, Merge), stores events in MongoDB, and shows them in a UI that polls every 15 seconds.

Reference: [techstax-dev/tsk-public-assignment-webhook-repo](https://github.com/techstax-dev/tsk-public-assignment-webhook-repo)

---

## Setup

- Create and activate virtualenv:
  ```bash
  pip install virtualenv
  virtualenv venv
  source venv/bin/activate   # Windows: .\venv\Scripts\Activate.ps1
  ```
- Install dependencies: `pip install -r requirements.txt`
- Optional: copy `.env.example` to `.env` and set `MONGO_URI` (e.g. `mongodb://localhost:27017`). If MongoDB is not running, the app uses in-memory storage.
- Run: `python run.py` — server at http://127.0.0.1:5000

Webhook endpoint: `POST http://127.0.0.1:5000/webhook/receiver` (Content-Type: application/json). Use ngrok for local testing and set this URL in action-repo’s GitHub webhook.

- `/` — UI (polls `/events` every 15s)
- `/events` — JSON list of events
- `/webhook/receiver` — receives GitHub payloads

---

## Submission

- Webhook repo: https://github.com/som2004-byte/webhook-repo
- Action repo: https://github.com/som2004-byte/action-repo
