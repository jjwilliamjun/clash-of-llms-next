<h1 align="center">Clash of LLMs</h1>

<p align="center">
  <em>Two LLM agents compete to shift public opinion across a directed social network.<br/>
  One spreads misinformation with unlimited reach; the other debunks it on a budget.</em>
</p>

<p align="center">
  <img alt="Vue 3" src="https://img.shields.io/badge/Vue-3-42b883?style=flat-square&logo=vue.js&logoColor=white">
  <img alt="Python" src="https://img.shields.io/badge/Python-3-3776ab?style=flat-square&logo=python&logoColor=white">
  <img alt="Flask" src="https://img.shields.io/badge/Flask-2.2-000000?style=flat-square&logo=flask&logoColor=white">
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

```bash
git clone https://github.com/jjwilliamjun/clash-of-llms-next.git
cd clash-of-llms-next

python -m venv venv && source venv/bin/activate     # Windows: .\venv\Scripts\activate
pip install -r requirements.txt

cd clash-of-llms && npm install
```

**The frontend and the backend are two separate processes.** Start each in its own
terminal, so that restarting one does not take down the other:

```bash
# Terminal 1 — Flask API on http://127.0.0.1:5000
export OPENAI_API_KEY="sk-..."
cd clash-of-llms && ./run-backend.sh
```

```bash
# Terminal 2 — vue-cli dev server on http://localhost:8080
cd clash-of-llms && npm run serve
```

Open <http://localhost:8080>.

> [!NOTE]
> `requirements.txt` pins PyTorch and TensorFlow because the app can serve an uploaded
> custom model in place of the OpenAI API. That is a multi-gigabyte install. If you only
> want the OpenAI path, install everything except `torch` and `tensorflow`.

**Requires:** Python 3, Node.js 14+, a bash-compatible shell, and an OpenAI API key with
access to a GPT-4-class model. The key is read from the environment and never committed.

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
└── run-backend.sh                 Starts Flask alone; the frontend is `npm run serve`
```

| Layer | Technology |
| --- | --- |
| Frontend | Vue 3, Vue Router, vis-network, SheetJS, marked |
| Backend | Python 3, Flask, Flask-CORS, NetworkX, pandas |
| LLM | OpenAI API · optional PyTorch / TensorFlow model upload |
| Tooling | Vue CLI, ESLint, pytest |

## Testing

```bash
source venv/bin/activate
python -m pytest clash-of-llms/flask_app
```

Seven tests cover network generation, Red team message and potency behaviour, and the
core simulation loop. Widening this is on the roadmap.

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
- [ ] Widen test coverage beyond network generation and the core loop
- [ ] Tighten CORS and configuration handling for non-local deployment

## Licence

MIT — see [LICENSE](LICENSE). Copyright is held by the Clash of LLMs contributors, which
includes the original five-person team as recorded in this repository's commit history.
