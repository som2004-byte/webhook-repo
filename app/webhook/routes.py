from flask import Blueprint, request, jsonify, render_template
from app.extensions import get_events_collection, fallback_insert_event, fallback_list_events
from datetime import datetime

webhook_blueprint = Blueprint("webhook", __name__)

@webhook_blueprint.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@webhook_blueprint.route("/webhook/receiver", methods=["POST"])
def github_webhook():

    payload = request.json
    event_type = request.headers.get("X-GitHub-Event")

    document = {}

    if event_type == "push":
        document = {
            "request_id": payload.get("after") or "",
            "author": payload["pusher"]["name"],
            "action": "PUSH",
            "from_branch": None,
            "to_branch": payload["ref"].split("/")[-1],
            "timestamp": datetime.utcnow().isoformat()
        }

    elif event_type == "pull_request":
        pr = payload["pull_request"]
        action = payload["action"]

        if action == "opened":
            document = {
                "request_id": str(pr["id"]),
                "author": pr["user"]["login"],
                "action": "PULL_REQUEST",
                "from_branch": pr["head"]["ref"],
                "to_branch": pr["base"]["ref"],
                "timestamp": datetime.utcnow().isoformat()
            }

        if action == "closed" and pr["merged"]:
            document = {
                "request_id": str(pr["id"]),
                "author": pr["user"]["login"],
                "action": "MERGE",
                "from_branch": pr["head"]["ref"],
                "to_branch": pr["base"]["ref"],
                "timestamp": datetime.utcnow().isoformat()
            }

    if document:
        try:
            get_events_collection().insert_one(document)
        except Exception:
            fallback_insert_event(document)

    return jsonify({"status": "ok"})


@webhook_blueprint.route("/events", methods=["GET"])
def get_events():
    try:
        events = list(get_events_collection().find().sort("timestamp", -1).limit(20))
    except Exception:
        events = fallback_list_events(limit=20)
    for e in events:
        if "_id" in e:
            e["_id"] = str(e["_id"])
    return jsonify(events)