<h1 align="center">Clash of LLMs</h1>

<p align="center">
  <em>Two LLM agents compete to shift public opinion across a directed social network.<br/>
  One spreads misinformation with unlimited reach; the other debunks it on a budget.</em>
</p>

<p align="center">
  <img alt="Vue 3" src="https://img.shields.io/badge/Vue-3-42b883?style=flat-square&logo=vue.js&logoColor=white">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.10%2B-3776ab?style=flat-square&logo=python&logoColor=white">
  <img alt="Flask" src="https://img.shields.io/badge/Flask-3-000000?style=flat-square&logo=flask&logoColor=white">
  <img alt="OpenAI" src="https://img.shields.io/badge/LLM-OpenAI%20API-412991?style=flat-square&logo=openai&logoColor=white">
  <a href="LICENSE"><img alt="MIT" src="https://img.shields.io/badge/licence-MIT-blue?style=flat-square"></a>
</p>

<p align="center">
  <a href="#how-the-simulation-works"><b>How it works</b></a> ·
  <a href="#quickstart">Quickstart</a> ·
  <a href="#architecture">Architecture</a> ·
  <a href="#provenance">Provenance</a> ·
  <a href="#roadmap">Roadmap</a>
</p>

---

A **Red agent** broadcasts misinformation on a topic to pull opinion toward its side. A
**Blue agent** counters by debunking it. Between them sits a network of **Green nodes** —
neutral agents, each with a predisposition and influence over the neighbours it links to.
Each round both agents generate a message with an LLM, the messages propagate through the
graph, and alignment is recomputed. Whichever side holds the majority when a termination
condition fires wins.

The asymmetry is the interesting part:

- **Red has unlimited reach but pays for overreach.** High-potency messages move the
  population harder, but nodes already leaning Blue grow sceptical of them.
- **Blue has limited energy.** Every broadcast costs, so Blue must choose which of Red's
  moves is worth answering — and runs out if it answers everything.

## Quickstart

One command per line, so this pastes into PowerShell as well as bash — Windows
PowerShell 5.1 does not accept `&&` and fails on the whole line if it sees one.

```bash
git clone https://github.com/jjwilliamjun/clash-of-llms-next.git
cd clash-of-llms-next
python -m venv venv
```

Activate it — this is the one line that differs by shell:

| Shell | Command |
| --- | --- |
| PowerShell | `.\venv\Scripts\activate` |
| cmd | `venv\Scripts\activate.bat` |
| bash, zsh | `source venv/bin/activate` |
| Git Bash on Windows | `source venv/Scripts/activate` |

Then, with the environment active:

```bash
pip install -r requirements.txt
cd clash-of-llms
npm install
```

Then run both halves:

| Shell | Command |
| --- | --- |
| PowerShell | `$env:OPENAI_API_KEY = "sk-..."` |
| cmd | `set OPENAI_API_KEY=sk-...` |
| bash, zsh | `export OPENAI_API_KEY="sk-..."` |

```bash
npm run dev
```

Open <http://localhost:8080>. Output is prefixed `[api]` and `[web]` so you can tell
which half is talking, and `--kill-others` means you never end up with one running
alone.

**They are still two independent processes.** `npm run dev` is a convenience over them,
not a replacement — when you want to restart one without the other, or watch one
closely, run them separately:

```bash
npm run dev:api     # Flask on http://127.0.0.1:5000  (or ./run-backend.sh)
npm run dev:web     # vue-cli dev server on http://localhost:8080
```

> [!IMPORTANT]
> **On Windows, Ctrl+C does not reliably stop everything.** Killing a process does not
> kill its children there, and this stack nests: a shell, the command, and then Flask's
> `--debug` reloader forking a supervisor and a worker. What survives keeps holding the
> port, and the next `npm run dev` then fails to bind for no visible reason.
>
> After Ctrl+C, if the ports are still busy:
>
> ```bash
> npm run dev:stop
> ```
>
> It kills by port rather than by process name, so it cannot take out an unrelated
> `node` or `python` you had running. To check by hand:
>
> ```powershell
> Get-NetTCPConnection -LocalPort 5000,8080 -State Listen
> ```
>
> Running the two halves in separate terminals avoids this: Ctrl+C there goes to that
> console's own process group.

> [!NOTE]
> Uploading your own PyTorch or TensorFlow model in place of the OpenAI API is optional,
> and those two are a multi-gigabyte install, so they are not in `requirements.txt`. Add
> them only if you want that feature:
> ```bash
> pip install -r requirements-custom-model.txt
> ```
> They are imported lazily, so the server starts and the simulation runs without them.

**Requires:** Python 3.10+ (developed against 3.13), Node.js 14+, and an OpenAI API key
with access to a GPT-4-class model. The key is read from the environment and never
committed.

No particular shell: `npm run dev` works the same in PowerShell, cmd, and bash. Only
`run-backend.sh` needs bash, and `npm run dev:api` does the same thing without it.

### Pointing the halves at each other

Because they are separate processes, each side has to be told where the other is. The
defaults work for local development and nothing needs setting.

| Setting | Side | Default | Set it when |
| --- | --- | --- | --- |
| `VUE_APP_API_BASE_URL` | frontend, `clash-of-llms/.env` | `http://127.0.0.1:5000` | the backend is not on this machine's port 5000 |
| `CORS_ORIGINS` | backend, environment | `http://localhost:8080,http://127.0.0.1:8080` | the frontend is served from another origin |
| `FLASK_PORT` | backend, environment | `5000` | port 5000 is taken |

Host spelling is not cosmetic here: a browser treats `http://localhost:8080` and
`http://127.0.0.1:8080` as **different origins** and matches them separately, so whichever
one you open has to appear in `CORS_ORIGINS`. Both are allowed by default for that reason.

`VUE_APP_*` variables are inlined by vue-cli at build time, so changing one needs a
restart of `npm run serve`.

### Configuring a run

Three spreadsheets in `clash-of-llms/public/documents/` define a simulation:

| File | Defines |
| --- | --- |
| `NodeConnections.xlsx` | Directed edges between Green nodes and the influence factor on each |
| `NodeAttributes.xlsx` | Each node's starting alignment and predisposition |
| `SimulationSettings.xlsx` | Team parameters, energy costs, and termination conditions |

Every column is documented in [`Setting_Guide.md`](clash-of-llms/public/documents/Setting_Guide.md).
Runs can be exported back to a spreadsheet for analysis.

## How the simulation works

```
round n
  ├─ Red    generate_message(topic)  ──▶  broadcast(potency, influence)  ──▶  green.update()
  ├─ Blue   generate_message(topic)  ──▶  broadcast(potency, influence)  ──▶  energy -= cost
  ├─ recompute red_alignment / blue_alignment over all Green nodes
  └─ terminate?  blue.energy == 0 · either alignment ≥ threshold · round == max
```

The loop lives in `flask_app/class_api/simulation.py`; team behaviour in `team.py`; the
Green network and propagation in `create_node_network/green_team.py`. Message generation
is dispatched through `llm_api/llm_handler.py`, which routes to the OpenAI API or to an
uploaded PyTorch / TensorFlow model.

The Flask API exposes each round (`/next_round`) so the frontend can step through a game
and render the network with vis-network, or run to completion (`/continuous_game`).

## Architecture

```
clash-of-llms/
├── flask_app/
│   ├── simulation_endpoint.py     Flask entry point — 13 routes
│   ├── class_api/                 Simulation loop, Red/Blue team logic, termination
│   ├── create_node_network/       Green node network generation and propagation
│   ├── excel_api/                 Spreadsheet import/export, parameter binding
│   └── llm_api/                   LLM dispatch: OpenAI API or uploaded custom model
├── src/
│   ├── components/                NetworkGraph · GamePlay · ParameterInput · FileUpload
│   ├── services/
│   │   ├── api.js                 Configured axios client — the only place the
│   │   │                          backend's address is written down
│   │   └── graphDataService.js    Round data → vis-network shape
│   └── views/                     Home · About
├── public/documents/              Default spreadsheets and in-app guides
├── scripts/stop-dev.mjs           Frees the dev ports when Ctrl+C leaves something behind
└── run-backend.sh                 Starts Flask alone, for a bash shell
```

Dependencies are split by what they are for:

```
requirements.txt                   Runtime — Flask, networkx, pandas, openai
requirements-custom-model.txt      Optional — PyTorch and TensorFlow, several GB
requirements-dev.txt               Tooling — pytest, pylint
```

| Layer | Technology |
| --- | --- |
| Frontend | Vue 3, Vue Router, vis-network, SheetJS, marked |
| Backend | Python 3.10+, Flask 3, Flask-Cors 6, NetworkX 3, pandas 2 |
| LLM | OpenAI API (SDK v1+) · optional PyTorch / TensorFlow model upload |
| Tooling | Vue CLI, ESLint, concurrently, pytest, pylint |

## Testing

With the virtual environment active (see [Quickstart](#quickstart)), from the
repository root:

```bash
pip install -r requirements-dev.txt
pytest
```

25 tests, no network access — the LLM call is mocked, so the suite checks the rules
rather than message quality.

| Area | Covers |
| --- | --- |
| Red team agent | Construction, round counting, alignment updates, and the penalty that turns a node away from Red — including the negative cases, with `random` pinned so the result is not a coin toss |
| Simulation loop | `next_round` termination: blue energy exhausted, either side reaching the majority threshold, the threshold coming from the `Termination` object, and a decided game staying decided |
| Network construction | Builds from the shipped spreadsheets and asserts the JSON contract the frontend reads |

One of those is a regression test worth naming: `test_json_uses_the_links_key` fails if
`node_link_data` stops emitting a `links` key. networkx 3.6 changed that default to
`edges` with no deprecation warning, which would empty the graph in the browser with no
error on either side.

`Simulation.start()` is not covered because it is dead code — `self._round_num` is only
assigned in a commented-out line, and it calls `generate_message` without the `previous`
argument the method requires. `next_round` is what the Flask endpoint drives.

## Provenance

**This started as a university group project built by a team of five.** That matters for
reading the commit history, so it is stated here rather than buried.

- **Origin.** The original repository is private. Its complete history — every
  contributor's commits, under their own names — is preserved here rather than squashed
  away. At the fork point it stood at 389 commits from five contributors.
- **My share.** 98 of those, roughly a quarter and the second-largest contribution: the
  LLM API integration and agent message-generation pipeline, the simulation endpoint, and
  the frontend components for parameter configuration and run playback.
- **From the fork point onward,** solo work. Anything dated after the fork is mine.

This repository exists so that continued development does not rewrite shared history or
imply sole authorship of what was a team effort.

## Roadmap

- [ ] Replace the linear influence model with a validated opinion-dynamics formulation
- [ ] Support model providers beyond the OpenAI API
- [ ] Batch mode: run many simulations headless and aggregate outcomes
- [ ] Widen coverage into green-network propagation and the Excel import/export path
- [ ] Remove the dead `excel_api/create_node_network/` duplicate
- [ ] Package the backend properly so modules stop importing each other as top-level names

## Licence

MIT — see [LICENSE](LICENSE). Copyright is held by the Clash of LLMs contributors, which
includes the original five-person team as recorded in this repository's commit history.
