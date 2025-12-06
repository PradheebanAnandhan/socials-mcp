# Unified Social-Media MCP Server

A lightweight, **open-source Model Context Protocol (MCP) server** that exposes a *single, consistent interface* to multiple social-media platforms.

This repository currently supports core posting & media-handling features for **Twitter / X**, **Facebook**, **Instagram**, **LinkedIn**, and lays the groundwork for additional platforms that can be switched on seamlessly as they are completed.

<div align="center">
  <img src="https://raw.githubusercontent.com/placeholder/socials-mcp/main/.github/hero.svg" width="600" alt="MCP Server architecture diagram"/>
</div>

---

## Road-map – Platform Checklist

| Status | Platform | Notes |
| ------ | -------- | ----- |
| ✅ | **Twitter / X** | Posting, deleting, media upload, analytics.<br/>Includes a specialised *rate-limited* client with automatic back-off. |
| ✅ | **Facebook** | Page posts, image uploads, comments, deletions. |
| ✅ | **Instagram** | Business/Creator photo container & publish, comments, deletions. |
| ✅ | **LinkedIn** | UGC post create / delete. |
| ✅ | **YouTube** | Video upload, search, analytics, comments |
| ⬜ | **Reddit** | Subreddit feed, submissions, voting |
| ⬜ | **Telegram** | Bot messaging, media, web-hooks |
| ✅ | **Discord** | Bot messaging, channel & guild utilities, MCP Server |

> Platforms not listed above are **out of scope for now** and will be revisited in future milestones.

---

## 1 · Architecture Overview

```
┌───────────────┐        ┌──────────────────────┐
│  Client App   │──────▶│  Unified MCP Server  │
└───────────────┘  HTTP  ├──────────┬───────────┤
                         │Core Auth │Rate-limit │
                         │& Routing │Supervisor │
                         └────┬─────┴──────┬────┘
            ┌─────────────────┤            ├─────────────────┐
            ▼                 ▼            ▼                 ▼
      Twitter Adapter   YouTube …    Reddit …        Discord …
```

* **Core layer** – Handles credential storage, request routing and global rate-limit safety.
* **Platform adapters** – Self-contained modules (e.g. `twitter.py`) implementing `{platform}_{action}` tool pattern.
* **Rate-limited adapter** – For endpoints that are prone to HTTP 429, providing automatic retry & exponential back-off (`twitter_rate_limits.py`).

Adding a new platform is as simple as dropping a new adapter file that subclasses the common base, registering its tools and credentials.

---

## 2 · Getting Started

### Prerequisites

* Python 3.10+
* A Twitter/X developer account (for current functionality)

### Installation

```bash
# Clone and enter the repo
$ git clone https://github.com/your-org/socials-mcp.git
$ cd socials-mcp

# Install dependencies
$ python -m venv .venv && source .venv/bin/activate  # optional but recommended
$ pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root (never commit this!) and add **at minimum** your Twitter credentials:

```dotenv
TWITTER_CONSUMER_KEY=xxxxxxxxxxxxxxxxxx
TWITTER_CONSUMER_SECRET=xxxxxxxxxxxxxxxxxx
TWITTER_ACCESS_TOKEN=xxxxxxxxxxxxxxxxxx
TWITTER_ACCESS_TOKEN_SECRET=xxxxxxxxxxxxxxxxxx
```

### Quick Start – Post a Tweet

```python
from Base_APIs.twitter import TwitterAPI

api = TwitterAPI()
api.create_tweet("Hello world from my unified MCP server! 🎉")
```

### Using the Rate-Limited Client

```python
from Base_APIs.twitter_rate_limits import TwitterRateLimitedAPI

tl = TwitterRateLimitedAPI()
print(tl.search_tweets("python", max_results=3))
```

The client will automatically wait or retry when a 429 status is returned and surfaces live rate-limit statistics via `get_rate_limit_status()`.

---

## 3 · Project Layout

```
Base APIs/
├── twitter.py              <- Core Twitter adapter (fast endpoints)
├── twitter_rate_limits.py  <- Twitter adapter w/ back-off
├── facebook_post.py        <- Facebook Page helper
├── insta_post.py           <- Instagram Graph helper
├── LinkedIn_post.py        <- LinkedIn UGC helper
└── requirements.txt
README.md (this file)
```

---

## 4 · Contributing

We :heart: contributions!  Before submitting a PR:

1. Fork the repo and create a feature branch.
2. Follow the naming pattern `{platform}_{action}` when adding tools.
3. Add tests or runnable examples where applicable.
4. Ensure `pre-commit run --all-files` passes (black, flake8, isort).

Open an issue if you're unsure where your change fits – we're happy to help.

---

## 5 · Contributors ✨

<table>
  <tr>
    <td align="center"><img src="https://avatars.githubusercontent.com/u/119799567?v=4" width="80;" alt="darkside"/><br /><sub><b>The&nbsp;Darkside</b></sub></td>
    <td align="center"><img src="https://avatars.githubusercontent.com/u/126973043?s=64&v=4" width="80;" alt="jk"/><br /><sub><b>JK</b></sub></td>
    <td align="center"><img src="https://avatars.githubusercontent.com/u/109946890?s=64&v=4" width="80;" alt="kanish"/><br /><sub><b>Kanish&nbsp;Yathra&nbsp;raj<br/>(joining&nbsp;soon)</b></sub></td>
  </tr>
</table>

> Want to see your face up there? Check out the next issue, pick one and open a PR! ✨

---

## 6 · License

This project is licensed under the **MIT License** – see the `LICENSE` file for details.

---

<div align="center">
Made with ☕ &nbsp;by the socials-mcp community
</div>
