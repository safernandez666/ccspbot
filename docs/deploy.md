# Deployment

Handoff notes for deploying `ccspbot` on Proxmox. Everything an operator or a
deployment agent needs to know is here.

## What this workload is

A Telegram bot using **long polling**. It opens outbound HTTPS connections to
`api.telegram.org` and holds them open; Telegram never connects inward.

The practical consequences:

- **No inbound port.** No reverse proxy, no certificate, no DNS record, no
  firewall pinhole. Do not provision any.
- **Outbound HTTPS to `api.telegram.org:443` is required.** If egress is
  filtered, allow that host. There is no proxy support configured.
- **Exactly one instance may run per bot token.** Two instances polling the
  same token make Telegram return `409 Conflict` to both and the bot stops
  responding. Do not scale this to more than one replica, and do not leave an
  old container running while starting a new one.

## Placement

Either an LXC container or a small VM running Docker works. If using LXC,
Docker inside an unprivileged container needs nesting enabled
(`features: nesting=1`). A minimal VM avoids that entirely and is the simpler
choice if there is no reason to prefer LXC.

## Resources

The workload is a single Python process with a SQLite file. It is small.

| Resource | Value |
|---|---|
| Memory | 256 MB limit, ~80 MB typical |
| CPU | 0.5 vCPU is ample |
| Disk | ~200 MB image, plus a volume that grows by roughly one row per answered question |

## Build

From the repository root, on branch `ccsp-question-bank`:

```bash
docker build -t ccspbot:latest .
```

The build compiles `content/*.json` into `sql/questions.db` inside the image
and **fails if any question is invalid**, so a bad content change cannot reach
production silently.

`.dockerignore` must be present. It keeps `.env`, `.venv`, `.git` and the test
suite out of the build context. Without it, a local `.env` holding the token
would be copied into an image layer.

## Required configuration

| Variable | Required | Notes |
|---|---|---|
| `TOKEN_BOT` | yes | Bot token from BotFather. **Secret.** |
| `TZ` | no | Defaults to `America/Argentina/Buenos_Aires`, set in the image. Affects log timestamps only. |

The container exits with status 1 and a clear message if `TOKEN_BOT` is unset,
so a misconfigured deploy fails immediately rather than running silently broken.

### Handling the token

Do not put the token in the compose file, in a `docker run -e` on the command
line, or in any file that is committed. Any of those puts it in shell history
or in the repository.

Write it to a root-owned file on the host and reference it:

```bash
install -m 600 /dev/null /etc/ccspbot.env
printf 'TOKEN_BOT=%s\n' 'the-token' > /etc/ccspbot.env
```

```bash
docker run -d --name ccspbot \
  --env-file /etc/ccspbot.env \
  -v ccspbot-data:/app/data \
  --restart unless-stopped \
  ccspbot:latest
```

Note that `docker inspect` still shows environment variables to anyone who can
reach the Docker socket. That is inherent to environment variables; the point
of the above is to keep the token out of the image, the repository and shell
history.

## Persistence

`/app/data` holds `stats.db`, the per-user attempt history that backs `/stats`
and `/weak`. **Mount it or it is lost on every restart.**

The question bank is deliberately *not* on this volume. It is baked into the
image read-only, so rebuilding the bank cannot destroy user progress. The two
reference each other only by question slug.

Back up by copying the volume:

```bash
docker run --rm -v ccspbot-data:/data -v "$PWD:/backup" alpine \
  tar czf /backup/ccspbot-stats-$(date +%F).tar.gz -C /data .
```

## Running it

```bash
export TOKEN_BOT="the-token"    # or use --env-file as above
docker compose up -d
```

`compose.yaml` in the repository root sets the restart policy, the volume, log
rotation and resource limits.

## Verifying the deploy

```bash
docker logs ccspbot
```

A healthy start logs the bank size:

```
INFO ccspbot: question bank loaded: 149 questions
```

Then message the bot `/start` in Telegram. It should reply with the command
list. If it does not:

| Symptom | Cause |
|---|---|
| Exits immediately, "TOKEN_BOT is not set" | Env var not reaching the container |
| Exits, "questions.db not found" | Image built without running `sql/build_db.py` |
| Starts, but never answers | Another instance is polling the same token, or egress to `api.telegram.org` is blocked |
| Statistics reset on restart | `/app/data` is not mounted |

## Upgrades

The question bank lives in the image, so **adding or correcting questions means
rebuilding and redeploying**:

```bash
git pull
docker compose build
docker compose up -d
```

Stop the old container before the new one starts, or the two will briefly
collide on the token. `docker compose up -d` handles this correctly; a manual
`docker run` alongside a running container does not.

The data volume is untouched by a rebuild.

## Security posture

- Runs as UID 10001, not root.
- No inbound network exposure at all.
- The token is supplied at run time. It is not in the image, the repository, or
  the CI workflow.
- **The previous token must be treated as compromised.** It was passed as a
  Docker build argument and fixed with `ENV` into images pushed to a public
  registry, so it is readable in those layers. Revoke it with `/revoke` in
  BotFather rather than merely replacing it.
