#!/bin/bash
# Compute Engine startup script for AICompared (Debian/Ubuntu images).
# Attach at VM creation:
#   gcloud compute instances create ... --metadata-from-file=startup-script=deploy/gcp/startup-script.sh
#
# Installs Node 22, clones the repo, builds, and starts the systemd service.
# Idempotent: safe to re-run on reboot.
set -euo pipefail

REPO_URL="${REPO_URL:-https://github.com/matt-jones-org/AICompared.git}"
APP_DIR=/opt/aicompared

# --- Node.js 22 (NodeSource) ---
if ! command -v node >/dev/null 2>&1; then
  curl -fsSL https://deb.nodesource.com/setup_22.x | bash -
  apt-get install -y nodejs git
fi

# --- Service user ---
id -u aicompared >/dev/null 2>&1 || useradd --system --home "$APP_DIR" --shell /usr/sbin/nologin aicompared

# --- Fetch / update code ---
if [ -d "$APP_DIR/.git" ]; then
  git -C "$APP_DIR" pull --ff-only
else
  git clone "$REPO_URL" "$APP_DIR"
fi

# --- Build ---
cd "$APP_DIR"
npm ci
npm run build

# --- Env file (API keys) ---
# Never bake keys into this script or VM metadata visible to all users.
# Preferred: store the key in Secret Manager and fetch it here at boot:
#   GOOGLE_API_KEY=$(gcloud secrets versions access latest --secret=google-api-key)
if [ ! -f "$APP_DIR/.env" ]; then
  install -m 600 -o aicompared /dev/null "$APP_DIR/.env"
  if command -v gcloud >/dev/null 2>&1 && gcloud secrets describe google-api-key >/dev/null 2>&1; then
    echo "GOOGLE_API_KEY=$(gcloud secrets versions access latest --secret=google-api-key)" >> "$APP_DIR/.env"
  else
    echo "# Add provider keys here, e.g. GOOGLE_API_KEY=..." >> "$APP_DIR/.env"
  fi
fi

chown -R aicompared:aicompared "$APP_DIR"

# --- systemd service ---
cp "$APP_DIR/deploy/gcp/aicompared.service" /etc/systemd/system/aicompared.service
systemctl daemon-reload
systemctl enable --now aicompared
systemctl restart aicompared

echo "AICompared deployed. Check: systemctl status aicompared"
