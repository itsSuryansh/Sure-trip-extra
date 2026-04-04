from database import engine, Base, SessionLocal
import models
from seed_data import CITIES, TRANSPORT_MODES, ROUTES

print("Creating tables...")

Base.metadata.create_all(bind=engine)

db = SessionLocal()

print("Adding cities and locations...")

city_map = {}

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

    for hub_type, hub in city["hubs"].items():

        loc = models.Location(
            city_id=city_obj.id,
            name=hub["name"],
            type=hub_type,
            latitude=hub["lat"],
            longitude=hub["lon"]
        )

        db.add(loc)

db.commit()


print("Adding transport modes...")

mode_map = {}

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


print("Adding routes and options...")

for (src, dst), route in ROUTES.items():

    route_obj = models.Route(
        source_city_id=city_map[src],
        destination_city_id=city_map[dst],
        distance_km=route["distance_km"]
    )

    db.add(route_obj)
    db.commit()
    db.refresh(route_obj)


    for option_type in ["fastest", "cheapest", "reliable"]:

        for leg in route[option_type]["legs"]:

            option = models.RouteOption(

                route_id=route_obj.id,
                mode_id=mode_map[leg["mode"]],
                option_type=option_type,
                base_travel_time=leg["base_time"],
                cost=leg["cost"],
                variance_minutes=leg["variance"],
                recommended_buffer=leg["buffer"]

            )

            db.add(option)

db.commit()

print("DATABASE FULLY CREATED SUCCESSFULLY")