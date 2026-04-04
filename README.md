# SureTrip — Multi-City Reliability Intelligence

> Journey reliability quantified across 6 cities and 30 routes.
> Delhi  Lucknow  Chandigarh  Jaipur  Pune  Shimla
> ---


```
---
| Feature        | v3                     | v4                                           |
| -------------- | ---------------------- | -------------------------------------------- |
| Cities         | 5 cities               | **6 cities (added Shimla 🏔️)**              |
| Routes         | 10 combinations        | **15+ routes (auto reverse supported)**      |
| Engine         | Simulation only        | **Simulation + ML Hybrid 🔥**                |
| Route Handling | Manual both directions | **Auto reverse via `get_route()`**           |
| ML Model       | Not integrated         | **Fully integrated (`predict_reliability`)** |
| Error Handling | Basic                  | **Robust (None-safe + validation)**          |
| Backend        | Static logic           | **Dynamic + scalable architecture**          |


## ⚡ Quick Start



The complete simulation engine runs client-side in JavaScript.
open frontend/index.html
---

## 🐍 Backend Setup

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
API: http://localhost:8000

Docs: http://localhost:8000/docs

---
## Core Architecture
delay → overflow → carried forward → final arrival

## 🗺 Supported Routes (All 30 Directional Combinations)

| Route | Distance | Fastest Option | Cheapest | Most Reliable |
|---|---|---|---|---|
| Delhi → Lucknow | 556 km | Flight ~3.5hr | Bus ~9hr ₹595 | Shatabdi ~7.5hr |
| Lucknow → Delhi | 556 km | Flight ~3.5hr | Bus ~9hr ₹595 | Shatabdi ~7.5hr |

| Delhi → Chandigarh | 250 km | Volvo Bus ~5hr | State Bus ₹445 | Shatabdi ~4hr |
| Chandigarh → Delhi | 250 km | Volvo Bus ~5hr | State Bus ₹445 | Shatabdi ~4hr |

| Delhi → Jaipur | 270 km | Cab NH-48 ~4.5hr | Roadways ₹385 | Shatabdi ~5hr |
| Jaipur → Delhi | 270 km | Cab NH-48 ~4.5hr | Roadways ₹385 | Shatabdi ~5hr |

| Delhi → Pune | 1408 km | Flight ~3.5hr | Train ~24hr ₹1260 | Flight (reliable) |
| Pune → Delhi | 1408 km | Flight ~3.5hr | Train ~24hr ₹1260 | Flight (reliable) |

| Delhi → Shimla | 350 km | Cab ~7hr | Bus ~9hr ₹500 | Volvo Bus ~8hr |
| Shimla → Delhi | 350 km | Cab ~7hr | Bus ~9hr ₹500 | Volvo Bus ~8hr |

| Lucknow → Chandigarh | 600 km | Via-Delhi flight | Overnight bus ₹900 | Chandigarh Express |
| Chandigarh → Lucknow | 600 km | Via-Delhi flight | Overnight bus ₹900 | Chandigarh Express |

| Lucknow → Jaipur | 630 km | Direct flight | Mail train ₹740 | Express train |
| Jaipur → Lucknow | 630 km | Direct flight | Mail train ₹740 | Express train |

| Lucknow → Pune | 1400 km | Direct flight | Express train ₹1210 | Flight (reliable) |
| Pune → Lucknow | 1400 km | Direct flight | Express train ₹1210 | Flight (reliable) |

| Lucknow → Shimla | 750 km | Flight via Delhi | Bus ~14hr ₹900 | Train + Cab |
| Shimla → Lucknow | 750 km | Flight via Delhi | Bus ~14hr ₹900 | Train + Cab |

| Chandigarh → Jaipur | 540 km | Volvo Bus | State bus ₹730 | Train via Delhi |
| Jaipur → Chandigarh | 540 km | Volvo Bus | State bus ₹730 | Train via Delhi |

| Chandigarh → Pune | 1650 km | Flight (1-stop) | Train ₹1610 | Flight (reliable) |
| Pune → Chandigarh | 1650 km | Flight (1-stop) | Train ₹1610 | Flight (reliable) |

| Chandigarh → Shimla | 115 km | Cab ~3hr | Bus ₹250 | Cab (reliable) |
| Shimla → Chandigarh | 115 km | Cab ~3hr | Bus ₹250 | Cab (reliable) |

| Jaipur → Pune | 1150 km | Direct flight | Train ₹1050 | Flight (reliable) |
| Pune → Jaipur | 1150 km | Direct flight | Train ₹1050 | Flight (reliable) |

| Jaipur → Shimla | 600 km | Flight via Delhi | Bus ₹800 | Train + Cab |
| Shimla → Jaipur | 600 km | Flight via Delhi | Bus ₹800 | Train + Cab |

| Pune → Shimla | 1700 km | Flight via Delhi | Train ₹1500 | Flight (reliable) |
| Shimla → Pune | 1700 km | Flight via Delhi | Train ₹1500 | Flight (reliable) |

## 📊 Data Sources

All transport parameters are based on publicly available averages and real-world approximations:

| Mode | Source |
|---|---|
| Train times | Indian Railways NTES timetables (Shatabdi, Rajdhani, Mail Express, Kalka–Shimla Toy Train) |
| Flight durations | DGCA domestic route averages + airport processing/transfer overhead |
| Road times | National Highway (NH) distance charts + average speeds (including hill terrain adjustments for Shimla routes) |
| Bus times | HRTC (Himachal), RSRTC, MSRTC, UPSRTC timetable averages |
| Costs | Ola/Uber city averages, IRCTC fare tables, airline average fares, HRTC hill-route pricing |
| Variance | IRails delay stats, DGCA punctuality reports, hill travel variability (weather + terrain impact for Shimla) |

---

### 🏔 Shimla-Specific Notes

- Shimla has **no major commercial airport connectivity**, so:
  - Flights are routed via **Chandigarh or Delhi**
- Final leg often involves:
  - 🚗 Cab (mountain roads)
  - 🚌 HRTC buses (high variance)
  - 🚆 Kalka–Shimla toy train (low variance, slow but reliable)

- Hill routes include:
  - Higher variance due to:
    - Weather (fog, snow)
    - Road curvature & elevation
  - Lower average speeds compared to plains

---

### 📌 Key Assumptions

- All values are **realistic approximations**, not live data
- Buffers are dynamically modeled based on variance
- Hill routes (Shimla) have:
  - ↑ Higher delay variance  
  - ↑ Buffer requirements  
  - ↓ Speed consistency  

---
## 🎲 Simulation Model

### Delay Propagation (Core Innovation)


for each simulation run:
  carried_delay ← 0

 for each leg:
  delay ~ Normal(0, variance)
  overflow = max(0, delay + carried - buffer)
  carried = overflow
  
  arrival = Σ(base_time_i) + Σ(buffer_i) + carried_delay - last_buffer
  success = arrival ≤ deadline
```

### Buffer Sizing Rule

```
Buffer is sized proportional to variance — not a fixed constant:
- `buffer = (variance × 0.6) + fixed_transfer_time`
- Short urban legs: 15–20 min buffers
- Long intercity: 20–35 min buffers
- Flight connections: 20–25 min (checked in downstream)

### Risk Classification

| Probability | Risk | Color |
|---|---|---|
| ≥ 80% | Low | 🟢 Green |
| 60–79% | Medium | 🟡 Yellow |
| < 60% | High | 🔴 Red |

### Recommendation Score

score = reliability × 0.60 + speed_score × 0.25 + cost_score × 0.15
```

---

## 🔌 API Reference

### `POST /plan-journey`

```
POST /plan-journey?source=delhi&destination=pune&departure_time=2024-03-15T08:00:00&deadline_time=2024-03-15T14:00:00&n_simulations=1000
```

```
{
  "journey_options": [
    {
      "type": "Fastest",
      "probability_of_success": 82.4,
      "risk_level": "Low",
      "ml_score": 0.87,
      "average_arrival_time": "13:20",
      "vulnerable_leg": "...",
      "sensitivity_explanation": "..."
    }
  ],
  "recommended": "Fastest",
  "distance_km": 350
}
```

### `GET /cities` — List all cities with coordinates
### `GET /routes` — List all route combinations with distances

---

## 📁 Project Structure

```
suretrip_v3/
├── backend/
│   ├── main.py                  # FastAPI app
│   ├── simulation_engine.py     # Core Monte Carlo with propagation
│   ├── risk_analysis.py         # Risk classifier and explainer
│   ├── models.py                # SQLAlchemy ORM models
│   ├── database.py              # DB config
│   └── requirements.txt
│
├── database/
│   └── seed_data.py             # All cities, routes, transport data
│
├── frontend/
│   ├── index.html               # Complete self-contained app
│   └── app.js                   # Simulation + rendering engine
│
├── docker-compose.yml
└── README.md
```

---

## 🗺 Google Maps Integration Note

The `GOOGLE_MAPS_API_KEY` in `.env.template` is provided for future upgrade.
Current map uses **OpenStreetMap + CartoDB dark tiles via Leaflet** — no API key needed.

To upgrade to Google Maps:
1. Add `GOOGLE_MAPS_API_KEY` to `.env`
2. Replace Leaflet tile layer with Google Maps API initialization
3. Keep all reliability logic unchanged — Google Maps is visualization only

---

## 🐳 Docker

```bash
docker-compose up
# Frontend: http://localhost:3000
# API: http://localhost:8000
```
