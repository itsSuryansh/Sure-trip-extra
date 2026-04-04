"""
SureTrip v3 — FastAPI Backend
Multi-city reliability-aware journey planning
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
 
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from datetime import datetime, timedelta
import uvicorn
 
from database import engine, Base
from simulation_engine import DelayPropagationSimulator, LegConfig
from risk_analysis import RiskAnalyzer
import models
import seed_data
 
# ── constants ────────────────────────────────────────────────────────────────
CITIES          = seed_data.CITIES
ROUTES          = seed_data.ROUTES
TRANSPORT_MODES = seed_data.TRANSPORT_MODES
 
# ── app setup ────────────────────────────────────────────────────────────────
app = FastAPI(title="SureTrip v3 API", version="3.0.0")
 
Base.metadata.create_all(bind=engine)
 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
 
# ── routes ───────────────────────────────────────────────────────────────────
 
@app.get("/")
def root():
    return {"message": "SureTrip v3 API", "version": "3.0.0"}
 
 
@app.get("/health")
def health():
    return {"status": "healthy"}
 
 
@app.get("/cities")
def get_cities():
    return [
        {
            "key":   k,
            "name":  v["name"],
            "lat":   v["lat"],
            "lon":   v["lon"],
            "code":  v["code"],
            "emoji": v["emoji"],
        }
        for k, v in CITIES.items()
    ]
 
 
@app.get("/routes")
def get_routes():
    return [
        {"src": s, "dst": d, "distance_km": ROUTES[(s, d)]["distance_km"]}
        for s, d in ROUTES.keys()
    ]
 
 
@app.post("/plan-journey")
def plan_journey(
    source:         str,
    destination:    str,
    departure_time: str,
    deadline_time:  str,
    n_simulations:  Optional[int] = 1000,
):
    # ── normalise inputs ──────────────────────────────────────────────────
    src = source.lower().strip()
    dst = destination.lower().strip()
 
    # ── validate cities ───────────────────────────────────────────────────
    if src not in CITIES:
        raise HTTPException(400, f"Unknown source city '{src}'. Valid: {list(CITIES.keys())}")
    if dst not in CITIES:
        raise HTTPException(400, f"Unknown destination city '{dst}'. Valid: {list(CITIES.keys())}")
    if src == dst:
        raise HTTPException(400, "Source and destination must differ.")
 
    # ── validate datetimes ────────────────────────────────────────────────
    try:
        dep  = datetime.fromisoformat(departure_time)
        dead = datetime.fromisoformat(deadline_time)
    except ValueError:
        raise HTTPException(400, "Invalid datetime format. Use ISO 8601.")
 
    if dead <= dep:
        raise HTTPException(400, "Deadline must be after departure.")
 
    # ── fetch route ───────────────────────────────────────────────────────
    try:
        route = seed_data.get_route(src, dst)
    except KeyError:
        raise HTTPException(404, f"No route data for {src} ↔ {dst}")
 
    # ── simulation setup ──────────────────────────────────────────────────
    n_sims     = min(max(n_simulations or 1000, 500), 2000)
    sim_engine = DelayPropagationSimulator(n_simulations=n_sims, random_seed=42)
    analyzer   = RiskAnalyzer()
    options_out = []
 
    def fmt_arr(minutes: float) -> str:
        t = dep + timedelta(minutes=minutes)
        return t.strftime("%H:%M, %d %b")
 
    # ── build each option ─────────────────────────────────────────────────
    for opt_key in ["fastest", "cheapest", "reliable"]:
        
        if opt_key not in route:
            continue
 
        tmpl = route[opt_key]
        legs = []
 
        for i, leg in enumerate(tmpl["legs"]):
            from_hub = seed_data.resolve_location(leg["from"])
            to_hub   = seed_data.resolve_location(leg["to"])
            legs.append(LegConfig(
                leg_id           = i,
                mode             = leg["mode"],
                from_location    = from_hub["name"],
                to_location      = to_hub["name"],
                base_travel_time = leg["base_time"],
                variance_minutes = leg["variance"],
                buffer_after     = leg["buffer"],
                cost             = leg["cost"],
                lat_from         = from_hub["lat"],
                lon_from         = from_hub["lon"],
                lat_to           = to_hub["lat"],
                lon_to           = to_hub["lon"],
            ))
 
        sim        = sim_engine.simulate(legs, dep, dead)
        total_cost = sum(l.cost for l in legs)
        total_time = (
            sum(l.base_travel_time + l.buffer_after for l in legs)
            - legs[-1].buffer_after
        )
        risk = analyzer.analyze(legs, sim, tmpl["name"], total_cost, total_time)
         
        # 🔥 ADD THIS HERE
        from ml_engine import predict_reliability

        ml_input = {
    "distance_km": route["distance_km"],
    "total_base_time_min": total_time,
    "total_buffer_min": sum(l.buffer_after for l in legs),
    "total_variance_min": sum(l.variance_minutes for l in legs),
    "total_cost_inr": total_cost,
    "n_legs": len(legs),

    "has_flight": int(any(l.mode == "flight" for l in legs)),
    "has_train": int(any("train" in l.mode for l in legs)),

    "tightest_buffer_ratio": min(l.buffer_after / l.base_travel_time for l in legs),
    "max_leg_variance_min": max(l.variance_minutes for l in legs),
    "min_buffer_min": min(l.buffer_after for l in legs),

    "variance_pct_of_base": sum(l.variance_minutes for l in legs) / total_time,
    "buffer_pct_of_base": sum(l.buffer_after for l in legs) / total_time,

    "deadline_multiplier": 1.0,
    "option_type_enc": ["fastest", "cheapest", "reliable"].index(opt_key),

    "src_delhi": int(src == "delhi"),
    "src_lucknow": int(src == "lucknow"),
    "src_chandigarh": int(src == "chandigarh"),
    "src_jaipur": int(src == "jaipur"),
    "src_pune": int(src == "pune"),

    "dst_delhi": int(dst == "delhi"),
    "dst_lucknow": int(dst == "lucknow"),
    "dst_chandigarh": int(dst == "chandigarh"),
    "dst_jaipur": int(dst == "jaipur"),
    "dst_pune": int(dst == "pune"),

    "std_arrival_min": sim.std_arrival_min,
    "mean_final_delay_min": sim.average_arrival_min,
    "risk_level_enc": 1
}

        ml_score = predict_reliability(ml_input)
        print("ML INPUT:", ml_input)
        print("ML SCORE:", ml_score)

        options_out.append({
    "type": tmpl["name"],
    "icon": tmpl["icon"],
    "description": tmpl["description"],

    "legs": [
        {
            "leg_number": i + 1,
            "mode": l.mode,
            "mode_display": TRANSPORT_MODES.get(l.mode, {}).get("name", l.mode),
            "mode_icon": TRANSPORT_MODES.get(l.mode, {}).get("icon", "🚗"),
            "mode_color": TRANSPORT_MODES.get(l.mode, {}).get("color", "#888"),
            "from_location": l.from_location,
            "to_location": l.to_location,
            "base_travel_time": l.base_travel_time,
            "variance_minutes": l.variance_minutes,
            "buffer_after": l.buffer_after,
            "cost": l.cost,
            "lat_from": l.lat_from,
            "lon_from": l.lon_from,
            "lat_to": l.lat_to,
            "lon_to": l.lon_to,
            "avg_delay": round(sim.leg_delay_means[i], 1),
            "overflow_rate_pct": round(sim.leg_overflow_rates[i], 1),
        }
        for i, l in enumerate(legs)
    ],   # ✅ VERY IMPORTANT COMMA

    # ✅ ADD HERE (INSIDE SAME DICT)
    "ml_score": ml_score,

    "total_base_time_min": round(total_time, 1),
    "total_cost": total_cost,
    "distance_km": route["distance_km"],
    "probability_of_success": sim.probability_of_success,
    "probability_of_failure": sim.probability_of_failure,
    "risk_level": risk.risk_level,
    "risk_color": risk.risk_color,
    "average_arrival_time": fmt_arr(sim.average_arrival_min),
    "best_case_arrival": fmt_arr(sim.best_case_arrival_min),
    "worst_case_arrival": fmt_arr(sim.worst_case_arrival_min),
    "arrival_std_min": sim.std_arrival_min,
    "main_risk_factor": risk.main_risk_factor,
    "vulnerable_leg": risk.vulnerable_leg,
    "tightest_buffer_description": risk.tightest_buffer_description,
    "sensitivity_explanation": risk.sensitivity_explanation,
    "full_explanation": risk.full_explanation,
    "recommendation_score": risk.recommendation_score,
    "arrival_distribution": sim.arrival_distribution,
})
        options_out.sort(key=lambda x: -x["recommendation_score"])
 
    return {
        "journey_options":   options_out,
        "recommended":       options_out[0]["type"] if options_out else None,
        "source":            src,
        "destination":       dst,
        "source_city":       CITIES[src]["name"],
        "destination_city":  CITIES[dst]["name"],
        "distance_km":       route["distance_km"],
        "departure_time":    departure_time,
        "deadline_time":     deadline_time,
        "simulation_runs":   n_sims,
    }
 
 
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
 