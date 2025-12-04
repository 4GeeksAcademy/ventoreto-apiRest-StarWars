
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, Boolean

db = SQLAlchemy()


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    # Relación con la tabla de favoritos
    favorites: Mapped[list["Favorite"]] = relationship(back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
        }


class People(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    uid: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False)  # UID de SWAPI
    birth_year: Mapped[str] = mapped_column(String(50), nullable=True)
    eye_color: Mapped[str] = mapped_column(String(50), nullable=True)
    gender: Mapped[str] = mapped_column(String(50), nullable=True)
    hair_color: Mapped[str] = mapped_column(String(50), nullable=True)
    height: Mapped[str] = mapped_column(String(50), nullable=True)
    mass: Mapped[str] = mapped_column(String(50), nullable=True)
    skin_color: Mapped[str] = mapped_column(String(50), nullable=True)
    homeworld: Mapped[str] = mapped_column(String(250), nullable=True)

    # Relación con la tabla de favoritos
    favorites: Mapped[list["Favorite"]] = relationship(back_populates="people")

    def serialize(self):
        return {
            "id": self.id,
            "uid": self.uid,
            "name": self.name,
            "birth_year": self.birth_year,
            "eye_color": self.eye_color,
            "gender": self.gender,
            "hair_color": self.hair_color,
            "height": self.height,
            "mass": self.mass,
            "skin_color": self.skin_color,
            "homeworld": self.homeworld,
        }


class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    uid: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False)  # UID de SWAPI
    climate: Mapped[str] = mapped_column(String(250), nullable=True)
    created: Mapped[str] = mapped_column(String(50), nullable=True)
    diameter: Mapped[str] = mapped_column(String(50), nullable=True)
    edited: Mapped[str] = mapped_column(String(50), nullable=True)
    gravity: Mapped[str] = mapped_column(String(50), nullable=True)
    orbital_period: Mapped[str] = mapped_column(String(50), nullable=True)
    population: Mapped[str] = mapped_column(String(50), nullable=True)
    rotation_period: Mapped[str] = mapped_column(String(50), nullable=True)
    surface_water: Mapped[str] = mapped_column(String(50), nullable=True)
    terrain: Mapped[str] = mapped_column(String(250), nullable=True)

    # Relación con la tabla de favoritos
    favorites: Mapped[list["Favorite"]] = relationship(back_populates="planet")

    def serialize(self):
        return {
            "id": self.id,
            "uid": self.uid,
            "name": self.name,
            "climate": self.climate,
            "diameter": self.diameter,
            "gravity": self.gravity,
            "orbital_period": self.orbital_period,
            "population": self.population,
            "rotation_period": self.rotation_period,
            "surface_water": self.surface_water,
            "terrain": self.terrain,
        }


class Favorite(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    people_id: Mapped[int] = mapped_column(
        ForeignKey('people.id'), nullable=True)
    planet_id: Mapped[int] = mapped_column(
        ForeignKey('planet.id'), nullable=True)

    # Relaciones inversas
    user: Mapped["User"] = relationship(back_populates="favorites")
    people: Mapped["People"] = relationship(back_populates="favorites")
    planet: Mapped["Planet"] = relationship(back_populates="favorites")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "people_id": self.people_id,
            "planet_id": self.planet_id,
        }
