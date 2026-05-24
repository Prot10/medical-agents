# Raspberry Pi 5 deployment — NeuroBench review platform

End-to-end runbook for deploying the NeuroBench dataset review platform
(`review_api` on :8889 + the `web-review` static build) on a Raspberry Pi 5,
exposed publicly so external clinicians can review the v5 dataset.

**Why a Pi:** the review app does no LLM inference, so no GPU is needed. The Pi
gives a free always-on host with a real persistent filesystem, which solves
the ephemeral-disk problem that rules out most free PaaS tiers — annotations
are stored as one JSON file per `(reviewer, version, case)` triple under
`data/review/annotations/`, and that needs a real disk.

**Audience:** first-time Raspberry Pi user. Each phase has a confirmation
point — do not run ahead.

---

## TL;DR checklist

- [ ] **Phase 1** — Unbox & identify parts (5 min)
- [ ] **Phase 2** — Flash microSD card from a Mac (15–20 min)
- [ ] **Phase 3** — Assemble the Pi (cooler + case + SD card) (10–15 min)
- [ ] **Phase 4** — First boot + SSH from your Mac (5–10 min)
- [ ] **Phase 5** — System update + install Python toolchain (20–30 min)
- [ ] **Phase 6** — Copy the project + build the frontend on your Mac (15 min)
- [ ] **Phase 7** — Run the backend as a `systemd` service + Caddy reverse proxy (15 min)
- [ ] **Phase 8** — Expose publicly with Cloudflare Tunnel (10–15 min)
- [ ] **Phase 9** — Backups, SSH key, optional SSD migration (15 min)

Total: ~2 hours of attentive work.

---

## Settings reference (fill in as you go)

| Setting | Value |
|---|---|
| Pi hostname | `neurobench-review` (suggested) |
| Pi username | `paolo` (suggested) |
| Pi password | _(set during Phase 2)_ |
| Wi-Fi SSID | _(your network)_ |
| Wi-Fi country code | `IT` / `US` / your country |
| Pi local URL | `http://neurobench-review.local:8889` |
| Public URL | _(set during Phase 8)_ |

---

## Prerequisites

What you should have on hand:

- Raspberry Pi 5 + case + active cooler/fan + micro-HDMI cable + microSD card + USB-C power supply (in the box)
- A Mac on the same Wi-Fi network as the Pi will be on
- A way to read the microSD card on your Mac (built-in SD slot + adapter sleeve, or a USB SD reader)
- The `medical-agents` repo cloned on the Mac you'll use for Phase 6 (the rsync source)
- Your Wi-Fi SSID + password
- ~30GB free on the microSD (16GB minimum, 32GB recommended)

---

## Phase 1 — Unbox & identify parts (5 min)

Lay everything on a desk. Identify each piece:

- [ ] **Pi 5 board** — credit-card-sized green PCB. On its edges:
  - **USB-C port** (power input)
  - **Two micro-HDMI ports** (smaller than regular HDMI — we won't use these today)
  - **Four USB ports** (two blue USB 3.0 + two black USB 2.0)
  - **Gigabit Ethernet** port
  - **40-pin GPIO header** along the top long edge
  - **microSD slot** — flip the board over, thin slot near the USB-C edge
  - **4-pin "FAN" JST connector** on the top side near the GPIO pins — this is where the fan cable plugs in
- [ ] **Case** — with mounting screws, possibly with a built-in fan
- [ ] **Active cooler / heatsink** — has thermal pads with a protective film + a small fan with a 4-pin cable
- [ ] **micro-HDMI cable** — set aside, not used today
- [ ] **USB-C power supply** — the official Pi 5 PSU is 5V / 5A USB-C PD
- [ ] **microSD card** — often inside a full-size SD adapter sleeve

> **Do not plug in power yet.** Power-on only happens at the start of Phase 4.

---

## Phase 2 — Flash the microSD card from your Mac (15–20 min)

This writes Raspberry Pi OS to the SD card with Wi-Fi + SSH preconfigured, so
the Pi appears on your network at first boot.

### 2.1 — Install Raspberry Pi Imager

- [ ] Open <https://www.raspberrypi.com/software/> on your Mac
- [ ] Click **Download for macOS** → open the `.dmg` → drag **Raspberry Pi Imager** into `Applications`
- [ ] Launch Imager. If macOS warns it's from the internet, go to **System Settings → Privacy & Security → Open Anyway**

### 2.2 — Insert the microSD card into your Mac

- [ ] Put the microSD into the SD adapter sleeve, then into your Mac's SD slot (or use a USB SD reader)

### 2.3 — Configure Imager

- [ ] **CHOOSE DEVICE** → **Raspberry Pi 5**
- [ ] **CHOOSE OS** → **Raspberry Pi OS (other)** → **Raspberry Pi OS Lite (64-bit)**
  - *Lite* = no desktop, command-line only — exactly what you want for a server
  - *64-bit* matches the Pi 5 CPU
- [ ] **CHOOSE STORAGE** → select your microSD card. **Triple-check the name and size** — this drive will be erased
- [ ] Click **NEXT** → on the "Apply OS customisation settings?" prompt, click **EDIT SETTINGS**

### 2.4 — OS customisation (the headless magic — 5 subtabs)

**Hostname tab**
- [ ] Set hostname: `neurobench-review`

**Localisation tab**
- [ ] Time zone: yours (e.g., `Europe/Rome`)
- [ ] Keyboard layout: matches your physical keyboard

**User tab**
- [ ] Username: `paolo` (lowercase, no spaces)
- [ ] Password: strong, **write it down**

**Wi-Fi tab**
- [ ] SSID: your network name (exactly as it appears in your Mac's Wi-Fi menu)
- [ ] Password: your Wi-Fi password
- [ ] Wireless LAN country: your country code (e.g., `IT`)

**Remote Access tab**
- [ ] Toggle **SSH** ON
- [ ] Choose **Use password authentication** (we'll upgrade to SSH keys in Phase 9)

### 2.5 — Write the card

- [ ] Click **SAVE** → **YES** to apply customisation → **YES** to confirm erase
- [ ] Wait ~10 minutes for download + write + verify
- [ ] When "Write Successful" appears, click **CONTINUE**, then physically eject the SD card

✅ **Phase 2 complete when:** Imager confirmed "Write Successful" and the SD card has been ejected from your Mac.

---

## Phase 3 — Assemble the Pi (10–15 min)

> ⚠ Cooling configurations vary by case. Follow your case's printed instructions if you have them. The steps below are the common pattern.

### 3.1 — Attach the cooler

- [ ] Peel the protective film off the thermal pads on the underside of the heatsink
- [ ] Align the heatsink over the Pi 5 board so the pads sit on the main SoC chip (center of the board) and the RAM chip
- [ ] Press the spring-loaded push-pins through the mounting holes until they click
- [ ] Plug the fan's 4-pin cable into the **FAN** JST header on the board (top side, near the GPIO pins)

### 3.2 — Insert the microSD card

- [ ] Flip the Pi board over
- [ ] Insert the (flashed) microSD card into the slot, contacts facing the board
- [ ] Push it in — it's friction-fit on the Pi 5 (no spring-load), just firmly seated

### 3.3 — Place in case

- [ ] Set the Pi board into the bottom half of the case so the ports align with the cutouts
- [ ] Secure with the case's screws if applicable
- [ ] If the **case has its own fan** instead of (or in addition to) the active cooler, plug its cable into the FAN JST header — only one fan can use the header at a time
- [ ] Close the case lid

> 🚫 **Still no power.** Power-on is the first step of Phase 4.

✅ **Phase 3 complete when:** the Pi is fully assembled inside the case, microSD inserted, fan connected, ready to be powered.

---

## Phase 4 — First boot + SSH from your Mac (5–10 min)

### 4.1 — Power on

- [ ] Make sure your Mac is on the **same Wi-Fi network** the Pi will join
- [ ] Plug the USB-C power supply into the Pi (then into the wall)
- [ ] The Pi powers on automatically — you'll see a green activity LED blink
- [ ] **Wait ~90 seconds** for first boot. The Pi will:
  - Expand its filesystem to fill the SD card
  - Connect to Wi-Fi using your configured credentials
  - Start the SSH service

### 4.2 — SSH in from your Mac

- [ ] Open **Terminal** on your Mac
- [ ] Run:
  ```bash
  ssh paolo@neurobench-review.local
  ```
  (replace `paolo` if you used a different username)
- [ ] First time: type `yes` to accept the host key
- [ ] Type the password you set in Phase 2
- [ ] You should see the Pi's shell prompt: `paolo@neurobench-review:~$`

### 4.3 — If `.local` doesn't resolve

If `ssh: Could not resolve hostname`:

- [ ] Wait another minute and retry — first boot can take a bit
- [ ] List Pi services advertised on the network:
  ```bash
  dns-sd -B _ssh._tcp .
  ```
  (Ctrl-C to exit; look for the Pi hostname)
- [ ] Or check your router's admin page for a new device named `neurobench-review` and use its IP directly: `ssh paolo@<ip>`
- [ ] If still not appearing: the Wi-Fi credentials were likely mistyped during Phase 2 — re-flash the card with corrected settings

### 4.4 — Confirm you're in

- [ ] Run `hostname` — should print `neurobench-review`
- [ ] Run `uname -m` — should print `aarch64` (confirms 64-bit ARM)
- [ ] Run `vcgencmd measure_temp` — should print something like `temp=42.0'C` (fan is working if this stays under ~70°C under load)

✅ **Phase 4 complete when:** you have an SSH session into the Pi from your Mac.

---

## Phase 5 — System update + install Python toolchain (20–30 min)

All commands below run **on the Pi** via SSH.

### 5.1 — Update the system

```bash
sudo apt update
sudo apt full-upgrade -y
sudo reboot
```

- [ ] After `sudo reboot`, your SSH session will close. Wait ~60 seconds, then reconnect:
  ```bash
  ssh paolo@neurobench-review.local
  ```

### 5.2 — Install base dependencies

```bash
sudo apt install -y \
    git build-essential \
    python3 python3-pip python3-venv python3-dev \
    curl wget pkg-config \
    rsync \
    debian-keyring debian-archive-keyring apt-transport-https
```

### 5.3 — Install `uv`

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc
uv --version
```

- [ ] `uv --version` should print a version (e.g., `uv 0.x.y`)

✅ **Phase 5 complete when:** `uv --version` works and `sudo apt full-upgrade -y` reports no further updates.

---

## Phase 6 — Copy the project + build the frontend (15 min)

The Pi gets the **code** + the **prebuilt frontend** + the **v5 dataset**. The
frontend build runs on your Mac (faster, has Node toolchain), then we rsync
the result to the Pi.

### 6.1 — Build the frontend on your Mac

On the **Mac** (the one with the repo at `/Users/aprotani/Documents/medical-agents`):

```bash
cd /Users/aprotani/Documents/medical-agents/web-review
npm install
npm run build
ls dist/    # confirm there's an index.html and an assets/ folder
```

### 6.2 — Rsync the project to the Pi

Still on the Mac:

```bash
rsync -avz --progress \
  --exclude='.venv/' \
  --exclude='node_modules/' \
  --exclude='.git/' \
  --exclude='data/traces/' \
  --exclude='data/neurobench_v1/' \
  --exclude='data/neurobench_v2/' \
  --exclude='data/neurobench_v3/' \
  --exclude='data/neurobench_v4/' \
  --exclude='__pycache__/' \
  --exclude='.pytest_cache/' \
  --exclude='*.pyc' \
  --exclude='.DS_Store' \
  /Users/aprotani/Documents/medical-agents/ \
  paolo@neurobench-review.local:~/medical-agents/
```

- [ ] First run prompts for SSH password; subsequent runs (after Phase 9 SSH key setup) will be passwordless
- [ ] Expect ~5–15 minutes depending on Wi-Fi speed (v5 cases + dist)

### 6.3 — Install Python dependencies on the Pi

Back on the **Pi** SSH session:

```bash
cd ~/medical-agents
uv sync --all-packages
```

- [ ] This creates `.venv/` on the Pi and installs all backend dependencies
- [ ] Some packages (Pydantic v2, FastAPI, etc.) ship ARM64 wheels and install fast; any pure-Python packages also fine; nothing should need GPU/CUDA libs since this is the review API only

### 6.4 — Smoke-test the backend

Still on the Pi:

```bash
uv run uvicorn neuroagent.review_api.app:app --host 127.0.0.1 --port 8889
```

- [ ] You should see uvicorn startup logs ending with `Application startup complete`
- [ ] In a **second SSH session** to the Pi (`ssh paolo@neurobench-review.local` in a new Terminal tab):
  ```bash
  curl -s http://127.0.0.1:8889/api/v1/health 2>&1 | head
  # If no /health endpoint, try the OpenAPI doc:
  curl -s http://127.0.0.1:8889/docs | head
  ```
  Either should return non-empty content
- [ ] Stop the test server with Ctrl-C in the first SSH session

✅ **Phase 6 complete when:** the backend started cleanly and responded to a local curl on port 8889.

---

## Phase 7 — Auto-start + Caddy reverse proxy (15 min)

We make the backend auto-start on boot via `systemd`, and put **Caddy** in
front as a reverse proxy that:
- Serves the `web-review/dist/` static files on `/`
- Proxies `/api/*` to the FastAPI backend on `:8889`

Caddy listens on port 80 (and 443 if we ever do direct TLS — but Cloudflare
Tunnel handles TLS for us, so port 80 is fine).

### 7.1 — Create the `systemd` unit for the backend

On the **Pi**:

```bash
sudo tee /etc/systemd/system/neurobench-review.service > /dev/null <<'EOF'
[Unit]
Description=NeuroBench Review API
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=paolo
WorkingDirectory=/home/paolo/medical-agents
Environment="PATH=/home/paolo/.local/bin:/usr/local/bin:/usr/bin:/bin"
ExecStart=/home/paolo/.local/bin/uv run uvicorn neuroagent.review_api.app:app --host 127.0.0.1 --port 8889
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF
```

> If you used a username other than `paolo`, replace all `paolo` references above.

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now neurobench-review
sudo systemctl status neurobench-review
```

- [ ] Status should show `active (running)`
- [ ] Watch the logs live to confirm clean startup:
  ```bash
  journalctl -u neurobench-review -f
  ```
  (Ctrl-C to stop following)

### 7.2 — Install Caddy

```bash
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | \
  sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | \
  sudo tee /etc/apt/sources.list.d/caddy-stable.list
sudo apt update
sudo apt install -y caddy
```

### 7.3 — Configure Caddy

```bash
sudo tee /etc/caddy/Caddyfile > /dev/null <<'EOF'
:80 {
    encode gzip

    handle /api/* {
        reverse_proxy 127.0.0.1:8889
    }

    handle {
        root * /home/paolo/medical-agents/web-review/dist
        try_files {path} /index.html
        file_server
    }

    log {
        output file /var/log/caddy/access.log
        format console
    }
}
EOF

sudo systemctl reload caddy
sudo systemctl enable caddy
```

### 7.4 — Test from your Mac on the local network

On your **Mac**:

```bash
curl -I http://neurobench-review.local/
# expect HTTP/1.1 200 OK and content-type: text/html
curl -I http://neurobench-review.local/api/v1/health
# (or whatever an existing review_api endpoint is)
```

Or open `http://neurobench-review.local/` in a browser on your Mac — you should see the review app's UI (reviewer-code login page).

- [ ] If the page loads → static serving + proxy both work

✅ **Phase 7 complete when:** the review UI is reachable from your Mac at `http://neurobench-review.local/` and both `systemd` services (`neurobench-review`, `caddy`) are `enabled` and `active`.

---

## Phase 8 — Expose publicly with Cloudflare Tunnel (10–15 min)

> ⚠ **Decision point.** Pick ONE of the two approaches below. Named tunnel
> is recommended for clinician review (stable URL). Quick tunnel is fine if
> you don't have a domain — the review API does NOT use SSE, so the quick
> tunnel SSE limitation does not apply here.

### Option A — Quick tunnel (no account, no domain, fastest)

Pros: zero setup, no account needed. Cons: URL changes on every restart, no
SLA, 200-concurrent-request limit (more than enough for clinician review).

On the **Pi**:

```bash
# Install cloudflared (ARM64 .deb)
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64.deb
sudo dpkg -i cloudflared-linux-arm64.deb
cloudflared --version

# Launch a quick tunnel (foreground, prints the URL)
cloudflared tunnel --url http://localhost:80
```

The output includes a line like:
```
https://random-words-abc-xyz.trycloudflare.com
```
That's the public URL — share it with clinicians.

- [ ] Note: the URL is only valid while this `cloudflared` process is running, and it changes if you restart. For a sustained review window, use Option B.

### Option B — Named tunnel (stable URL, recommended)

Requires:
- A free Cloudflare account
- A domain managed via Cloudflare DNS (you can register cheaply at cost via Cloudflare Registrar, or transfer an existing domain)

On the **Pi**:

```bash
# Install cloudflared if not already done
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64.deb
sudo dpkg -i cloudflared-linux-arm64.deb

# Authenticate (this opens a browser link — copy it to your Mac's browser)
cloudflared tunnel login

# Create the tunnel
cloudflared tunnel create neurobench-review
# Note the Tunnel UUID it prints

# Write the config
mkdir -p ~/.cloudflared
cat > ~/.cloudflared/config.yml <<EOF
tunnel: <PASTE-UUID-HERE>
credentials-file: /home/paolo/.cloudflared/<PASTE-UUID-HERE>.json
ingress:
  - hostname: review.yourdomain.com
    service: http://localhost:80
  - service: http_status:404
EOF

# Create the DNS record pointing review.yourdomain.com → this tunnel
cloudflared tunnel route dns neurobench-review review.yourdomain.com

# Install as a systemd service (auto-start on boot)
sudo cloudflared service install
sudo systemctl enable --now cloudflared
sudo systemctl status cloudflared
```

- [ ] Replace `<PASTE-UUID-HERE>` with the actual UUID (appears twice)
- [ ] Replace `review.yourdomain.com` with the subdomain you want on your Cloudflare-managed domain
- [ ] Test from anywhere (not just your Wi-Fi): visit `https://review.yourdomain.com/` — Cloudflare handles HTTPS termination

✅ **Phase 8 complete when:** the review UI loads in a browser on a different network (e.g., your phone on 4G) at the public URL.

---

## Phase 9 — Backups, SSH key, optional SSD migration (15 min)

### 9.1 — Annotation backup cron

On the **Pi**:

```bash
mkdir -p /home/paolo/backups
crontab -e
```

Add this line (daily 3 AM rsync of annotations into a dated folder):

```cron
0 3 * * * rsync -az /home/paolo/medical-agents/data/review/annotations/ /home/paolo/backups/annotations-$(date +\%Y\%m\%d)/ 2>&1 | logger -t neurobench-backup
```

Save and exit (Ctrl-X, Y, Enter in `nano`).

- [ ] Verify cron is enabled: `sudo systemctl status cron`
- [ ] Optional: also rsync the backups off-Pi to your Mac periodically — from your Mac:
  ```bash
  rsync -az paolo@neurobench-review.local:~/backups/ ~/neurobench-backups/
  ```

### 9.2 — SSH key (replace password auth)

On your **Mac** (each Mac you'll SSH from):

```bash
# Skip ssh-keygen if you already have ~/.ssh/id_ed25519
ssh-keygen -t ed25519 -C "$(whoami)@$(hostname)"

ssh-copy-id paolo@neurobench-review.local
# Enter the Pi password one last time

ssh paolo@neurobench-review.local
# Should now log in without asking for a password
```

Then on the **Pi**, disable password auth:

```bash
sudo nano /etc/ssh/sshd_config
```

Find and set:
```
PasswordAuthentication no
PubkeyAuthentication yes
```

Then:

```bash
sudo systemctl restart ssh
```

- [ ] Test from a new Terminal: `ssh paolo@neurobench-review.local` — must still log in (via key)
- [ ] **Do not log out of all sessions until you've confirmed key login works**, or you'll be locked out

### 9.3 — Optional: SSD-over-USB migration (future)

The microSD card works fine for the review window but is the weakest link
long-term (write wear from frequent annotation saves). When ready:

- Buy a small USB-3 SSD (120GB is plenty) + USB-to-SATA cable, OR a Pi 5 NVMe HAT + small NVMe drive
- Use Pi Imager on the Mac to clone the running SD card to the SSD
- Follow the Pi 5 boot-order docs to boot from USB/NVMe first

Not blocking — defer until the SD card shows signs of trouble or after a successful review round.

✅ **Phase 9 complete when:** annotations are being backed up nightly, SSH key login works, and password auth is disabled.

---

## Day-to-day operations

| Task | Command (on the Pi) |
|---|---|
| Check backend status | `sudo systemctl status neurobench-review` |
| Tail backend logs | `journalctl -u neurobench-review -f` |
| Restart backend | `sudo systemctl restart neurobench-review` |
| Check Caddy status | `sudo systemctl status caddy` |
| Reload Caddy after config change | `sudo systemctl reload caddy` |
| Check tunnel status | `sudo systemctl status cloudflared` |
| Tail tunnel logs | `journalctl -u cloudflared -f` |
| CPU temp | `vcgencmd measure_temp` |
| Disk usage | `df -h /` |

### Updating the code or data

When you change something on the Mac and want to push it to the Pi:

```bash
# From the Mac:
rsync -avz --progress \
  --exclude='.venv/' --exclude='node_modules/' --exclude='.git/' \
  --exclude='data/traces/' \
  --exclude='data/neurobench_v1/' --exclude='data/neurobench_v2/' \
  --exclude='data/neurobench_v3/' --exclude='data/neurobench_v4/' \
  --exclude='__pycache__/' --exclude='*.pyc' --exclude='.DS_Store' \
  /Users/aprotani/Documents/medical-agents/ \
  paolo@neurobench-review.local:~/medical-agents/

# Then on the Pi:
ssh paolo@neurobench-review.local 'cd ~/medical-agents && uv sync --all-packages && sudo systemctl restart neurobench-review'
```

If you changed the frontend, rebuild on the Mac (`cd web-review && npm run
build`) before rsyncing — Caddy serves `dist/` directly so a Caddy reload
isn't usually needed (it serves whatever is on disk).

### Editing reviewer codes

```bash
# On the Pi:
nano ~/medical-agents/agent-platform/config/review/reviewer_codes.yaml
```

The backend hot-reloads on mtime change — no restart needed.

---

## Troubleshooting

**`ssh: Could not resolve hostname neurobench-review.local`**
- Wait longer after first boot (90s isn't always enough on first run)
- Check that your Mac is on the same Wi-Fi as the Pi
- Try the IP directly via router admin page

**Backend won't start (systemd status shows failed)**
- `journalctl -u neurobench-review -n 100` to see the error
- Common cause: `uv sync --all-packages` wasn't run, or `~/.local/bin/uv` path is different — `which uv` to confirm the path matches the `ExecStart` line

**Caddy returns 502 on `/api/*`**
- Backend isn't running. `sudo systemctl status neurobench-review`

**Frontend loads but API calls fail with 404**
- Check the React build is configured to call `/api/*` (not `http://localhost:8889/api/*`). The Vite proxy is only for dev — the production build must use relative URLs

**`cloudflared` quick tunnel URL randomly changes**
- That's expected — switch to named tunnel (Option B) for a stable URL

**Pi too hot under load**
- `vcgencmd measure_temp` — anything sustained >75°C is bad
- Confirm fan cable is plugged into the FAN JST header
- Check the case has airflow gaps

**SD card corruption / read-only filesystem**
- Time to migrate to SSD (Phase 9.3)
- Restore from `~/backups/annotations-*/`

---

## Files & paths reference

| What | Where |
|---|---|
| Project root on Pi | `/home/paolo/medical-agents/` |
| Backend code | `agent-platform/src/neuroagent/review_api/` |
| Frontend build | `web-review/dist/` |
| Annotations | `data/review/annotations/{version}/{reviewer}/{case_id}.json` |
| v5 dataset | `data/neurobench_v5/cases/` |
| Reviewer codes | `agent-platform/config/review/reviewer_codes.yaml` |
| systemd unit | `/etc/systemd/system/neurobench-review.service` |
| Caddy config | `/etc/caddy/Caddyfile` |
| Cloudflare config | `/home/paolo/.cloudflared/config.yml` |
| Backups | `/home/paolo/backups/annotations-YYYYMMDD/` |
