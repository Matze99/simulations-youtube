from dataclasses import dataclass
from typing import Optional
import random

from housing_rent_simulation.models.property import Property


@dataclass
class Renter:
    """Represents a renter in the housing market simulation."""

    id: int
    min_price: float
    max_price: float
    income: float
    job_stability: float  # Score between 0 and 1

    def can_afford(self, price: float) -> bool:
        """Check if the renter can afford a given price."""
        return self.min_price <= price <= self.max_price
