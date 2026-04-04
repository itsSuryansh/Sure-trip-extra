
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class City(Base):
    __tablename__ = "cities"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    code = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    emoji = Column(String, default="📍")


class Location(Base):
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=False)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False) 
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    city = relationship("City")


class Route(Base):
    __tablename__ = "routes"
    id = Column(Integer, primary_key=True, index=True)
    source_city_id = Column(Integer, ForeignKey("cities.id"), nullable=False)
    destination_city_id = Column(Integer, ForeignKey("cities.id"), nullable=False)
    distance_km = Column(Float, nullable=False)
    source = relationship("City", foreign_keys=[source_city_id])
    destination = relationship("City", foreign_keys=[destination_city_id])


class TransportMode(Base):
    __tablename__ = "transport_modes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    icon = Column(String, default="🚗")
    color = Column(String, default="#888")
    avg_speed_kmph = Column(Float, nullable=False)
    base_cost_per_km = Column(Float, nullable=False)
    variance_factor = Column(Float, nullable=False)
    fixed_variance = Column(Float, nullable=False)
    notes = Column(Text, nullable=True)


class RouteOption(Base):
    __tablename__ = "route_options"
    id = Column(Integer, primary_key=True, index=True)
    route_id = Column(Integer, ForeignKey("routes.id"), nullable=False)
    mode_id = Column(Integer, ForeignKey("transport_modes.id"), nullable=False)
    option_type = Column(String, nullable=False)  
    base_travel_time = Column(Float, nullable=False)
    cost = Column(Float, nullable=False)
    variance_minutes = Column(Float, nullable=False)
    recommended_buffer = Column(Float, nullable=False)
    route = relationship("Route")
    mode = relationship("TransportMode")


class Journey(Base):
    __tablename__ = "journeys"
    id = Column(Integer, primary_key=True, index=True)
    source = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    departure_time = Column(DateTime, nullable=False)
    deadline_time = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
