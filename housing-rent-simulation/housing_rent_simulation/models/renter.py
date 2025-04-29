from dataclasses import dataclass

from housing_rent_simulation.constants import MAX_INCOME, MIN_INCOME, INCOME_WEIGHT


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

    def calculate_attractiveness_score(self) -> float:
        """
        Calculate the attractiveness score for the renter.

        Args:
            max_income: The maximum income in the market to normalize against

        Returns:
            float: Attractiveness score between 0 and 2 (normalized income + job stability)
        """
        normalized_income = (self.income - MIN_INCOME) / (MAX_INCOME - MIN_INCOME)
        return normalized_income * INCOME_WEIGHT + self.job_stability
