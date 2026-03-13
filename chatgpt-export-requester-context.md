# Export Requester Context

## Scope

This project exists to **initiate only** data exports from the ChatGPT and Claude web interfaces.

It should:

1. Run in a container
2. Reuse persisted Chromium profiles that are already logged into each service
3. Navigate to the service's UI
4. Open the export/data settings
5. Click the export button
6. Save screenshots and logs
7. Exit

It should **not**:

- read email
- poll IMAP
- download the export archive
- parse `conversations.json`
- use the OpenAI or Anthropic APIs
- require API keys

## Why this project exists

The user wants a low-friction way to periodically request data exports from ChatGPT and Claude without manually clicking through the UI each time.

The export email and archive handling remain manual for now.

## Architecture

```text
host cron / manual run
        ↓
docker compose run --rm exporter request          (ChatGPT)
docker compose run --rm claude-exporter claude-request  (Claude)
        ↓
Playwright launches Chromium with persistent profile
        ↓
session already authenticated
        ↓
navigate to export settings
        ↓
click export button
        ↓
write screenshots + logs
        ↓
exit
```

## Repository layout

```text
chatgpt-export-requester/
├── README.md
├── AGENTS.md
├── chatgpt-export-requester-context.md
├── Dockerfile
├── docker-compose.yml
├── .gitignore
├── scripts/
│   ├── request_export.py            # ChatGPT export
│   ├── request_claude_export.py     # Claude export
│   ├── bootstrap_profile.py        # ChatGPT bootstrap
│   ├── bootstrap_claude_profile.py  # Claude bootstrap
│   ├── run_export.sh
│   ├── run_claude_export.sh
│   ├── bootstrap_profile.sh
│   └── bootstrap_claude_profile.sh
├── logs/
├── profile/                         # ChatGPT session
├── claude-profile/                  # Claude session
└── screenshots/
```

## Implementation notes

### Persistent browser profile
Use a mounted profile directory per service. The first run should be interactive so the user can log in manually and persist cookies.

### Headless vs non-headless
- Bootstrap: non-headless
- Steady-state request mode: headless by default, but configurable

### Selector philosophy
Prefer selectors that are easy to adjust and well-commented. Each service has its own script with service-specific selectors that can drift independently.

### Proof of action
Each run should save:
- a timestamped log line
- a before screenshot
- an after screenshot
- an error screenshot on failure

## Security notes

The `profile/` and `claude-profile/` directories effectively contain authenticated session material. Protect them like credentials:
- do not commit them
- restrict permissions
- keep them off casual backups if possible

## Later phase plan

After a human downloads the archive manually, a separate project can:
1. unpack `conversations.json`
2. normalize thread/message structures
3. extract commands, config paths, services, fixes, and root causes
4. generate:
   - `SERVER_NOTES.md`
   - `AGENTS.md`
   - `KNOWN_ISSUES.md`
   - runbooks and helper scripts for `rin-city-infra`

That later parser/documentation project is intentionally out of scope here, but this repo should keep enough context to make that future phase straightforward.

## Suggested next iteration ideas
- add a dry-run mode that stops before clicking the export button
- add a healthcheck mode that verifies sessions are still logged in
- add selector fallback logic if the settings UI changes
- add structured JSON logging
