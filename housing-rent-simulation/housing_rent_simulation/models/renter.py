from dataclasses import dataclass
from typing import List, Optional
import random


@dataclass
class Renter:
    """Represents a renter in the housing market simulation."""

    id: int
    min_price: float
    max_price: float
    income: float
    job_stability: float  # Score between 0 and 1
    assigned_property: Optional[int] = None

    def can_afford(self, price: float) -> bool:
        """Check if the renter can afford a given price."""
        return self.min_price <= price <= self.max_price

    def rank_properties(
        self, properties: List["Property"], noise_level: float = 0.0
    ) -> List["Property"]:
        """
        Rank properties based on observed fair price and landlord quality.

        Args:
            properties: List of available properties
            noise_level: Amount of noise to add to fair price (0 for no noise)

        Returns:
            List of properties ranked by preference
        """
        affordable_properties = [
            p for p in properties if self.can_afford(p.listed_price)
        ]

        def get_observed_price(property: "Property") -> float:
            if noise_level > 0:
                noise = random.gauss(0, noise_level * property.fair_price)
                return property.fair_price + noise
            return property.fair_price

        # Sort by observed price (lower is better) and then by landlord quality (higher is better)
        return sorted(
            affordable_properties,
            key=lambda p: (get_observed_price(p), -p.landlord_quality),
        )

    def bid_on_property(self, property: "Property") -> bool:
        """Determine if the renter will bid on a property."""
        return self.can_afford(property.listed_price)
