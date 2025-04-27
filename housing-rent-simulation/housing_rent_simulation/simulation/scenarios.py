from typing import List
from housing_rent_simulation.simulation.base import BaseSimulation, SimulationResult
from housing_rent_simulation.models.renter import Renter
from housing_rent_simulation.models.property import Property


class NoisyFairPriceSimulation(BaseSimulation):
    """Simulation where renters see a noisy estimate of the fair price."""

    def __init__(
        self,
        renters: List[Renter],
        properties: List[Property],
        noise_level: float = 0.1,
    ):
        """
        Initialize the simulation with noise level.

        Args:
            renters: List of renters in the simulation
            properties: List of properties in the simulation
            noise_level: Standard deviation of the noise as a fraction of fair price
        """
        super().__init__(renters, properties)
        self.noise_level = noise_level

    def _get_property_bids(self) -> dict[int, List[Renter]]:
        """Override to include noise in price observations."""
        bids = {p.id: [] for p in self.properties}

        for renter in self.renters:
            if renter.assigned_property is None:
                for property in self.properties:
                    if property.is_available():
                        observed_price = property.get_observed_price(self.noise_level)
                        if renter.can_afford(observed_price):
                            bids[property.id].append(renter)

        return bids


class ActualFairPriceSimulation(BaseSimulation):
    """Simulation where renters see the actual fair price."""

    def _get_property_bids(self) -> dict[int, List[Renter]]:
        """Override to use actual fair prices."""
        bids = {p.id: [] for p in self.properties}

        for renter in self.renters:
            if renter.assigned_property is None:
                for property in self.properties:
                    if property.is_available() and renter.can_afford(
                        property.fair_price
                    ):
                        bids[property.id].append(renter)

        return bids


class NoisyFairPriceWithLandlordScoreSimulation(NoisyFairPriceSimulation):
    """Simulation where renters see noisy fair price and landlord quality score."""

    def _get_property_bids(self) -> dict[int, List[Renter]]:
        """Override to include both noisy price and landlord quality in ranking."""
        bids = {p.id: [] for p in self.properties}

        for renter in self.renters:
            if renter.assigned_property is None:
                # Get properties the renter can afford
                affordable_properties = [
                    p
                    for p in self.properties
                    if p.is_available()
                    and renter.can_afford(p.get_observed_price(self.noise_level))
                ]

                # Sort by observed price and landlord quality
                sorted_properties = sorted(
                    affordable_properties,
                    key=lambda p: (
                        p.get_observed_price(self.noise_level),
                        -p.landlord_quality,
                    ),
                )

                # Add bids in order of preference
                for property in sorted_properties:
                    bids[property.id].append(renter)

        return bids


class ActualFairPriceWithLandlordScoreSimulation(ActualFairPriceSimulation):
    """Simulation where renters see actual fair price and landlord quality score."""

    def _get_property_bids(self) -> dict[int, List[Renter]]:
        """Override to include both actual price and landlord quality in ranking."""
        bids = {p.id: [] for p in self.properties}

        for renter in self.renters:
            if renter.assigned_property is None:
                # Get properties the renter can afford
                affordable_properties = [
                    p
                    for p in self.properties
                    if p.is_available() and renter.can_afford(p.fair_price)
                ]

                # Sort by fair price and landlord quality
                sorted_properties = sorted(
                    affordable_properties,
                    key=lambda p: (p.fair_price, -p.landlord_quality),
                )

                # Add bids in order of preference
                for property in sorted_properties:
                    bids[property.id].append(renter)

        return bids
