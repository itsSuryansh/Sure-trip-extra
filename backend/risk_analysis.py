"""
SureTrip v3 — Risk Analysis & Explanation Engine
"""
from dataclasses import dataclass
from typing import List
from simulation_engine import SimulationResult, LegConfig

MODE_NOTES = {
    "metro":          "Metro is signal-controlled and very consistent.",
    "cab":            "Cab variance is driven by urban traffic density.",
    "auto":           "Auto rickshaws face moderate urban traffic uncertainty.",
    "dtc_bus":        "City buses are subject to dwell time and signal delays.",
    "express_train":  "Express trains have fewer stops but platform congestion adds risk.",
    "mail_train":     "Mail/Express trains have the highest rail variance — crossing waits and scheduling gaps.",
    "flight":         "Flights carry ATC holds, boarding queues, and taxi-line uncertainty.",
    "intercity_bus":  "Intercity buses face the highest variance — highway traffic, rest stops, and diversions.",
    "volvo_bus":      "Volvo AC buses are faster and more reliable than state buses but highway variability remains.",
}

@dataclass
class RiskReport:
    risk_level: str
    risk_color: str
    main_risk_factor: str
    vulnerable_leg: str
    tightest_buffer_description: str
    sensitivity_explanation: str
    full_explanation: str
    recommendation_score: float


class RiskAnalyzer:
    def classify(self, pct: float):
        if pct >= 80: return "Low", "#22c55e"
        if pct >= 60: return "Medium", "#eab308"
        return "High", "#ef4444"

    def analyze(self, legs, sim: SimulationResult, option_name, total_cost, total_time_min) -> RiskReport:
        risk_level, risk_color = self.classify(sim.probability_of_success)
        n = len(legs)

        vuln = legs[sim.most_vulnerable_leg_idx]
        overflow_rate = sim.leg_overflow_rates[sim.most_vulnerable_leg_idx]
        vuln_desc = (
            f"{vuln.mode}: {vuln.from_location.split('(')[0].strip()} → "
            f"{vuln.to_location.split('(')[0].strip()} "
            f"(±{vuln.variance_minutes:.0f} min, {overflow_rate:.0f}% overflow)"
        )

        
        tight_idx = sim.tightest_buffer_idx
        if tight_idx < n - 1:
            tl = legs[tight_idx]
            nl = legs[tight_idx + 1]
            ratio = tl.buffer_after / max(1, tl.variance_minutes)
            qual = "critically tight" if ratio < 0.8 else "tight" if ratio < 1.5 else "adequate"
            tight_desc = f"{tl.buffer_after:.0f}-min buffer between {tl.mode} and {nl.mode} ({ratio:.1f}× variance — {qual})"
        else:
            tight_desc = "Final leg — no forward buffer required."

        sens_desc = (
            f"+10 min on {legs[0].mode} reduces reliability by ~{sim.sensitivity_10min:.1f} percentage points"
            f" ({'high sensitivity' if sim.sensitivity_10min > 8 else 'moderate' if sim.sensitivity_10min > 4 else 'low'})"
        )

        
        max_of = sim.leg_overflow_rates.index(max(sim.leg_overflow_rates))
        if sim.leg_overflow_rates[max_of] > 25:
            main_risk = f"{legs[max_of].mode} buffer overflow in {sim.leg_overflow_rates[max_of]:.0f}% of simulations cascades downstream"
        elif risk_level == "High":
            main_risk = f"Cumulative propagated delays exceed window in {sim.probability_of_failure:.0f}% of runs"
        elif risk_level == "Medium":
            main_risk = f"{vuln.mode} variance (±{vuln.variance_minutes:.0f} min) creates moderate deadline pressure"
        else:
            main_risk = f"Well-buffered route; {sim.probability_of_success:.0f}% probability of on-time arrival"

       
        if risk_level == "Low":
            narrative = (f"The {option_name} option is reliable. With {sim.probability_of_success:.0f}% "
                        f"on-time probability, buffers adequately absorb typical delays. "
                        f"{MODE_NOTES.get(vuln.mode, '')}")
        elif risk_level == "Medium":
            narrative = (f"The {option_name} option carries moderate risk ({sim.probability_of_success:.0f}% success). "
                        f"Roughly 1 in {max(2, round(100 / max(1, sim.probability_of_failure)))} journeys misses the deadline. "
                        f"{MODE_NOTES.get(vuln.mode, '')}")
        else:
            narrative = (f"High risk: only {sim.probability_of_success:.0f}% of simulated journeys arrive on time. "
                        f"More than 1 in 3 miss the deadline due to delay propagation. "
                        f"{MODE_NOTES.get(vuln.mode, '')}")


        speed_score = max(0, 100 - (total_time_min / 1800) * 100)  
        cost_score = max(0, 100 - (total_cost / 8000) * 100)      
        rec_score = sim.probability_of_success * 0.6 + speed_score * 0.25 + cost_score * 0.15

        return RiskReport(
            risk_level=risk_level,
            risk_color=risk_color,
            main_risk_factor=main_risk,
            vulnerable_leg=vuln_desc,
            tightest_buffer_description=tight_desc,
            sensitivity_explanation=sens_desc,
            full_explanation=narrative,
            recommendation_score=round(rec_score, 2),
        )
