from database import engine, Base, SessionLocal
import models

Base.metadata.create_all(bind=engine)

CITIES = {
    "delhi": {
        "name": "Delhi",
        "lat": 28.6139, "lon": 77.2090,
        "code": "DEL",
        "emoji": "🏛",
        "hubs": {
            "home":            {"name": "Connaught Place",                    "lat": 28.6315, "lon": 77.2167},
            "railway_station": {"name": "New Delhi Railway Station (NDLS)",   "lat": 28.6419, "lon": 77.2195},
            "airport":         {"name": "Indira Gandhi Intl Airport (IGI)",   "lat": 28.5562, "lon": 77.1000},
            "bus_terminal":    {"name": "Kashmere Gate ISBT",                 "lat": 28.6670, "lon": 77.2286},
            "metro_station":   {"name": "Rajiv Chowk Metro Station",          "lat": 28.6328, "lon": 77.2197},
        }
    },
    "lucknow": {
        "name": "Lucknow",
        "lat": 26.8467, "lon": 80.9462,
        "code": "LKO",
        "emoji": "🕌",
        "hubs": {
            "home":            {"name": "Hazratganj",                         "lat": 26.8467, "lon": 80.9462},
            "railway_station": {"name": "Charbagh Railway Station",           "lat": 26.8467, "lon": 80.9148},
            "airport":         {"name": "Chaudhary Charan Singh Airport",     "lat": 26.7606, "lon": 80.8893},
            "bus_terminal":    {"name": "Alambagh Bus Terminal",              "lat": 26.8004, "lon": 80.9014},
            "metro_station":   {"name": "Hazratganj Metro Station",           "lat": 26.8467, "lon": 80.9462},
        }
    },
    "chandigarh": {
        "name": "Chandigarh",
        "lat": 30.7333, "lon": 76.7794,
        "code": "IXC",
        "emoji": "🌿",
        "hubs": {
            "home":            {"name": "Sector 17 Plaza",                    "lat": 30.7417, "lon": 76.7882},
            "railway_station": {"name": "Chandigarh Railway Station",         "lat": 30.7090, "lon": 76.8020},
            "airport":         {"name": "Chandigarh International Airport",   "lat": 30.6735, "lon": 76.7885},
            "bus_terminal":    {"name": "ISBT Sector 43",                    "lat": 30.7074, "lon": 76.7908},
            "metro_station":   {"name": "N/A — No Metro (Cab/Bus feeder)",   "lat": 30.7333, "lon": 76.7794},
        }
    },
    "jaipur": {
        "name": "Jaipur",
        "lat": 26.9124, "lon": 75.7873,
        "code": "JAI",
        "emoji": "🏰",
        "hubs": {
            "home":            {"name": "MI Road / City Center",              "lat": 26.9199, "lon": 75.8162},
            "railway_station": {"name": "Jaipur Junction Railway Station",    "lat": 26.9215, "lon": 75.7873},
            "airport":         {"name": "Jaipur International Airport (JAI)", "lat": 26.8242, "lon": 75.8122},
            "bus_terminal":    {"name": "Sindhi Camp Bus Stand",              "lat": 26.9185, "lon": 75.7970},
            "metro_station":   {"name": "Chandpole Metro Station",            "lat": 26.9228, "lon": 75.8078},
        }
    },
    "pune": {
        "name": "Pune",
        "lat": 18.5204, "lon": 73.8567,
        "code": "PNQ",
        "emoji": "🎓",
        "hubs": {
            "home":            {"name": "Shivajinagar / FC Road",             "lat": 18.5314, "lon": 73.8446},
            "railway_station": {"name": "Pune Junction Railway Station",      "lat": 18.5279, "lon": 73.8742},
            "airport":         {"name": "Pune Airport (PNQ)",                 "lat": 18.5822, "lon": 73.9197},
            "bus_terminal":    {"name": "Swargate Bus Terminal",              "lat": 18.5018, "lon": 73.8636},
            "metro_station":   {"name": "Shivajinagar Metro Station",         "lat": 18.5314, "lon": 73.8446},
        }
    },
    "shimla": {
        "name": "Shimla",
        "lat": 31.1048, "lon": 77.1734,
        "code": "SLV",
        "emoji": "🏔",
        "hubs": {
            "home":            {"name": "The Mall Road",                      "lat": 31.1048, "lon": 77.1734},
            "railway_station": {"name": "Shimla Railway Station (NMR)",       "lat": 31.1041, "lon": 77.1670},
            "airport":         {"name": "Shimla Airport (Jubbarhatti)",       "lat": 31.0818, "lon": 77.0674},
            "bus_terminal":    {"name": "Shimla ISBT (Tutikandi)",            "lat": 31.0913, "lon": 77.1398},
            "metro_station":   {"name": "N/A — No Metro (Cab/Bus feeder)",   "lat": 31.1048, "lon": 77.1734},
        }
    },
}


TRANSPORT_MODES = {
    "metro": {
        "name": "Metro",
        "icon": "🚇",
        "color": "#3b82f6",
        "avg_speed_kmph": 35,
        "base_cost_per_km": 2.5,
        "variance_factor": 0.18,
        "fixed_variance": 7,
        "notes": "Signal-controlled; very consistent"
    },
    "cab": {
        "name": "Cab",
        "icon": "🚕",
        "color": "#f59e0b",
        "avg_speed_kmph": 28,
        "base_cost_per_km": 14,
        "variance_factor": 0.35,
        "fixed_variance": 12,
        "notes": "Traffic-sensitive; Ola/Uber pricing"
    },
    "auto": {
        "name": "Auto Rickshaw",
        "icon": "🛺",
        "color": "#10b981",
        "avg_speed_kmph": 22,
        "base_cost_per_km": 10,
        "variance_factor": 0.30,
        "fixed_variance": 8,
        "notes": "Urban short-distance; moderate variance"
    },
    "dtc_bus": {
        "name": "City Bus",
        "icon": "🚌",
        "color": "#8b5cf6",
        "avg_speed_kmph": 20,
        "base_cost_per_km": 1.5,
        "variance_factor": 0.30,
        "fixed_variance": 12,
        "notes": "City buses; traffic + stop delays"
    },
    "express_train": {
        "name": "Express Train",
        "icon": "🚄",
        "color": "#06b6d4",
        "avg_speed_kmph": 90,
        "base_cost_per_km": 1.8,
        "variance_factor": 0.08,
        "fixed_variance": 15,
        "notes": "Shatabdi/Rajdhani class; fewer stops"
    },
    "mail_train": {
        "name": "Mail/Express Train",
        "icon": "🚂",
        "color": "#64748b",
        "avg_speed_kmph": 65,
        "base_cost_per_km": 1.2,
        "variance_factor": 0.12,
        "fixed_variance": 20,
        "notes": "Regular express; crossing waits"
    },
    "flight": {
        "name": "Flight",
        "icon": "✈️",
        "color": "#ef4444",
        "avg_speed_kmph": 750,
        "base_cost_per_km": 6.5,
        "variance_factor": 0.22,
        "fixed_variance": 18,
        "notes": "ATC, boarding, taxi-queue uncertainty"
    },
    "intercity_bus": {
        "name": "Intercity Bus",
        "icon": "🚎",
        "color": "#d97706",
        "avg_speed_kmph": 55,
        "base_cost_per_km": 1.0,
        "variance_factor": 0.14,
        "fixed_variance": 25,
        "notes": "NH traffic, rest stops, driver changeovers"
    },
    "volvo_bus": {
        "name": "Volvo/AC Bus",
        "icon": "🚐",
        "color": "#7c3aed",
        "avg_speed_kmph": 65,
        "base_cost_per_km": 1.6,
        "variance_factor": 0.12,
        "fixed_variance": 20,
        "notes": "Premium intercity AC bus"
    },
    "toy_train": {
        "name": "Toy Train (NMR)",
        "icon": "🚞",
        "color": "#16a34a",
        "avg_speed_kmph": 20,
        "base_cost_per_km": 3.5,
        "variance_factor": 0.10,
        "fixed_variance": 15,
        "notes": "Narrow-gauge heritage railway Kalka–Shimla; scenic but slow"
    },
    "hrtc_bus": {
        "name": "HRTC Bus",
        "icon": "🚍",
        "color": "#dc2626",
        "avg_speed_kmph": 40,
        "base_cost_per_km": 1.1,
        "variance_factor": 0.20,
        "fixed_variance": 30,
        "notes": "Hill-route state bus; mountain roads, hairpin bends"
    },
}


ROUTES = {

    # ==================== DELHI ↔ OTHERS ====================

    ("delhi", "lucknow"): {
        "distance_km": 556,
        "fastest": {
            "name": "Fastest", "icon": "⚡",
            "description": "Metro to IGI + Flight + Cab — 3.5-4 hr total including transfers",
            "legs": [
                {"mode": "metro",   "from": "delhi.home",      "to": "delhi.airport",      "base_time": 45,  "variance": 9,  "buffer": 15, "cost": 60},
                {"mode": "flight",  "from": "delhi.airport",   "to": "lucknow.airport",    "base_time": 65,  "variance": 20, "buffer": 20, "cost": 4200},
                {"mode": "cab",     "from": "lucknow.airport", "to": "lucknow.home",       "base_time": 35,  "variance": 12, "buffer": 0,  "cost": 350},
            ]
        },
        "cheapest": {
            "name": "Cheapest", "icon": "💰",
            "description": "City bus to ISBT + Overnight intercity bus — lowest cost option",
            "legs": [
                {"mode": "dtc_bus",       "from": "delhi.home",          "to": "delhi.bus_terminal",    "base_time": 50,  "variance": 14, "buffer": 20, "cost": 25},
                {"mode": "intercity_bus", "from": "delhi.bus_terminal",  "to": "lucknow.bus_terminal",  "base_time": 480, "variance": 55, "buffer": 15, "cost": 450},
                {"mode": "auto",          "from": "lucknow.bus_terminal","to": "lucknow.home",          "base_time": 25,  "variance": 9,  "buffer": 0,  "cost": 120},
            ]
        },
        "reliable": {
            "name": "Most Reliable", "icon": "🛡",
            "description": "Metro + Shatabdi Express + Metro — best on-time record for this corridor",
            "legs": [
                {"mode": "metro",         "from": "delhi.home",           "to": "delhi.railway_station",  "base_time": 20,  "variance": 7,  "buffer": 30, "cost": 30},
                {"mode": "express_train", "from": "delhi.railway_station","to": "lucknow.railway_station", "base_time": 390, "variance": 25, "buffer": 25, "cost": 650},
                {"mode": "metro",         "from": "lucknow.metro_station","to": "lucknow.home",            "base_time": 12,  "variance": 5,  "buffer": 0,  "cost": 20},
            ]
        }
    },

    ("delhi", "chandigarh"): {
        "distance_km": 250,
        "fastest": {
            "name": "Fastest", "icon": "⚡",
            "description": "Volvo AC Bus via NH-44 — faster than train with less transfer overhead",
            "legs": [
                {"mode": "cab",       "from": "delhi.home",            "to": "delhi.bus_terminal",        "base_time": 35,  "variance": 14, "buffer": 15, "cost": 280},
                {"mode": "volvo_bus", "from": "delhi.bus_terminal",    "to": "chandigarh.bus_terminal",   "base_time": 240, "variance": 28, "buffer": 10, "cost": 600},
                {"mode": "cab",       "from": "chandigarh.bus_terminal","to": "chandigarh.home",          "base_time": 20,  "variance": 8,  "buffer": 0,  "cost": 200},
            ]
        },
        "cheapest": {
            "name": "Cheapest", "icon": "💰",
            "description": "City bus + Intercity bus — most affordable NH-44 corridor option",
            "legs": [
                {"mode": "dtc_bus",       "from": "delhi.home",            "to": "delhi.bus_terminal",        "base_time": 50,  "variance": 14, "buffer": 20, "cost": 25},
                {"mode": "intercity_bus", "from": "delhi.bus_terminal",    "to": "chandigarh.bus_terminal",   "base_time": 270, "variance": 32, "buffer": 15, "cost": 320},
                {"mode": "auto",          "from": "chandigarh.bus_terminal","to": "chandigarh.home",          "base_time": 18,  "variance": 7,  "buffer": 0,  "cost": 100},
            ]
        },
        "reliable": {
            "name": "Most Reliable", "icon": "🛡",
            "description": "Metro + Shatabdi Express — fixed departure, good punctuality on this route",
            "legs": [
                {"mode": "metro",         "from": "delhi.home",           "to": "delhi.railway_station",       "base_time": 20,  "variance": 7,  "buffer": 30, "cost": 30},
                {"mode": "express_train", "from": "delhi.railway_station","to": "chandigarh.railway_station",  "base_time": 210, "variance": 18, "buffer": 20, "cost": 520},
                {"mode": "cab",           "from": "chandigarh.railway_station","to": "chandigarh.home",        "base_time": 18,  "variance": 7,  "buffer": 0,  "cost": 180},
            ]
        }
    },

    ("delhi", "jaipur"): {
        "distance_km": 270,
        "fastest": {
            "name": "Fastest", "icon": "⚡",
            "description": "Cab via NH-48 (Jaipur Expressway) — no terminal overhead, direct city-to-city",
            "legs": [
                {"mode": "cab", "from": "delhi.home", "to": "jaipur.home",
                 "base_time": 270, "variance": 38, "buffer": 0, "cost": 3200},
            ]
        },
        "cheapest": {
            "name": "Cheapest", "icon": "💰",
            "description": "City bus + Rajasthan Roadways — cheapest on this short-to-medium corridor",
            "legs": [
                {"mode": "dtc_bus",       "from": "delhi.home",          "to": "delhi.bus_terminal",   "base_time": 50,  "variance": 14, "buffer": 20, "cost": 25},
                {"mode": "intercity_bus", "from": "delhi.bus_terminal",  "to": "jaipur.bus_terminal",  "base_time": 300, "variance": 38, "buffer": 10, "cost": 280},
                {"mode": "auto",          "from": "jaipur.bus_terminal", "to": "jaipur.home",          "base_time": 20,  "variance": 8,  "buffer": 0,  "cost": 80},
            ]
        },
        "reliable": {
            "name": "Most Reliable", "icon": "🛡",
            "description": "Metro + Shatabdi/Intercity Express — structured schedule with high punctuality",
            "legs": [
                {"mode": "metro",         "from": "delhi.home",           "to": "delhi.railway_station",  "base_time": 20,  "variance": 7,  "buffer": 30, "cost": 30},
                {"mode": "express_train", "from": "delhi.railway_station","to": "jaipur.railway_station",  "base_time": 270, "variance": 20, "buffer": 20, "cost": 480},
                {"mode": "cab",           "from": "jaipur.railway_station","to": "jaipur.home",            "base_time": 12,  "variance": 6,  "buffer": 0,  "cost": 120},
            ]
        }
    },

    ("delhi", "pune"): {
        "distance_km": 1408,
        "fastest": {
            "name": "Fastest", "icon": "⚡",
            "description": "Metro + Flight + Cab — only practical fast option for this 1400 km corridor",
            "legs": [
                {"mode": "metro",  "from": "delhi.home",    "to": "delhi.airport",  "base_time": 45,  "variance": 9,  "buffer": 15, "cost": 60},
                {"mode": "flight", "from": "delhi.airport", "to": "pune.airport",   "base_time": 120, "variance": 25, "buffer": 25, "cost": 5500},
                {"mode": "cab",    "from": "pune.airport",  "to": "pune.home",      "base_time": 30,  "variance": 14, "buffer": 0,  "cost": 450},
            ]
        },
        "cheapest": {
            "name": "Cheapest", "icon": "💰",
            "description": "Metro + Mail/Express Train — long but most economical for 1400 km",
            "legs": [
                {"mode": "metro",      "from": "delhi.home",           "to": "delhi.railway_station",  "base_time": 20,   "variance": 7,  "buffer": 30, "cost": 30},
                {"mode": "mail_train", "from": "delhi.railway_station","to": "pune.railway_station",   "base_time": 1380, "variance": 80, "buffer": 30, "cost": 1200},
                {"mode": "metro",      "from": "pune.railway_station", "to": "pune.home",              "base_time": 20,   "variance": 10, "buffer": 0,  "cost": 30},
            ]
        },
        "reliable": {
            "name": "Most Reliable", "icon": "🛡",
            "description": "Metro + Flight + Cab — flight is most reliable for long haul; generous airport buffers",
            "legs": [
                {"mode": "metro",  "from": "delhi.home",    "to": "delhi.airport",  "base_time": 45,  "variance": 9,  "buffer": 20, "cost": 60},
                {"mode": "flight", "from": "delhi.airport", "to": "pune.airport",   "base_time": 120, "variance": 22, "buffer": 25, "cost": 5800},
                {"mode": "cab",    "from": "pune.airport",  "to": "pune.home",      "base_time": 30,  "variance": 14, "buffer": 0,  "cost": 450},
            ]
        }
    },

    ("delhi", "shimla"): {
        "distance_km": 350,
        "fastest": {
            "name": "Fastest", "icon": "⚡",
            "description": "Metro + Flight to Chandigarh + Cab uphill — ~5.5 hr door-to-door",
            "legs": [
                {"mode": "metro",  "from": "delhi.home",          "to": "delhi.airport",          "base_time": 45,  "variance": 9,  "buffer": 20, "cost": 60},
                {"mode": "flight", "from": "delhi.airport",       "to": "chandigarh.airport",     "base_time": 60,  "variance": 20, "buffer": 20, "cost": 3500},
                {"mode": "cab",    "from": "chandigarh.airport",  "to": "shimla.home",            "base_time": 210, "variance": 55, "buffer": 0,  "cost": 2500},
            ]
        },
        "cheapest": {
            "name": "Cheapest", "icon": "💰",
            "description": "ISBT bus (Delhi-Shimla direct HRTC/HPRTC overnight) — cheapest option",
            "legs": [
                {"mode": "dtc_bus",       "from": "delhi.home",         "to": "delhi.bus_terminal",   "base_time": 50,  "variance": 14, "buffer": 20, "cost": 25},
                {"mode": "hrtc_bus",      "from": "delhi.bus_terminal", "to": "shimla.bus_terminal",  "base_time": 540, "variance": 90, "buffer": 20, "cost": 500},
                {"mode": "auto",          "from": "shimla.bus_terminal","to": "shimla.home",          "base_time": 15,  "variance": 7,  "buffer": 0,  "cost": 100},
            ]
        },
        "reliable": {
            "name": "Most Reliable", "icon": "🛡",
            "description": "Metro + Kalka Shatabdi + Toy Train — most structured timing despite long duration",
            "legs": [
                {"mode": "metro",         "from": "delhi.home",           "to": "delhi.railway_station",   "base_time": 30,  "variance": 10, "buffer": 30, "cost": 40},
                {"mode": "express_train", "from": "delhi.railway_station","to": "chandigarh.railway_station","base_time": 210, "variance": 18, "buffer": 30, "cost": 520},
                {"mode": "toy_train",     "from": "chandigarh.railway_station","to": "shimla.railway_station","base_time": 330, "variance": 35, "buffer": 0,  "cost": 500},
            ]
        }
    },

    # ==================== CHANDIGARH ↔ OTHERS ====================

    ("chandigarh", "lucknow"): {
        "distance_km": 600,
        "fastest": {
            "name": "Fastest", "icon": "⚡",
            "description": "Cab + Flight via Delhi + Cab — no direct CHD–LKO flight; 1-stop via IGI",
            "legs": [
                {"mode": "cab",    "from": "chandigarh.home",    "to": "chandigarh.airport", "base_time": 28,  "variance": 10, "buffer": 20, "cost": 280},
                {"mode": "flight", "from": "chandigarh.airport", "to": "delhi.airport",      "base_time": 55,  "variance": 18, "buffer": 60, "cost": 2800},
                {"mode": "flight", "from": "delhi.airport",      "to": "lucknow.airport",    "base_time": 65,  "variance": 20, "buffer": 15, "cost": 3200},
                {"mode": "cab",    "from": "lucknow.airport",    "to": "lucknow.home",       "base_time": 35,  "variance": 12, "buffer": 0,  "cost": 350},
            ]
        },
        "cheapest": {
            "name": "Cheapest", "icon": "💰",
            "description": "Auto + Overnight intercity bus (direct Chandigarh–Lucknow) — lowest cost",
            "legs": [
                {"mode": "auto",          "from": "chandigarh.home",         "to": "chandigarh.bus_terminal", "base_time": 20,  "variance": 7,  "buffer": 20, "cost": 100},
                {"mode": "intercity_bus", "from": "chandigarh.bus_terminal", "to": "lucknow.bus_terminal",    "base_time": 600, "variance": 70, "buffer": 15, "cost": 650},
                {"mode": "auto",          "from": "lucknow.bus_terminal",    "to": "lucknow.home",            "base_time": 25,  "variance": 9,  "buffer": 0,  "cost": 120},
            ]
        },
        "reliable": {
            "name": "Most Reliable", "icon": "🛡",
            "description": "Cab + Express Train (Chandigarh–Lucknow Express) — direct rail, structured schedule",
            "legs": [
                {"mode": "cab",           "from": "chandigarh.home",          "to": "chandigarh.railway_station", "base_time": 20,  "variance": 8,  "buffer": 35, "cost": 180},
                {"mode": "express_train", "from": "chandigarh.railway_station","to": "lucknow.railway_station",    "base_time": 600, "variance": 40, "buffer": 20, "cost": 720},
                {"mode": "auto",          "from": "lucknow.railway_station",  "to": "lucknow.home",               "base_time": 20,  "variance": 8,  "buffer": 0,  "cost": 80},
            ]
        }
    },


    ("chandigarh", "delhi"): {
    "distance_km": 250,

    "fastest": {
        "name": "Fastest", "icon": "⚡",
        "description": "Direct cab via NH-44 — fastest door-to-door option (~4–5 hrs)",
        "legs": [
            {"mode": "cab", "from": "chandigarh.home", "to": "delhi.home", "base_time": 270, "variance": 40, "buffer": 0, "cost": 2800},
        ]
    },

    "cheapest": {
        "name": "Cheapest", "icon": "💰",
        "description": "Bus via ISBT — cheapest intercity option",
        "legs": [
            {"mode": "auto", "from": "chandigarh.home", "to": "chandigarh.bus_terminal", "base_time": 15, "variance": 5, "buffer": 15, "cost": 80},
            {"mode": "intercity_bus", "from": "chandigarh.bus_terminal", "to": "delhi.bus_terminal", "base_time": 360, "variance": 60, "buffer": 20, "cost": 400},
            {"mode": "auto", "from": "delhi.bus_terminal", "to": "delhi.home", "base_time": 25, "variance": 10, "buffer": 0, "cost": 120},
        ]
    },

    "reliable": {
        "name": "Most Reliable", "icon": "🛡️",
        "description": "Cab to station + Shatabdi Express — highly punctual and structured",
        "legs": [
            {"mode": "cab", "from": "chandigarh.home", "to": "chandigarh.railway_station", "base_time": 25, "variance": 8, "buffer": 25, "cost": 200},
            {"mode": "express_train", "from": "chandigarh.railway_station", "to": "delhi.railway_station", "base_time": 210, "variance": 15, "buffer": 20, "cost": 600},
            {"mode": "metro", "from": "delhi.railway_station", "to": "delhi.home", "base_time": 30, "variance": 8, "buffer": 0, "cost": 60},
        ]
    }
},

    ("chandigarh", "jaipur"): {
        "distance_km": 540,
        "fastest": {
            "name": "Fastest", "icon": "⚡",
            "description": "Volvo AC Bus via NH-48 — direct overnight/daytime, beats train+metro overhead",
            "legs": [
                {"mode": "cab",       "from": "chandigarh.home",        "to": "chandigarh.bus_terminal", "base_time": 22,  "variance": 8,  "buffer": 15, "cost": 200},
                {"mode": "volvo_bus", "from": "chandigarh.bus_terminal","to": "jaipur.bus_terminal",     "base_time": 480, "variance": 50, "buffer": 10, "cost": 800},
                {"mode": "cab",       "from": "jaipur.bus_terminal",    "to": "jaipur.home",             "base_time": 15,  "variance": 7,  "buffer": 0,  "cost": 120},
            ]
        },
        "cheapest": {
            "name": "Cheapest", "icon": "💰",
            "description": "Auto + State roadways bus (Chandigarh to Jaipur) — cheapest direct intercity option",
            "legs": [
                {"mode": "auto",          "from": "chandigarh.home",        "to": "chandigarh.bus_terminal", "base_time": 20,  "variance": 7,  "buffer": 20, "cost": 100},
                {"mode": "intercity_bus", "from": "chandigarh.bus_terminal","to": "jaipur.bus_terminal",     "base_time": 510, "variance": 55, "buffer": 15, "cost": 550},
                {"mode": "auto",          "from": "jaipur.bus_terminal",    "to": "jaipur.home",             "base_time": 15,  "variance": 7,  "buffer": 0,  "cost": 80},
            ]
        },
        "reliable": {
            "name": "Most Reliable", "icon": "🛡",
            "description": "Cab + Express Train (via Delhi) — train is most predictable despite longer routing",
            "legs": [
                {"mode": "cab",           "from": "chandigarh.home",           "to": "chandigarh.railway_station", "base_time": 20,  "variance": 8,  "buffer": 35, "cost": 180},
                {"mode": "express_train", "from": "chandigarh.railway_station","to": "jaipur.railway_station",     "base_time": 720, "variance": 45, "buffer": 25, "cost": 860},
                {"mode": "cab",           "from": "jaipur.railway_station",    "to": "jaipur.home",                "base_time": 12,  "variance": 6,  "buffer": 0,  "cost": 120},
            ]
        }
    },

    ("chandigarh", "pune"): {
        "distance_km": 1650,
        "fastest": {
            "name": "Fastest", "icon": "⚡",
            "description": "Cab + Flight (1-stop via Delhi or Mumbai) + Cab — only practical option",
            "legs": [
                {"mode": "cab",    "from": "chandigarh.home",    "to": "chandigarh.airport", "base_time": 28,  "variance": 10, "buffer": 20, "cost": 280},
                {"mode": "flight", "from": "chandigarh.airport", "to": "pune.airport",       "base_time": 155, "variance": 28, "buffer": 20, "cost": 6200},
                {"mode": "cab",    "from": "pune.airport",       "to": "pune.home",          "base_time": 30,  "variance": 14, "buffer": 0,  "cost": 450},
            ]
        },
        "cheapest": {
            "name": "Cheapest", "icon": "💰",
            "description": "Cab + Long-distance train (via Delhi) — slow but very affordable for 1650 km",
            "legs": [
                {"mode": "cab",        "from": "chandigarh.home",           "to": "chandigarh.railway_station", "base_time": 20,   "variance": 8,  "buffer": 35, "cost": 180},
                {"mode": "mail_train", "from": "chandigarh.railway_station","to": "pune.railway_station",       "base_time": 1680, "variance": 95, "buffer": 30, "cost": 1400},
                {"mode": "metro",      "from": "pune.railway_station",      "to": "pune.home",                  "base_time": 20,   "variance": 10, "buffer": 0,  "cost": 30},
            ]
        },
        "reliable": {
            "name": "Most Reliable", "icon": "🛡",
            "description": "Cab + Flight + Cab — only reliable option for 1650 km; train variance is prohibitively high",
            "legs": [
                {"mode": "cab",    "from": "chandigarh.home",    "to": "chandigarh.airport", "base_time": 28,  "variance": 10, "buffer": 20, "cost": 280},
                {"mode": "flight", "from": "chandigarh.airport", "to": "pune.airport",       "base_time": 155, "variance": 25, "buffer": 25, "cost": 6500},
                {"mode": "cab",    "from": "pune.airport",       "to": "pune.home",          "base_time": 30,  "variance": 14, "buffer": 0,  "cost": 450},
            ]
        }
    },

    ("chandigarh", "shimla"): {
        "distance_km": 115,
        "fastest": {
            "name": "Fastest", "icon": "⚡",
            "description": "Direct cab uphill via NH-5 — fastest door-to-door for this short route",
            "legs": [
                {"mode": "cab", "from": "chandigarh.home", "to": "shimla.home",
                 "base_time": 180, "variance": 50, "buffer": 0, "cost": 2200},
            ]
        },
        "cheapest": {
            "name": "Cheapest", "icon": "💰",
            "description": "HRTC Bus (Chandigarh ISBT to Shimla ISBT) — cheapest hill route option",
            "legs": [
                {"mode": "auto",     "from": "chandigarh.home",        "to": "chandigarh.bus_terminal", "base_time": 18,  "variance": 7,  "buffer": 15, "cost": 100},
                {"mode": "hrtc_bus", "from": "chandigarh.bus_terminal","to": "shimla.bus_terminal",     "base_time": 240, "variance": 60, "buffer": 10, "cost": 300},
                {"mode": "auto",     "from": "shimla.bus_terminal",    "to": "shimla.home",             "base_time": 15,  "variance": 7,  "buffer": 0,  "cost": 100},
            ]
        },
        "reliable": {
            "name": "Most Reliable", "icon": "🛡",
            "description": "Cab to Kalka + Toy Train — scenic and structured; NMR rarely cancels",
            "legs": [
                {"mode": "cab",       "from": "chandigarh.home",          "to": "chandigarh.railway_station", "base_time": 45,  "variance": 12, "buffer": 20, "cost": 400},
                {"mode": "toy_train", "from": "chandigarh.railway_station","to": "shimla.railway_station",     "base_time": 330, "variance": 35, "buffer": 0,  "cost": 500},
            ]
        }
    },

    # ==================== JAIPUR ↔ OTHERS ====================

    ("jaipur", "lucknow"): {
        "distance_km": 630,
        "fastest": {
            "name": "Fastest", "icon": "⚡",
            "description": "Cab + Direct flight (Jaipur–Lucknow, limited frequency) + Cab",
            "legs": [
                {"mode": "cab",    "from": "jaipur.home",    "to": "jaipur.airport",  "base_time": 30,  "variance": 10, "buffer": 20, "cost": 300},
                {"mode": "flight", "from": "jaipur.airport", "to": "lucknow.airport", "base_time": 80,  "variance": 22, "buffer": 20, "cost": 4500},
                {"mode": "cab",    "from": "lucknow.airport","to": "lucknow.home",    "base_time": 35,  "variance": 12, "buffer": 0,  "cost": 350},
            ]
        },
        "cheapest": {
            "name": "Cheapest", "icon": "💰",
            "description": "Auto + Mail/Express train (Marudhara/Sarayu Express) — direct JAI–LKO route, good value",
            "legs": [
                {"mode": "auto",       "from": "jaipur.home",           "to": "jaipur.railway_station",  "base_time": 12,  "variance": 6,  "buffer": 35, "cost": 80},
                {"mode": "mail_train", "from": "jaipur.railway_station","to": "lucknow.railway_station",  "base_time": 600, "variance": 55, "buffer": 20, "cost": 580},
                {"mode": "auto",       "from": "lucknow.railway_station","to": "lucknow.home",            "base_time": 20,  "variance": 8,  "buffer": 0,  "cost": 80},
            ]
        },
        "reliable": {
            "name": "Most Reliable", "icon": "🛡",
            "description": "Auto + Express train with extra buffer — more reliable schedule than mail train",
            "legs": [
                {"mode": "auto",          "from": "jaipur.home",           "to": "jaipur.railway_station",  "base_time": 12,  "variance": 6,  "buffer": 35, "cost": 80},
                {"mode": "express_train", "from": "jaipur.railway_station","to": "lucknow.railway_station",  "base_time": 560, "variance": 38, "buffer": 25, "cost": 780},
                {"mode": "cab",           "from": "lucknow.railway_station","to": "lucknow.home",            "base_time": 20,  "variance": 8,  "buffer": 0,  "cost": 120},
            ]
        }
    },

    ("jaipur", "pune"): {
        "distance_km": 1150,
        "fastest": {
            "name": "Fastest", "icon": "⚡",
            "description": "Metro + Direct flight (Jaipur–Pune IndiGo) + Cab — ~4.5 hr door-to-door",
            "legs": [
                {"mode": "metro",  "from": "jaipur.home",    "to": "jaipur.airport",  "base_time": 28,  "variance": 7,  "buffer": 15, "cost": 35},
                {"mode": "flight", "from": "jaipur.airport", "to": "pune.airport",    "base_time": 95,  "variance": 22, "buffer": 20, "cost": 4800},
                {"mode": "cab",    "from": "pune.airport",   "to": "pune.home",       "base_time": 30,  "variance": 14, "buffer": 0,  "cost": 450},
            ]
        },
        "cheapest": {
            "name": "Cheapest", "icon": "💰",
            "description": "Cab + Mail/Express train (Jaipur–Pune Express) — long but affordable",
            "legs": [
                {"mode": "cab",        "from": "jaipur.home",          "to": "jaipur.railway_station",  "base_time": 12,  "variance": 6,  "buffer": 35, "cost": 120},
                {"mode": "mail_train", "from": "jaipur.railway_station","to": "pune.railway_station",    "base_time": 960, "variance": 65, "buffer": 25, "cost": 900},
                {"mode": "metro",      "from": "pune.railway_station", "to": "pune.home",               "base_time": 20,  "variance": 10, "buffer": 0,  "cost": 30},
            ]
        },
        "reliable": {
            "name": "Most Reliable", "icon": "🛡",
            "description": "Metro + Flight + Cab — most reliable for 1150 km; extra airport buffer reduces risk",
            "legs": [
                {"mode": "metro",  "from": "jaipur.home",    "to": "jaipur.airport",  "base_time": 28,  "variance": 7,  "buffer": 20, "cost": 35},
                {"mode": "flight", "from": "jaipur.airport", "to": "pune.airport",    "base_time": 95,  "variance": 20, "buffer": 25, "cost": 5100},
                {"mode": "cab",    "from": "pune.airport",   "to": "pune.home",       "base_time": 30,  "variance": 14, "buffer": 0,  "cost": 450},
            ]
        }
    },

    ("jaipur", "shimla"): {
        "distance_km": 600,
        "fastest": {
            "name": "Fastest", "icon": "⚡",
            "description": "Cab + Flight via Chandigarh + Cab uphill — ~6 hr door-to-door",
            "legs": [
                {"mode": "cab",    "from": "jaipur.home",        "to": "jaipur.airport",      "base_time": 30,  "variance": 10, "buffer": 20, "cost": 300},
                {"mode": "flight", "from": "jaipur.airport",     "to": "chandigarh.airport",  "base_time": 90,  "variance": 25, "buffer": 20, "cost": 4500},
                {"mode": "cab",    "from": "chandigarh.airport", "to": "shimla.home",         "base_time": 210, "variance": 55, "buffer": 0,  "cost": 2500},
            ]
        },
        "cheapest": {
            "name": "Cheapest", "icon": "💰",
            "description": "Intercity bus to Delhi + HRTC bus to Shimla — cheapest multi-leg option",
            "legs": [
                {"mode": "intercity_bus", "from": "jaipur.bus_terminal", "to": "delhi.bus_terminal",  "base_time": 300, "variance": 40, "buffer": 15, "cost": 350},
                {"mode": "hrtc_bus",      "from": "delhi.bus_terminal",  "to": "shimla.bus_terminal", "base_time": 540, "variance": 90, "buffer": 15, "cost": 500},
                {"mode": "auto",          "from": "shimla.bus_terminal", "to": "shimla.home",         "base_time": 15,  "variance": 7,  "buffer": 0,  "cost": 100},
            ]
        },
        "reliable": {
            "name": "Most Reliable", "icon": "🛡",
            "description": "Train via Delhi + Kalka Shatabdi + Toy Train — structured schedule, predictable legs",
            "legs": [
                {"mode": "cab",           "from": "jaipur.home",           "to": "jaipur.railway_station",    "base_time": 12,  "variance": 6,  "buffer": 35, "cost": 120},
                {"mode": "express_train", "from": "jaipur.railway_station","to": "delhi.railway_station",      "base_time": 270, "variance": 20, "buffer": 30, "cost": 480},
                {"mode": "express_train", "from": "delhi.railway_station", "to": "chandigarh.railway_station", "base_time": 210, "variance": 18, "buffer": 20, "cost": 520},
                {"mode": "toy_train",     "from": "chandigarh.railway_station","to": "shimla.railway_station", "base_time": 330, "variance": 35, "buffer": 0,  "cost": 500},
            ]
        }
    },
 
 ("jaipur", "delhi"): {
    "distance_km": 270,

    "fastest": {
        "name": "Fastest", "icon": "⚡",
        "description": "Direct cab via NH-48 — fastest door-to-door (~4.5–5 hrs)",
        "legs": [
            {"mode": "cab", "from": "jaipur.home", "to": "delhi.home", "base_time": 300, "variance": 45, "buffer": 0, "cost": 3000},
        ]
    },

    "cheapest": {
        "name": "Cheapest", "icon": "💰",
        "description": "Intercity bus — economical option for Jaipur to Delhi",
        "legs": [
            {"mode": "auto", "from": "jaipur.home", "to": "jaipur.bus_terminal", "base_time": 20, "variance": 8, "buffer": 20, "cost": 80},
            {"mode": "intercity_bus", "from": "jaipur.bus_terminal", "to": "delhi.bus_terminal", "base_time": 360, "variance": 60, "buffer": 20, "cost": 400},
            {"mode": "auto", "from": "delhi.bus_terminal", "to": "delhi.home", "base_time": 25, "variance": 10, "buffer": 0, "cost": 120},
        ]
    },

    "reliable": {
        "name": "Most Reliable", "icon": "🛡️",
        "description": "Cab + Express train — structured and dependable timing",
        "legs": [
            {"mode": "cab", "from": "jaipur.home", "to": "jaipur.railway_station", "base_time": 25, "variance": 8, "buffer": 25, "cost": 200},
            {"mode": "express_train", "from": "jaipur.railway_station", "to": "delhi.railway_station", "base_time": 270, "variance": 18, "buffer": 20, "cost": 600},
            {"mode": "metro", "from": "delhi.railway_station", "to": "delhi.home", "base_time": 30, "variance": 8, "buffer": 0, "cost": 60},
        ]
    }
},

 ("jaipur", "chandigarh"): {
    "distance_km": 540,

    "fastest": {
        "name": "Fastest", "icon": "⚡",
        "description": "Cab + flight (Jaipur → Chandigarh via Delhi) — fastest multi-leg (~4–5 hrs)",
        "legs": [
            {"mode": "cab", "from": "jaipur.home", "to": "jaipur.airport", "base_time": 30, "variance": 10, "buffer": 25, "cost": 250},
            {"mode": "flight", "from": "jaipur.airport", "to": "chandigarh.airport", "base_time": 90, "variance": 25, "buffer": 25, "cost": 4500},
            {"mode": "cab", "from": "chandigarh.airport", "to": "chandigarh.home", "base_time": 30, "variance": 10, "buffer": 0, "cost": 300},
        ]
    },

    "cheapest": {
        "name": "Cheapest", "icon": "💰",
        "description": "Bus via Delhi — most economical long-distance option",
        "legs": [
            {"mode": "auto", "from": "jaipur.home", "to": "jaipur.bus_terminal", "base_time": 20, "variance": 8, "buffer": 20, "cost": 80},
            {"mode": "intercity_bus", "from": "jaipur.bus_terminal", "to": "delhi.bus_terminal", "base_time": 360, "variance": 60, "buffer": 20, "cost": 400},
            {"mode": "intercity_bus", "from": "delhi.bus_terminal", "to": "chandigarh.bus_terminal", "base_time": 300, "variance": 50, "buffer": 20, "cost": 350},
            {"mode": "auto", "from": "chandigarh.bus_terminal", "to": "chandigarh.home", "base_time": 20, "variance": 7, "buffer": 0, "cost": 100},
        ]
    },

    "reliable": {
        "name": "Most Reliable", "icon": "🛡️",
        "description": "Cab + train via Delhi — structured and predictable timing",
        "legs": [
            {"mode": "cab", "from": "jaipur.home", "to": "jaipur.railway_station", "base_time": 25, "variance": 8, "buffer": 25, "cost": 200},
            {"mode": "express_train", "from": "jaipur.railway_station", "to": "delhi.railway_station", "base_time": 270, "variance": 18, "buffer": 25, "cost": 600},
            {"mode": "express_train", "from": "delhi.railway_station", "to": "chandigarh.railway_station", "base_time": 210, "variance": 15, "buffer": 20, "cost": 500},
            {"mode": "metro", "from": "chandigarh.railway_station", "to": "chandigarh.home", "base_time": 20, "variance": 7, "buffer": 0, "cost": 50},
        ]
    }
},
    # ==================== LUCKNOW ↔ OTHERS ====================

    ("lucknow", "chandigarh"): {
        "distance_km": 600,
        "fastest": {
            "name": "Fastest", "icon": "⚡",
            "description": "Cab + Flight via Delhi + Cab — no direct LKO–CHD flight; 1-stop via IGI",
            "legs": [
                {"mode": "cab",    "from": "lucknow.home",    "to": "lucknow.airport",    "base_time": 40,  "variance": 14, "buffer": 20, "cost": 380},
                {"mode": "flight", "from": "lucknow.airport", "to": "delhi.airport",      "base_time": 65,  "variance": 20, "buffer": 60, "cost": 3200},
                {"mode": "flight", "from": "delhi.airport",   "to": "chandigarh.airport", "base_time": 55,  "variance": 18, "buffer": 15, "cost": 2800},
                {"mode": "cab",    "from": "chandigarh.airport","to": "chandigarh.home",  "base_time": 25,  "variance": 9,  "buffer": 0,  "cost": 220},
            ]
        },
        "cheapest": {
            "name": "Cheapest", "icon": "💰",
            "description": "Auto + Overnight bus (direct Lucknow–Chandigarh) — cheapest option",
            "legs": [
                {"mode": "auto",          "from": "lucknow.home",         "to": "lucknow.bus_terminal",    "base_time": 25,  "variance": 9,  "buffer": 20, "cost": 100},
                {"mode": "intercity_bus", "from": "lucknow.bus_terminal", "to": "chandigarh.bus_terminal", "base_time": 600, "variance": 65, "buffer": 20, "cost": 700},
                {"mode": "auto",          "from": "chandigarh.bus_terminal","to": "chandigarh.home",       "base_time": 18,  "variance": 7,  "buffer": 0,  "cost": 100},
            ]
        },
        "reliable": {
            "name": "Most Reliable", "icon": "🛡",
            "description": "Auto + Express Train (Chandigarh Express) — direct rail, structured schedule",
            "legs": [
                {"mode": "auto",          "from": "lucknow.home",          "to": "lucknow.railway_station",    "base_time": 20,  "variance": 8,  "buffer": 35, "cost": 80},
                {"mode": "express_train", "from": "lucknow.railway_station","to": "chandigarh.railway_station", "base_time": 660, "variance": 40, "buffer": 20, "cost": 750},
                {"mode": "cab",           "from": "chandigarh.railway_station","to": "chandigarh.home",         "base_time": 18,  "variance": 7,  "buffer": 0,  "cost": 180},
            ]
        }
    },

    ("lucknow", "delhi"): {
    "distance_km": 550,

    "fastest": {
        "name": "Fastest", "icon": "⚡",
        "description": "Direct flight (Lucknow → Delhi) + cab — fastest door-to-door (~2.5–3 hrs)",
        "legs": [
            {"mode": "cab", "from": "lucknow.home", "to": "lucknow.airport", "base_time": 35, "variance": 12, "buffer": 25, "cost": 300},
            {"mode": "flight", "from": "lucknow.airport", "to": "delhi.airport", "base_time": 80, "variance": 20, "buffer": 20, "cost": 4500},
            {"mode": "cab", "from": "delhi.airport", "to": "delhi.home", "base_time": 45, "variance": 15, "buffer": 0, "cost": 500},
        ]
    },

    "cheapest": {
        "name": "Cheapest", "icon": "💰",
        "description": "Intercity bus — most economical option for 550 km route",
        "legs": [
            {"mode": "auto", "from": "lucknow.home", "to": "lucknow.bus_terminal", "base_time": 20, "variance": 8, "buffer": 20, "cost": 80},
            {"mode": "intercity_bus", "from": "lucknow.bus_terminal", "to": "delhi.bus_terminal", "base_time": 600, "variance": 90, "buffer": 20, "cost": 500},
            {"mode": "auto", "from": "delhi.bus_terminal", "to": "delhi.home", "base_time": 30, "variance": 10, "buffer": 0, "cost": 120},
        ]
    },

    "reliable": {
        "name": "Most Reliable", "icon": "🛡️",
        "description": "Cab + Shatabdi/Express train — structured and dependable timing",
        "legs": [
            {"mode": "cab", "from": "lucknow.home", "to": "lucknow.railway_station", "base_time": 25, "variance": 8, "buffer": 25, "cost": 200},
            {"mode": "express_train", "from": "lucknow.railway_station", "to": "delhi.railway_station", "base_time": 360, "variance": 20, "buffer": 20, "cost": 700},
            {"mode": "metro", "from": "delhi.railway_station", "to": "delhi.home", "base_time": 35, "variance": 10, "buffer": 0, "cost": 60},
        ]
    }
},

    ("lucknow", "jaipur"): {
        "distance_km": 630,
        "fastest": {
            "name": "Fastest", "icon": "⚡",
            "description": "Cab + Direct flight (Lucknow–Jaipur, limited frequency) + Cab",
            "legs": [
                {"mode": "cab",    "from": "lucknow.home",    "to": "lucknow.airport", "base_time": 40,  "variance": 14, "buffer": 20, "cost": 380},
                {"mode": "flight", "from": "lucknow.airport", "to": "jaipur.airport",  "base_time": 80,  "variance": 22, "buffer": 20, "cost": 4500},
                {"mode": "cab",    "from": "jaipur.airport",  "to": "jaipur.home",     "base_time": 25,  "variance": 10, "buffer": 0,  "cost": 300},
            ]
        },
        "cheapest": {
            "name": "Cheapest", "icon": "💰",
            "description": "Auto + Mail/Express train — direct LKO–JP route, good value",
            "legs": [
                {"mode": "auto",       "from": "lucknow.home",          "to": "lucknow.railway_station", "base_time": 20,  "variance": 8,  "buffer": 35, "cost": 80},
                {"mode": "mail_train", "from": "lucknow.railway_station","to": "jaipur.railway_station",  "base_time": 600, "variance": 55, "buffer": 20, "cost": 580},
                {"mode": "auto",       "from": "jaipur.railway_station", "to": "jaipur.home",             "base_time": 12,  "variance": 6,  "buffer": 0,  "cost": 80},
            ]
        },
        "reliable": {
            "name": "Most Reliable", "icon": "🛡",
            "description": "Auto + Express train with extra buffer — more reliable schedule than mail train",
            "legs": [
                {"mode": "auto",          "from": "lucknow.home",          "to": "lucknow.railway_station", "base_time": 20,  "variance": 8,  "buffer": 35, "cost": 80},
                {"mode": "express_train", "from": "lucknow.railway_station","to": "jaipur.railway_station",  "base_time": 560, "variance": 38, "buffer": 25, "cost": 780},
                {"mode": "cab",           "from": "jaipur.railway_station", "to": "jaipur.home",             "base_time": 12,  "variance": 6,  "buffer": 0,  "cost": 120},
            ]
        }
    },

    ("lucknow", "pune"): {
        "distance_km": 1400,
        "fastest": {
            "name": "Fastest", "icon": "⚡",
            "description": "Cab + Direct flight (Lucknow–Pune, IndiGo/SpiceJet) + Cab",
            "legs": [
                {"mode": "cab",    "from": "lucknow.home",    "to": "lucknow.airport", "base_time": 40,  "variance": 14, "buffer": 20, "cost": 380},
                {"mode": "flight", "from": "lucknow.airport", "to": "pune.airport",    "base_time": 110, "variance": 24, "buffer": 20, "cost": 5200},
                {"mode": "cab",    "from": "pune.airport",    "to": "pune.home",       "base_time": 30,  "variance": 14, "buffer": 0,  "cost": 450},
            ]
        },
        "cheapest": {
            "name": "Cheapest", "icon": "💰",
            "description": "Auto + Long-distance Express train — most economical for 1400 km route",
            "legs": [
                {"mode": "auto",       "from": "lucknow.home",          "to": "lucknow.railway_station", "base_time": 20,   "variance": 8,  "buffer": 30, "cost": 80},
                {"mode": "mail_train", "from": "lucknow.railway_station","to": "pune.railway_station",    "base_time": 1320, "variance": 75, "buffer": 30, "cost": 1100},
                {"mode": "metro",      "from": "pune.railway_station",  "to": "pune.home",               "base_time": 20,   "variance": 10, "buffer": 0,  "cost": 30},
            ]
        },
        "reliable": {
            "name": "Most Reliable", "icon": "🛡",
            "description": "Cab + Flight + Cab — only practical reliable option for 1400 km; generous airport buffers",
            "legs": [
                {"mode": "cab",    "from": "lucknow.home",    "to": "lucknow.airport", "base_time": 40,  "variance": 14, "buffer": 25, "cost": 380},
                {"mode": "flight", "from": "lucknow.airport", "to": "pune.airport",    "base_time": 110, "variance": 22, "buffer": 25, "cost": 5500},
                {"mode": "cab",    "from": "pune.airport",    "to": "pune.home",       "base_time": 30,  "variance": 14, "buffer": 0,  "cost": 450},
            ]
        }
    },

    ("lucknow", "shimla"): {
        "distance_km": 800,
        "fastest": {
            "name": "Fastest", "icon": "⚡",
            "description": "Cab + Flight to Chandigarh + Cab uphill — ~7 hr door-to-door",
            "legs": [
                {"mode": "cab",    "from": "lucknow.home",    "to": "lucknow.airport",    "base_time": 40,  "variance": 14, "buffer": 20, "cost": 380},
                {"mode": "flight", "from": "lucknow.airport", "to": "chandigarh.airport", "base_time": 100, "variance": 25, "buffer": 20, "cost": 5000},
                {"mode": "cab",    "from": "chandigarh.airport","to": "shimla.home",      "base_time": 210, "variance": 55, "buffer": 0,  "cost": 2500},
            ]
        },
        "cheapest": {
            "name": "Cheapest", "icon": "💰",
            "description": "Intercity bus to Delhi + HRTC bus to Shimla — cheapest multi-leg option",
            "legs": [
                {"mode": "auto",          "from": "lucknow.home",         "to": "lucknow.bus_terminal",  "base_time": 25,  "variance": 9,  "buffer": 20, "cost": 100},
                {"mode": "intercity_bus", "from": "lucknow.bus_terminal", "to": "delhi.bus_terminal",    "base_time": 480, "variance": 55, "buffer": 20, "cost": 450},
                {"mode": "hrtc_bus",      "from": "delhi.bus_terminal",   "to": "shimla.bus_terminal",   "base_time": 540, "variance": 90, "buffer": 15, "cost": 500},
                {"mode": "auto",          "from": "shimla.bus_terminal",  "to": "shimla.home",           "base_time": 15,  "variance": 7,  "buffer": 0,  "cost": 100},
            ]
        },
        "reliable": {
            "name": "Most Reliable", "icon": "🛡",
            "description": "Train via Delhi + Kalka Shatabdi + Toy Train — most structured timing",
            "legs": [
                {"mode": "auto",          "from": "lucknow.home",          "to": "lucknow.railway_station",    "base_time": 20,  "variance": 8,  "buffer": 35, "cost": 80},
                {"mode": "express_train", "from": "lucknow.railway_station","to": "delhi.railway_station",      "base_time": 390, "variance": 25, "buffer": 30, "cost": 650},
                {"mode": "express_train", "from": "delhi.railway_station",  "to": "chandigarh.railway_station", "base_time": 210, "variance": 18, "buffer": 20, "cost": 520},
                {"mode": "toy_train",     "from": "chandigarh.railway_station","to": "shimla.railway_station",  "base_time": 330, "variance": 35, "buffer": 0,  "cost": 500},
            ]
        }
    },

    # ==================== PUNE ↔ SHIMLA ====================

    ("pune", "shimla"): {
        "distance_km": 1800,
        "fastest": {
            "name": "Fastest", "icon": "⚡",
            "description": "Cab + Flight to Chandigarh + Cab uphill — only practical fast option for 1800 km",
            "legs": [
                {"mode": "cab",    "from": "pune.home",          "to": "pune.airport",          "base_time": 30,  "variance": 14, "buffer": 20, "cost": 400},
                {"mode": "flight", "from": "pune.airport",       "to": "chandigarh.airport",    "base_time": 150, "variance": 30, "buffer": 20, "cost": 6500},
                {"mode": "cab",    "from": "chandigarh.airport", "to": "shimla.home",           "base_time": 210, "variance": 55, "buffer": 0,  "cost": 2500},
            ]
        },
        "cheapest": {
            "name": "Cheapest", "icon": "💰",
            "description": "Train to Delhi + HRTC bus to Shimla — slow but most economical for 1800 km",
            "legs": [
                {"mode": "metro",         "from": "pune.home",             "to": "pune.railway_station",      "base_time": 20,   "variance": 10, "buffer": 30, "cost": 30},
                {"mode": "mail_train",    "from": "pune.railway_station",  "to": "delhi.railway_station",     "base_time": 1380, "variance": 85, "buffer": 30, "cost": 1200},
                {"mode": "hrtc_bus",      "from": "delhi.bus_terminal",    "to": "shimla.bus_terminal",       "base_time": 540,  "variance": 90, "buffer": 15, "cost": 500},
                {"mode": "auto",          "from": "shimla.bus_terminal",   "to": "shimla.home",               "base_time": 15,   "variance": 7,  "buffer": 0,  "cost": 100},
            ]
        },
        "reliable": {
            "name": "Most Reliable", "icon": "🛡",
            "description": "Cab + Flight to Chandigarh + Cab — flight eliminates train variance for this long haul",
            "legs": [
                {"mode": "cab",    "from": "pune.home",          "to": "pune.airport",          "base_time": 30,  "variance": 14, "buffer": 20, "cost": 400},
                {"mode": "flight", "from": "pune.airport",       "to": "chandigarh.airport",    "base_time": 150, "variance": 28, "buffer": 25, "cost": 6800},
                {"mode": "cab",    "from": "chandigarh.airport", "to": "shimla.home",           "base_time": 210, "variance": 50, "buffer": 0,  "cost": 2500},
            ]
        }
    },

 ("jaipur", "chandigarh"): {
    "distance_km": 540,

    "fastest": {
        "name": "Fastest", "icon": "⚡",
        "description": "Cab + flight (Jaipur → Chandigarh via Delhi) — fastest multi-leg (~4–5 hrs)",
        "legs": [
            {"mode": "cab", "from": "jaipur.home", "to": "jaipur.airport", "base_time": 30, "variance": 10, "buffer": 25, "cost": 250},
            {"mode": "flight", "from": "jaipur.airport", "to": "chandigarh.airport", "base_time": 90, "variance": 25, "buffer": 25, "cost": 4500},
            {"mode": "cab", "from": "chandigarh.airport", "to": "chandigarh.home", "base_time": 30, "variance": 10, "buffer": 0, "cost": 300},
        ]
    },

    "cheapest": {
        "name": "Cheapest", "icon": "💰",
        "description": "Bus via Delhi — most economical long-distance option",
        "legs": [
            {"mode": "auto", "from": "jaipur.home", "to": "jaipur.bus_terminal", "base_time": 20, "variance": 8, "buffer": 20, "cost": 80},
            {"mode": "intercity_bus", "from": "jaipur.bus_terminal", "to": "delhi.bus_terminal", "base_time": 360, "variance": 60, "buffer": 20, "cost": 400},
            {"mode": "intercity_bus", "from": "delhi.bus_terminal", "to": "chandigarh.bus_terminal", "base_time": 300, "variance": 50, "buffer": 20, "cost": 350},
            {"mode": "auto", "from": "chandigarh.bus_terminal", "to": "chandigarh.home", "base_time": 20, "variance": 7, "buffer": 0, "cost": 100},
        ]
    },

    "reliable": {
        "name": "Most Reliable", "icon": "🛡️",
        "description": "Cab + train via Delhi — structured and predictable timing",
        "legs": [
            {"mode": "cab", "from": "jaipur.home", "to": "jaipur.railway_station", "base_time": 25, "variance": 8, "buffer": 25, "cost": 200},
            {"mode": "express_train", "from": "jaipur.railway_station", "to": "delhi.railway_station", "base_time": 270, "variance": 18, "buffer": 25, "cost": 600},
            {"mode": "express_train", "from": "delhi.railway_station", "to": "chandigarh.railway_station", "base_time": 210, "variance": 15, "buffer": 20, "cost": 500},
            {"mode": "metro", "from": "chandigarh.railway_station", "to": "chandigarh.home", "base_time": 20, "variance": 7, "buffer": 0, "cost": 50},
        ]
    }
 },
 ("pune", "chandigarh"): {
    "distance_km": 1650,

    "fastest": {
        "name": "Fastest", "icon": "⚡",
        "description": "Cab + direct flight (Pune → Chandigarh) + cab — fastest (~4.5–5.5 hrs)",
        "legs": [
            {"mode": "cab", "from": "pune.home", "to": "pune.airport", "base_time": 40, "variance": 12, "buffer": 30, "cost": 350},
            {"mode": "flight", "from": "pune.airport", "to": "chandigarh.airport", "base_time": 140, "variance": 30, "buffer": 25, "cost": 6500},
            {"mode": "cab", "from": "chandigarh.airport", "to": "chandigarh.home", "base_time": 30, "variance": 10, "buffer": 0, "cost": 300},
        ]
    },

    "cheapest": {
        "name": "Cheapest", "icon": "💰",
        "description": "Train via Delhi — most economical long-distance option",
        "legs": [
            {"mode": "auto", "from": "pune.home", "to": "pune.railway_station", "base_time": 20, "variance": 8, "buffer": 25, "cost": 80},
            {"mode": "mail_train", "from": "pune.railway_station", "to": "delhi.railway_station", "base_time": 1400, "variance": 80, "buffer": 30, "cost": 900},
            {"mode": "express_train", "from": "delhi.railway_station", "to": "chandigarh.railway_station", "base_time": 210, "variance": 15, "buffer": 20, "cost": 500},
            {"mode": "metro", "from": "chandigarh.railway_station", "to": "chandigarh.home", "base_time": 20, "variance": 7, "buffer": 0, "cost": 50},
        ]
    },

    "reliable": {
        "name": "Most Reliable", "icon": "🛡️",
        "description": "Flight via Delhi + cab — structured with buffers",
        "legs": [
            {"mode": "cab", "from": "pune.home", "to": "pune.airport", "base_time": 40, "variance": 12, "buffer": 30, "cost": 350},
            {"mode": "flight", "from": "pune.airport", "to": "delhi.airport", "base_time": 140, "variance": 25, "buffer": 40, "cost": 5500},
            {"mode": "cab", "from": "delhi.airport", "to": "chandigarh.home", "base_time": 300, "variance": 45, "buffer": 0, "cost": 2800},
        ]
    }
},
 ("pune", "jaipur"): {
    "distance_km": 1150,

    "fastest": {
        "name": "Fastest", "icon": "⚡",
        "description": "Cab + direct flight (Pune → Jaipur) + cab (~3.5–4.5 hrs)",
        "legs": [
            {"mode": "cab", "from": "pune.home", "to": "pune.airport", "base_time": 40, "variance": 12, "buffer": 30, "cost": 350},
            {"mode": "flight", "from": "pune.airport", "to": "jaipur.airport", "base_time": 120, "variance": 25, "buffer": 25, "cost": 5500},
            {"mode": "cab", "from": "jaipur.airport", "to": "jaipur.home", "base_time": 30, "variance": 10, "buffer": 0, "cost": 250},
        ]
    },

    "cheapest": {
        "name": "Cheapest", "icon": "💰",
        "description": "Mail train — most economical option",
        "legs": [
            {"mode": "auto", "from": "pune.home", "to": "pune.railway_station", "base_time": 20, "variance": 8, "buffer": 25, "cost": 80},
            {"mode": "mail_train", "from": "pune.railway_station", "to": "jaipur.railway_station", "base_time": 1100, "variance": 70, "buffer": 30, "cost": 850},
            {"mode": "auto", "from": "jaipur.railway_station", "to": "jaipur.home", "base_time": 25, "variance": 10, "buffer": 0, "cost": 100},
        ]
    },

    "reliable": {
        "name": "Most Reliable", "icon": "🛡️",
        "description": "Flight via Delhi + train — structured and stable",
        "legs": [
            {"mode": "cab", "from": "pune.home", "to": "pune.airport", "base_time": 40, "variance": 12, "buffer": 30, "cost": 350},
            {"mode": "flight", "from": "pune.airport", "to": "delhi.airport", "base_time": 140, "variance": 25, "buffer": 40, "cost": 5500},
            {"mode": "express_train", "from": "delhi.railway_station", "to": "jaipur.railway_station", "base_time": 270, "variance": 18, "buffer": 20, "cost": 600},
            {"mode": "auto", "from": "jaipur.railway_station", "to": "jaipur.home", "base_time": 25, "variance": 10, "buffer": 0, "cost": 100},
        ]
    }
 },
 ("pune", "delhi"): {
    "distance_km": 1408,

    "fastest": {
        "name": "Fastest", "icon": "⚡",
        "description": "Cab + direct flight (Pune → Delhi) + cab (~3–4 hrs)",
        "legs": [
            {"mode": "cab", "from": "pune.home", "to": "pune.airport", "base_time": 40, "variance": 12, "buffer": 30, "cost": 350},
            {"mode": "flight", "from": "pune.airport", "to": "delhi.airport", "base_time": 140, "variance": 25, "buffer": 25, "cost": 5000},
            {"mode": "cab", "from": "delhi.airport", "to": "delhi.home", "base_time": 45, "variance": 15, "buffer": 0, "cost": 500},
        ]
    },

    "cheapest": {
        "name": "Cheapest", "icon": "💰",
        "description": "Mail train — lowest cost option",
        "legs": [
            {"mode": "auto", "from": "pune.home", "to": "pune.railway_station", "base_time": 20, "variance": 8, "buffer": 25, "cost": 80},
            {"mode": "mail_train", "from": "pune.railway_station", "to": "delhi.railway_station", "base_time": 1400, "variance": 80, "buffer": 30, "cost": 900},
            {"mode": "metro", "from": "delhi.railway_station", "to": "delhi.home", "base_time": 30, "variance": 10, "buffer": 0, "cost": 60},
        ]
    },

    "reliable": {
        "name": "Most Reliable", "icon": "🛡️",
        "description": "Flight + structured buffers — most predictable option",
        "legs": [
            {"mode": "cab", "from": "pune.home", "to": "pune.airport", "base_time": 40, "variance": 12, "buffer": 30, "cost": 350},
            {"mode": "flight", "from": "pune.airport", "to": "delhi.airport", "base_time": 140, "variance": 20, "buffer": 40, "cost": 5000},
            {"mode": "cab", "from": "delhi.airport", "to": "delhi.home", "base_time": 45, "variance": 15, "buffer": 0, "cost": 500},
        ]
    }
},
    # ==================== SHIMLA ↔ OTHERS ====================

    ("shimla", "delhi"): {
        "distance_km": 350,
        "fastest": {
            "name": "Fastest", "icon": "⚡",
            "description": "Cab to Chandigarh + Flight to Delhi — fastest descent-then-fly option",
            "legs": [
                {"mode": "cab",    "from": "shimla.home",        "to": "chandigarh.airport",  "base_time": 210, "variance": 55, "buffer": 30, "cost": 2500},
                {"mode": "flight", "from": "chandigarh.airport", "to": "delhi.airport",       "base_time": 60,  "variance": 20, "buffer": 20, "cost": 3500},
                {"mode": "metro",  "from": "delhi.airport",      "to": "delhi.home",          "base_time": 45,  "variance": 9,  "buffer": 0,  "cost": 60},
            ]
        },
        "cheapest": {
            "name": "Cheapest", "icon": "💰",
            "description": "HRTC Bus (Shimla ISBT to Delhi Kashmere Gate) — cheapest hill route option",
            "legs": [
                {"mode": "auto",     "from": "shimla.home",        "to": "shimla.bus_terminal",  "base_time": 15,  "variance": 7,  "buffer": 20, "cost": 100},
                {"mode": "hrtc_bus", "from": "shimla.bus_terminal","to": "delhi.bus_terminal",   "base_time": 540, "variance": 90, "buffer": 20, "cost": 500},
                {"mode": "dtc_bus",  "from": "delhi.bus_terminal", "to": "delhi.home",           "base_time": 45,  "variance": 14, "buffer": 0,  "cost": 25},
            ]
        },
        "reliable": {
            "name": "Most Reliable", "icon": "🛡",
            "description": "Toy Train to Kalka + Kalka Shatabdi to Delhi — most structured timing despite long duration",
            "legs": [
                {"mode": "auto",          "from": "shimla.home",              "to": "shimla.railway_station",      "base_time": 10,  "variance": 5,  "buffer": 20, "cost": 60},
                {"mode": "toy_train",     "from": "shimla.railway_station",   "to": "chandigarh.railway_station",  "base_time": 330, "variance": 35, "buffer": 30, "cost": 500},
                {"mode": "express_train", "from": "chandigarh.railway_station","to": "delhi.railway_station",      "base_time": 210, "variance": 18, "buffer": 20, "cost": 520},
                {"mode": "metro",         "from": "delhi.railway_station",    "to": "delhi.home",                  "base_time": 20,  "variance": 7,  "buffer": 0,  "cost": 30},
            ]
        }
    },

    ("shimla", "chandigarh"): {
        "distance_km": 115,
        "fastest": {
            "name": "Fastest", "icon": "⚡",
            "description": "Direct cab (hill descent via NH-5) — fastest door-to-door for this short route",
            "legs": [
                {"mode": "cab", "from": "shimla.home", "to": "chandigarh.home",
                 "base_time": 180, "variance": 50, "buffer": 0, "cost": 2200},
            ]
        },
        "cheapest": {
            "name": "Cheapest", "icon": "💰",
            "description": "HRTC Bus (Shimla to Chandigarh ISBT) — cheapest hill route option",
            "legs": [
                {"mode": "auto",     "from": "shimla.home",        "to": "shimla.bus_terminal",     "base_time": 15,  "variance": 7,  "buffer": 15, "cost": 100},
                {"mode": "hrtc_bus", "from": "shimla.bus_terminal","to": "chandigarh.bus_terminal",  "base_time": 240, "variance": 60, "buffer": 10, "cost": 300},
                {"mode": "auto",     "from": "chandigarh.bus_terminal","to": "chandigarh.home",      "base_time": 18,  "variance": 7,  "buffer": 0,  "cost": 100},
            ]
        },
        "reliable": {
            "name": "Most Reliable", "icon": "🛡",
            "description": "Toy Train to Kalka + Cab to Chandigarh — NMR rarely cancels; structured schedule",
            "legs": [
                {"mode": "auto",      "from": "shimla.home",             "to": "shimla.railway_station",      "base_time": 10,  "variance": 5,  "buffer": 20, "cost": 60},
                {"mode": "toy_train", "from": "shimla.railway_station",  "to": "chandigarh.railway_station",  "base_time": 330, "variance": 35, "buffer": 20, "cost": 500},
                {"mode": "cab",       "from": "chandigarh.railway_station","to": "chandigarh.home",           "base_time": 18,  "variance": 7,  "buffer": 0,  "cost": 180},
            ]
        }
    },

    ("shimla", "jaipur"): {
        "distance_km": 600,
        "fastest": {
            "name": "Fastest", "icon": "⚡",
            "description": "Cab to Chandigarh + Flight to Jaipur + Cab — ~6 hr door-to-door",
            "legs": [
                {"mode": "cab",    "from": "shimla.home",        "to": "chandigarh.airport",  "base_time": 210, "variance": 55, "buffer": 30, "cost": 2500},
                {"mode": "flight", "from": "chandigarh.airport", "to": "jaipur.airport",      "base_time": 90,  "variance": 25, "buffer": 20, "cost": 4500},
                {"mode": "cab",    "from": "jaipur.airport",     "to": "jaipur.home",         "base_time": 25,  "variance": 10, "buffer": 0,  "cost": 300},
            ]
        },
        "cheapest": {
            "name": "Cheapest", "icon": "💰",
            "description": "HRTC bus to Delhi + Intercity bus to Jaipur — cheapest multi-leg option",
            "legs": [
                {"mode": "auto",          "from": "shimla.home",        "to": "shimla.bus_terminal",  "base_time": 15,  "variance": 7,  "buffer": 20, "cost": 100},
                {"mode": "hrtc_bus",      "from": "shimla.bus_terminal","to": "delhi.bus_terminal",   "base_time": 540, "variance": 90, "buffer": 20, "cost": 500},
                {"mode": "intercity_bus", "from": "delhi.bus_terminal", "to": "jaipur.bus_terminal",  "base_time": 300, "variance": 38, "buffer": 10, "cost": 280},
                {"mode": "auto",          "from": "jaipur.bus_terminal","to": "jaipur.home",          "base_time": 20,  "variance": 8,  "buffer": 0,  "cost": 80},
            ]
        },
        "reliable": {
            "name": "Most Reliable", "icon": "🛡",
            "description": "Toy Train + Shatabdi to Delhi + Express to Jaipur — structured schedule, predictable legs",
            "legs": [
                {"mode": "auto",          "from": "shimla.home",              "to": "shimla.railway_station",      "base_time": 10,  "variance": 5,  "buffer": 20, "cost": 60},
                {"mode": "toy_train",     "from": "shimla.railway_station",   "to": "chandigarh.railway_station",  "base_time": 330, "variance": 35, "buffer": 30, "cost": 500},
                {"mode": "express_train", "from": "chandigarh.railway_station","to": "delhi.railway_station",      "base_time": 210, "variance": 18, "buffer": 25, "cost": 520},
                {"mode": "express_train", "from": "delhi.railway_station",    "to": "jaipur.railway_station",      "base_time": 270, "variance": 20, "buffer": 0,  "cost": 480},
            ]
        }
    }, 

    ("shimla", "lucknow"): {
        "distance_km": 800,
        "fastest": {
            "name": "Fastest", "icon": "⚡",
            "description": "Cab to Chandigarh + Flight to Lucknow + Cab — ~7.5 hr door-to-door",
            "legs": [
                {"mode": "cab",    "from": "shimla.home",        "to": "chandigarh.airport",  "base_time": 210, "variance": 55, "buffer": 30, "cost": 2500},
                {"mode": "flight", "from": "chandigarh.airport", "to": "lucknow.airport",     "base_time": 100, "variance": 25, "buffer": 20, "cost": 5000},
                {"mode": "cab",    "from": "lucknow.airport",    "to": "lucknow.home",        "base_time": 35,  "variance": 12, "buffer": 0,  "cost": 350},
            ]
        },
        "cheapest": {
            "name": "Cheapest", "icon": "💰",
            "description": "HRTC bus to Delhi + Intercity bus to Lucknow — cheapest multi-leg option",
            "legs": [
                {"mode": "auto",          "from": "shimla.home",         "to": "shimla.bus_terminal",  "base_time": 15,  "variance": 7,  "buffer": 20, "cost": 100},
                {"mode": "hrtc_bus",      "from": "shimla.bus_terminal", "to": "delhi.bus_terminal",   "base_time": 540, "variance": 90, "buffer": 20, "cost": 500},
                {"mode": "intercity_bus", "from": "delhi.bus_terminal",  "to": "lucknow.bus_terminal", "base_time": 480, "variance": 55, "buffer": 15, "cost": 450},
                {"mode": "auto",          "from": "lucknow.bus_terminal","to": "lucknow.home",         "base_time": 25,  "variance": 9,  "buffer": 0,  "cost": 120},
            ]
        },
        "reliable": {
            "name": "Most Reliable", "icon": "🛡",
            "description": "Toy Train + Shatabdi to Delhi + Express to Lucknow — most structured timing",
            "legs": [
                {"mode": "auto",          "from": "shimla.home",              "to": "shimla.railway_station",      "base_time": 10,  "variance": 5,  "buffer": 20, "cost": 60},
                {"mode": "toy_train",     "from": "shimla.railway_station",   "to": "chandigarh.railway_station",  "base_time": 330, "variance": 35, "buffer": 30, "cost": 500},
                {"mode": "express_train", "from": "chandigarh.railway_station","to": "delhi.railway_station",      "base_time": 210, "variance": 18, "buffer": 25, "cost": 520},
                {"mode": "express_train", "from": "delhi.railway_station",    "to": "lucknow.railway_station",     "base_time": 390, "variance": 25, "buffer": 0,  "cost": 650},
            ]
        }
    },

    ("shimla", "pune"): {
        "distance_km": 1800,
        "fastest": {
            "name": "Fastest", "icon": "⚡",
            "description": "Cab to Chandigarh + Flight to Pune + Cab — only practical fast option for 1800 km",
            "legs": [
                {"mode": "cab",    "from": "shimla.home",        "to": "chandigarh.airport",  "base_time": 210, "variance": 55, "buffer": 30, "cost": 2500},
                {"mode": "flight", "from": "chandigarh.airport", "to": "pune.airport",        "base_time": 150, "variance": 30, "buffer": 20, "cost": 6500},
                {"mode": "cab",    "from": "pune.airport",       "to": "pune.home",           "base_time": 30,  "variance": 14, "buffer": 0,  "cost": 450},
            ]
        },
        "cheapest": {
            "name": "Cheapest", "icon": "💰",
            "description": "HRTC bus to Delhi + Long-haul train to Pune — slow but most economical for 1800 km",
            "legs": [
                {"mode": "auto",       "from": "shimla.home",         "to": "shimla.bus_terminal",     "base_time": 15,   "variance": 7,  "buffer": 20, "cost": 100},
                {"mode": "hrtc_bus",   "from": "shimla.bus_terminal", "to": "delhi.bus_terminal",      "base_time": 540,  "variance": 90, "buffer": 20, "cost": 500},
                {"mode": "mail_train", "from": "delhi.railway_station","to": "pune.railway_station",   "base_time": 1380, "variance": 80, "buffer": 20, "cost": 1200},
                {"mode": "metro",      "from": "pune.railway_station","to": "pune.home",               "base_time": 20,   "variance": 10, "buffer": 0,  "cost": 30},
            ]
        },
        "reliable": {
            "name": "Most Reliable", "icon": "🛡",
            "description": "Toy Train + Shatabdi to Delhi + Flight to Pune — flight eliminates train variance for long haul",
            "legs": [
                {"mode": "auto",          "from": "shimla.home",              "to": "shimla.railway_station",      "base_time": 10,  "variance": 5,  "buffer": 20, "cost": 60},
                {"mode": "toy_train",     "from": "shimla.railway_station",   "to": "chandigarh.railway_station",  "base_time": 330, "variance": 35, "buffer": 30, "cost": 500},
                {"mode": "express_train", "from": "chandigarh.railway_station","to": "delhi.railway_station",      "base_time": 210, "variance": 18, "buffer": 25, "cost": 520},
                {"mode": "flight",        "from": "delhi.airport",            "to": "pune.airport",                "base_time": 120, "variance": 22, "buffer": 25, "cost": 5500},
                {"mode": "cab",           "from": "pune.airport",             "to": "pune.home",                   "base_time": 30,  "variance": 14, "buffer": 0,  "cost": 450},
            ]
        }
    },
}


def get_route(src: str, dst: str) -> dict:
    if (src, dst) in ROUTES:
        return ROUTES[(src, dst)]
    if (dst, src) in ROUTES:
        return ROUTES[(dst, src)]
    raise KeyError(f"No route found {src} → {dst}")



def resolve_location(loc_key: str) -> dict:
    """Resolve 'city.hub_type' to coordinates and name."""
    parts = loc_key.split(".")
    if len(parts) != 2:
        return {"name": loc_key, "lat": 0, "lon": 0}
    city_key, hub_type = parts
    city = CITIES.get(city_key, {})
    hubs = city.get("hubs", {})
    hub = hubs.get(hub_type, {"name": loc_key, "lat": city.get("lat", 0), "lon": city.get("lon", 0)})
    return hub


CITY_LIST = list(CITIES.keys())
VALID_COMBINATIONS = [
    (CITY_LIST[i], CITY_LIST[j])
    for i in range(len(CITY_LIST))
    for j in range(i + 1, len(CITY_LIST))
]
print("Seed file loaded")


def seed_database():

    print("Seeding started...")

    db = SessionLocal()

    city_map = {}
    mode_map = {}

    for key, city in CITIES.items():

        city_obj = models.City(
            name=city["name"],
            code=city["code"],
            latitude=city["lat"],
            longitude=city["lon"],
            emoji=city["emoji"]
        )

        db.add(city_obj)
        db.commit()
        db.refresh(city_obj)

        city_map[key] = city_obj.id

        for loc_type, loc in city["hubs"].items():

            location = models.Location(
                city_id=city_obj.id,
                name=loc["name"],
                type=loc_type,
                latitude=loc["lat"],
                longitude=loc["lon"]
            )

            db.add(location)

    db.commit()

    for key, mode in TRANSPORT_MODES.items():

        mode_obj = models.TransportMode(
            name=mode["name"],
            icon=mode["icon"],
            color=mode["color"],
            avg_speed_kmph=mode["avg_speed_kmph"],
            base_cost_per_km=mode["base_cost_per_km"],
            variance_factor=mode["variance_factor"],
            fixed_variance=mode["fixed_variance"],
            notes=mode["notes"]
        )

        db.add(mode_obj)
        db.commit()
        db.refresh(mode_obj)

        mode_map[key] = mode_obj.id

    for (src, dst), route in ROUTES.items():

        route_obj = models.Route(
            source_city_id=city_map[src],
            destination_city_id=city_map[dst],
            distance_km=route["distance_km"]
        )

        db.add(route_obj)
        db.commit()
        db.refresh(route_obj)

        for opt_type in ["fastest", "cheapest", "reliable"]:

            for leg in route[opt_type]["legs"]:

                option = models.RouteOption(
                    route_id=route_obj.id,
                    mode_id=mode_map[leg["mode"]],
                    option_type=opt_type,
                    base_travel_time=leg["base_time"],
                    cost=leg["cost"],
                    variance_minutes=leg["variance"],
                    recommended_buffer=leg["buffer"]
                )

                db.add(option)

    db.commit()

    db.close()

    print("Database fully seeded!")


if __name__ == "__main__":
    seed_database()