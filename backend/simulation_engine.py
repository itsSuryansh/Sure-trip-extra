
import numpy as np
from dataclasses import dataclass
from typing import List
from datetime import datetime, timedelta


@dataclass
class LegConfig:
    leg_id: int
    mode: str
    from_location: str
    to_location: str
    base_travel_time: float   
    variance_minutes: float  
    buffer_after: float       
    cost: float              
    lat_from: float = 0.0
    lon_from: float = 0.0
    lat_to: float = 0.0
    lon_to: float = 0.0


@dataclass
class SimulationResult:
    probability_of_success: float
    probability_of_failure: float
    average_arrival_min: float
    worst_case_arrival_min: float    
    best_case_arrival_min: float     
    std_arrival_min: float
    leg_delay_means: List[float]
    leg_overflow_rates: List[float]
    most_vulnerable_leg_idx: int
    tightest_buffer_idx: int
    sensitivity_10min: float
    arrival_distribution: List[float]


class DelayPropagationSimulator:
    """
    Route-aware Monte Carlo simulation with delay propagation.

    Key improvement in v3:
      Variance is route-specific and calibrated to actual route duration.
      Short routes: variance is tightly bounded.
      Long routes: variance compounds — 22hr train has much higher spread.
    """
    def __init__(self, n_simulations: int = 1000, random_seed: int = 42):
        self.n = n_simulations
        self.rng = np.random.default_rng(random_seed)

    def _sample_delays(self, legs: List[LegConfig]) -> np.ndarray:
        """
        Draw delays per leg: Normal(0, σ) clipped to [-0.5σ, +2.5σ].
        Asymmetric clip: real delays skew late.
        """
        delays = np.zeros((self.n, len(legs)))
        for i, leg in enumerate(legs):
            raw = self.rng.normal(0.0, leg.variance_minutes, size=self.n)
            clipped = np.clip(raw, -0.5 * leg.variance_minutes, 2.5 * leg.variance_minutes)
            delays[:, i] = clipped
        return delays

    def simulate(
        self,
        legs: List[LegConfig],
        departure: datetime,
        deadline: datetime,
    ) -> SimulationResult:
        
        n_legs = len(legs)
        deadline_min = (deadline - departure).total_seconds() / 60.0

        raw_delays = self._sample_delays(legs)
        arrival_times = np.zeros(self.n)
        leg_delays_rec = np.zeros((self.n, n_legs))
        buffer_overflows = np.zeros((self.n, n_legs))

        
        total_base = sum(l.base_travel_time + l.buffer_after for l in legs) - legs[-1].buffer_after

        for sim in range(self.n):
            carried = 0.0
            for i, leg in enumerate(legs):
                leg_raw = raw_delays[sim, i]
                leg_delay = max(0.0, leg_raw)
                leg_delays_rec[sim, i] = leg_delay + carried

        
                overflow = max(0.0, carried + leg_delay - leg.buffer_after)
                buffer_overflows[sim, i] = 1.0 if overflow > 0 else 0.0
                carried = overflow

            arrival_times[sim] = total_base + carried

        
        successes = np.sum(arrival_times <= deadline_min)
        prob_success = float(successes / self.n * 100)

        sorted_arr = np.sort(arrival_times)
        mean_arr = float(np.mean(arrival_times))
        std_arr = float(np.std(arrival_times))
        p5 = float(sorted_arr[max(0, int(self.n * 0.05))])
        p95 = float(sorted_arr[min(self.n - 1, int(self.n * 0.95))])

        leg_means = [float(np.mean(leg_delays_rec[:, i])) for i in range(n_legs)]
        overflow_rates = [float(np.mean(buffer_overflows[:, i]) * 100) for i in range(n_legs)]

        
        vuln_scores = [legs[i].variance_minutes / max(1.0, legs[i].buffer_after) for i in range(n_legs)]
        vuln_idx = int(np.argmax(vuln_scores))

        # Tightest buffer (not last leg)
        if n_legs > 1:
            tight_scores = [legs[i].buffer_after / max(1.0, legs[i].variance_minutes) for i in range(n_legs - 1)]
            tight_idx = int(np.argmin(tight_scores))
        else:
            tight_idx = 0

        sens = 0

        sample = list(arrival_times[:min(200, self.n)])

        return SimulationResult(
            probability_of_success=round(prob_success, 1),
            probability_of_failure=round(100 - prob_success, 1),
            average_arrival_min=round(mean_arr, 1),
            worst_case_arrival_min=round(p95, 1),
            best_case_arrival_min=round(p5, 1),
            std_arrival_min=round(std_arr, 1),
            leg_delay_means=leg_means,
            leg_overflow_rates=overflow_rates,
            most_vulnerable_leg_idx=vuln_idx,
            tightest_buffer_idx=tight_idx,
            sensitivity_10min=sens,
            arrival_distribution=sample,
        )

    def _sensitivity(self, legs, departure, deadline, base_prob, delta=10.0):
        """Estimate reliability drop if first leg gets +10min."""
        mod = [LegConfig(
            l.leg_id, l.mode, l.from_location, l.to_location,
            l.base_travel_time + (delta if i == 0 else 0),
            l.variance_minutes, l.buffer_after, l.cost
        ) for i, l in enumerate(legs)]
        quick = DelayPropagationSimulator(n_simulations=500, random_seed=77)
        r = quick.simulate(mod, departure, deadline)
        return max(0.0, round(base_prob - r.probability_of_success, 1))
