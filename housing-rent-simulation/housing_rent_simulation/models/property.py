from dataclasses import dataclass
from typing import Optional
import random


@dataclass
class Property:
    """Represents a property in the housing market simulation."""

    id: int
    fair_price: float
    listed_price: float
    landlord_quality: float  # Score between 0 and 1
    max_possible_price: Optional[float] = None

    def __post_init__(self):
        """Validate the property attributes after initialization."""
        if not 0 <= self.landlord_quality <= 1:
            raise ValueError("Landlord quality must be between 0 and 1")
        if self.listed_price <= 0:
            raise ValueError("Listed price must be positive")
        if self.fair_price <= 0:
            raise ValueError("Fair price must be positive")

    def get_observed_price(self, noise_level: float = 0.0) -> float:
        """
        Get the observed price of the property with optional noise.

        Args:
            noise_level: Amount of noise to add to the fair price

        Returns:
            Observed price with noise if noise_level > 0, otherwise fair price
        """
        if noise_level > 0:
            noise = random.gauss(0, noise_level * self.fair_price)
            return self.fair_price + noise
        return self.fair_price
