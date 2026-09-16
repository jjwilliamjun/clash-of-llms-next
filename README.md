# Clash of LLMs — Next

A personal continuation of [Clash of LLMs](https://github.com/jjwilliamjun/Clash-of-LLMs), a simulation platform where two opposing LLM agents compete to shift public opinion across a directed social network.

<!-- TODO: replace with a screenshot or GIF of a running simulation -->

## Provenance

The original project was built by a team of five as a university group project, and its full commit history is preserved in this repository. This fork exists so that further work can be done solo without rewriting shared history or implying sole authorship of the original.

- **Upstream:** [`jjwilliamjun/Clash-of-LLMs`](https://github.com/jjwilliamjun/Clash-of-LLMs) — the team project as submitted, 389 commits.
- **My share of upstream:** 98 commits, roughly 25% and the second-largest contributor — LLM API integration and the agent message-generation pipeline, simulation endpoint work, and the frontend components for parameter configuration and run playback.
- **This repository:** everything after the fork point is my own work.

## What the simulation does

A **Red agent** broadcasts misinformation to pull public opinion toward its position. A **Blue agent** counters by debunking it. Between them sits a network of **Green nodes** — neutral agents, each with a predisposition toward one side and influence over the neighbours it links to. Whichever agent holds majority alignment at termination wins.

The asymmetry is the interesting part:

- **Red has unlimited reach but pays for overreach.** High-potency messages move the population harder, but Green nodes already leaning Blue grow sceptical of them.
- **Blue has limited energy.** Every broadcast costs, so Blue must choose which of Red's moves is worth answering.

## Roadmap

Planned work in this fork:

- [ ] Replace the linear influence model with a validated opinion-dynamics formulation
- [ ] Support models beyond the OpenAI API
- [ ] Batch mode: run many simulations headless and aggregate outcomes
- [ ] Expand test coverage beyond network generation and core simulation logic
- [ ] Tighten CORS and configuration handling for non-local deployment

<!-- Adjust the list above to match what you actually intend to build. -->

## Tech stack

| Layer | Technology |
| --- | --- |
| Frontend | Vue 3, Vue Router, vis-network, SheetJS (`xlsx`), marked |
| Backend | Python 3, Flask, Flask-CORS |
| LLM | OpenAI API; optional PyTorch / TensorFlow model upload |
| Tooling | Vue CLI, Babel, ESLint |

## Getting started

### Prerequisites

- Python 3.x
- Node.js 14 or later, with npm
- A bash-compatible shell (macOS, Linux, or WSL)
- An OpenAI API key with access to GPT-4 or newer

### Installation

```bash
git clone https://github.com/jjwilliamjun/clash-of-llms-next.git
cd clash-of-llms-next

python -m venv venv
source venv/bin/activate        # Windows: .\venv\Scripts\activate
pip install -r requirements.txt

cd clash-of-llms
npm install
```

### Configuration

```bash
export OPENAI_API_KEY="sk-..."
```

The key is read from the environment and is never committed.

### Running

```bash
cd clash-of-llms
./init.sh
```

Frontend on <http://localhost:8080>, Flask API on <http://localhost:5000>.

### Configuring a simulation

Three spreadsheets in `clash-of-llms/public/documents/` define a run — `NodeConnections.xlsx` (directed edges and influence factors), `NodeAttributes.xlsx` (per-node starting alignment), and `SimulationSettings.xlsx` (team parameters and termination conditions). `Setting_Guide.md` in the same directory documents every column.

## Project structure

```
clash-of-llms/
├── flask_app/
│   ├── simulation_endpoint.py     # Flask entry point and routes
│   ├── class_api/                 # Simulation loop, team logic, termination
│   ├── create_node_network/       # Green node network generation
│   ├── excel_api/                 # Spreadsheet import/export
│   └── llm_api/                   # LLM dispatch and custom model loading
├── src/
│   ├── components/                # NetworkGraph, GamePlay, ParameterInput, FileUpload
│   └── views/                     # HomeView, AboutView
└── public/documents/              # Default spreadsheets and in-app guides
```

## Testing

```bash
source venv/bin/activate
python -m pytest clash-of-llms/flask_app
```

## License

MIT — see [LICENSE](LICENSE). The original team project is under the same terms; see upstream for its contributor list.
