# Vehicle Cybersecurity Gateway — Dashboard

Desktop-first React demo UI for the opendbc simulation backend.

## Prerequisites

- Python 3.11+ with `pip install -e ".[dashboard]"`
- Node.js 18+

## Run (two terminals)

**Terminal 1 — Backend API + WebSocket (port 8080):**

```bash
cd opendbc
python -m opendbc.simulation.server
```

**Terminal 2 — Frontend (port 5173):**

```bash
cd dashboard
npm install
npm run dev
```

Open http://localhost:5173

## Features

- Animated system flow & attack visualization
- Authentication panel (challenge-response demo)
- Security gateway + CAN firewall panels
- Virtual vehicle telemetry with **OpenDBC** vehicle profiles
- CAN packet inspector (raw + decoded)
- Threat simulation center (10 conceptual attacks)
- Full demo scenario controller
- Presentation & privacy modes

## Stack

React · Vite · TailwindCSS v4 · Framer Motion · Lucide · FastAPI WebSocket
