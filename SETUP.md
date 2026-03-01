# Webhook Receiver – Step-by-Step Setup

Follow these steps to run the Flask webhook receiver without errors.

---

## 1. Prerequisites

- **Python 3.8+**  
  Check: `python --version`
- **MongoDB** (optional for local dev)  
  Either install locally or use [MongoDB Atlas](https://www.mongodb.com/cloud/atlas).  
  If you skip this, the app still starts and uses `mongodb://localhost:27017` (MongoDB must be running for webhook storage).

---

## 2. Open the project folder

```powershell
cd "C:\Users\Somya verma\Documents\GitHub\Techstax_Assignment\webhook-repo"
```

(Use your actual path to `webhook-repo`.)

---

## 3. Create a virtual environment

```powershell
python -m venv venv
```

---

## 4. Activate the virtual environment

**Windows (PowerShell):**  
Run this from the **webhook-repo** folder (not from inside venv):

```powershell
.\venv\Scripts\Activate.ps1
```

If you're already inside `venv\Scripts`, use:

```powershell
.\Activate.ps1
```

*(The `.\` is required—PowerShell does not run scripts from the current directory by name alone.)*

If you get an execution policy error, run once:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Windows (Command Prompt):**

```cmd
venv\Scripts\activate.bat
```

**macOS/Linux:**

```bash
source venv/bin/activate
```

You should see `(venv)` in your prompt.

---

## 5. Install dependencies

```powershell
pip install -r requirements.txt
```

Minimum needed if you use a minimal env: `Flask`, `pymongo`, `python-dotenv`. The existing `requirements.txt` already includes them.

---

## 6. Configure environment (optional)

- There is a `.env` file in the project root.
- If `MONGO_URI` is missing or set to `your_mongodb_connection_string`, the app uses `mongodb://localhost:27017`.
- To use a real database, set in `.env`:

```env
MONGO_URI=mongodb://localhost:27017
```

Or for MongoDB Atlas:

```env
MONGO_URI=mongodb+srv://USER:PASSWORD@cluster.mongodb.net/
```

You can copy `.env.example` to `.env` and edit:

```powershell
copy .env.example .env
```

---

## 7. Run the application

From the `webhook-repo` folder (with `venv` activated):

```powershell
python run.py
```

You should see something like:

```
 * Running on http://127.0.0.1:5000
```

---

## 8. Verify it works

- **Home page:**  
  Open in browser: [http://127.0.0.1:5000/](http://127.0.0.1:5000/)
- **Events API:**  
  [http://127.0.0.1:5000/events](http://127.0.0.1:5000/events) (returns stored events as JSON)
- **Webhook endpoint (for GitHub):**  
  `POST http://127.0.0.1:5000/webhook/receiver`  
  Use this URL in your GitHub repo’s Webhooks settings.

---

## 9. Connect GitHub webhook (using ngrok)

GitHub cannot send webhooks to `127.0.0.1`. Use **ngrok** to give your local app a public URL.

### Step A: Install ngrok (if needed)

- Download from [ngrok.com](https://ngrok.com/download) or install with: `winget install ngrok`
- Sign up at [ngrok.com](https://ngrok.com) and copy your auth token from the dashboard, then run: `ngrok config add-authtoken YOUR_TOKEN`

### Step B: Run two things at once

You need **two terminals** open at the same time.

**Terminal 1 – Flask app**

1. Open PowerShell.
2. Go to the project and activate venv:
   ```powershell
   cd "C:\Users\Somya verma\Documents\GitHub\Techstax_Assignment\webhook-repo"
   .\venv\Scripts\Activate.ps1
   ```
3. Start the app:
   ```powershell
   python run.py
   ```
4. Leave this running. You should see: `Running on http://127.0.0.1:5000`

**Terminal 2 – ngrok**

1. Open a **second** PowerShell (do not close Terminal 1).
2. Run ngrok and forward to **port 5000** (same port as Flask):
   ```powershell
   ngrok http 5000
   ```
   *(Use `5000`, not `80` – your Flask app runs on 5000.)*
3. In the ngrok output you’ll see a line like:
   ```text
   Forwarding   https://abc1-23-45.ngrok-free.app -> http://localhost:5000
   ```
4. Copy the **https** URL only, e.g. `https://abc1-23-45.ngrok-free.app`  
   Do not copy `-> http://localhost:5000`.

### Step C: Add the webhook on GitHub

1. On GitHub: open your **repository** → **Settings** → **Webhooks** → **Add webhook**.
2. Fill the form like this:

   | Field            | What to enter |
   |------------------|----------------|
   | **Payload URL**  | Your ngrok URL + `/webhook/receiver`<br>Example: `https://abc1-23-45.ngrok-free.app/webhook/receiver` |
   | **Content type** | Choose **application/json** (not form-urlencoded). |
   | **Secret**       | Leave empty. |
   | **SSL**          | Keep “Enable SSL verification” checked. |

3. Under **Which events would you like to trigger this webhook?**
   - Choose **Let me select individual events**, then check at least:
     - **Pushes**
     - **Pull requests**
   - Or use **Just the push event** if you only want pushes.
4. Click **Add webhook**.

GitHub will send a test “ping”; if the URL is correct and both Flask and ngrok are running, the webhook will show a green check. After that, pushes and pull requests to the repo will hit your app and show up at http://127.0.0.1:5000/ and http://127.0.0.1:5000/events.

---

## Quick reference

| Step              | Command / action                          |
|-------------------|-------------------------------------------|
| Go to project     | `cd webhook-repo`                          |
| Create venv       | `python -m venv venv`                      |
| Activate (Win PS) | `.\venv\Scripts\Activate.ps1`             |
| Install deps      | `pip install -r requirements.txt`          |
| Run app           | `python run.py`                            |
| Webhook URL       | `POST http://127.0.0.1:5000/webhook/receiver` |

---

## Troubleshooting

- **“Import could not be resolved”**  
  Use the project root as the working directory and run `python run.py` from there so `app` is on the path.

- **“cannot import name 'events_collection'”**  
  Ensure you’re in `webhook-repo` when running and that `app/extensions.py` is present. If `MONGO_URI` is invalid, set it to a valid URI or leave it unset/placeholder to use localhost.

- **PowerShell: “activate” not found**  
  Use `.\venv\Scripts\Activate.ps1` or `.\activate` from `venv\Scripts`, not just `activate`.

- **MongoDB connection errors**  
  If you see something like:
  - `ServerSelectionTimeoutError: localhost:27017 ... actively refused`
  - `WinError 10061`

  It means **MongoDB is not running** (or not installed) on your machine.

  Fix options:

  - **Option A (local MongoDB)**:
    - Install MongoDB Community Server
    - Start the service (Windows):
      ```powershell
      net start MongoDB
      ```
      Or open **Services** (`services.msc`) → find **MongoDB Server** → **Start**
    - Then set `.env`:
      ```env
      MONGO_URI=mongodb://localhost:27017
      ```

  - **Option B (MongoDB Atlas)**:
    - Create a free cluster on Atlas
    - Copy the connection string and put it in `.env` as `MONGO_URI=...`

  Note: This project also has a **safe fallback**: if MongoDB is down, webhook deliveries still return 200 and events are stored in-memory temporarily (so the UI still works), but you won’t get persistence until MongoDB is running.
