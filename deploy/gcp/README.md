# Deploying AICompared on Google Compute Engine

Runs the AICompared HTTP server (`src/server.ts`) on a small VM under systemd.

## Prerequisites (one-time, in your GCP project)

```bash
# Enable the Compute Engine API (this is where it's needed — not in app code)
gcloud services enable compute.googleapis.com

# Recommended: keep the Gemini key in Secret Manager instead of on-disk plaintext
gcloud services enable secretmanager.googleapis.com
printf '%s' "YOUR_GOOGLE_API_KEY" | gcloud secrets create google-api-key --data-file=-
```

## Create the VM

```bash
gcloud compute instances create aicompared \
  --zone=us-central1-a \
  --machine-type=e2-micro \
  --image-family=debian-12 --image-project=debian-cloud \
  --scopes=cloud-platform \
  --metadata-from-file=startup-script=deploy/gcp/startup-script.sh \
  --tags=aicompared

# Allow HTTP traffic to the server port (or front it with a load balancer/IAP)
gcloud compute firewall-rules create allow-aicompared \
  --allow=tcp:8080 --target-tags=aicompared
```

The startup script installs Node 22, clones the repo, builds it, pulls the
`google-api-key` secret into `/opt/aicompared/.env` (mode 600), and starts the
`aicompared` systemd service on port 8080.

> **Note:** the repo is currently private, so the plain `git clone` in the
> startup script will fail unless the VM has access (deploy key, or make the
> repo public, or bake a tarball into a GCS bucket). Adjust `REPO_URL` env or
> the script accordingly.

## Verify

```bash
gcloud compute ssh aicompared --zone=us-central1-a
systemctl status aicompared
curl -s localhost:8080/health        # {"status":"ok"}
curl -s localhost:8080/providers     # {"configured":["google"]}
curl -s localhost:8080/ask -X POST -H 'content-type: application/json' \
  -d '{"prompt":"Say hello in five words."}'
```

## Endpoints

| Method | Path         | Purpose                                   |
|--------|--------------|-------------------------------------------|
| GET    | `/health`    | Liveness check                            |
| GET    | `/providers` | Which provider API keys are configured    |
| POST   | `/ask`       | `{ prompt, model? }` → Gemini completion  |

## Security notes

- **Never** put API keys in VM metadata, the startup script, or the repo —
  use Secret Manager (wired in already) or write `/opt/aicompared/.env` by hand
  over SSH.
- Port 8080 open to the world means anyone can spend your Gemini quota.
  For anything beyond a demo, restrict the firewall rule to your IP
  (`--source-ranges=YOUR_IP/32`) or put the VM behind IAP / a load balancer
  with auth.
- `e2-micro` is in GCP's free tier in some regions; this app is I/O-bound and
  needs very little CPU.

## Updating

```bash
gcloud compute ssh aicompared --zone=us-central1-a --command \
  'cd /opt/aicompared && sudo git pull --ff-only && sudo npm ci && sudo npm run build && sudo systemctl restart aicompared'
```
