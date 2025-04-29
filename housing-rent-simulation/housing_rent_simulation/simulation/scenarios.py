from housing_rent_simulation.simulation.base import BaseSimulation
from housing_rent_simulation.models.renter import Renter
from housing_rent_simulation.models.property import Property
from housing_rent_simulation.constants import MIN_RENT, MAX_RENT, LANDLORD_WEIGHT


class NoisyFairPriceSimulation(BaseSimulation):
    """Simulation where renters see a noisy estimate of the fair price."""

    def __init__(
        self,
        renters: list[Renter],
        properties: list[Property],
        noise_level: float = 0.1,
    ):
        """
        Initialize the simulation with noise level.

        Args:
            renters: list of renters in the simulation
            properties: list of properties in the simulation
            noise_level: Standard deviation of the noise as a fraction of fair price
        """
        super().__init__(renters, properties)
        self.noise_level = noise_level

    def _get_scored_property(
        self, renter: Renter, _property: Property
    ) -> tuple[float, Property]:
        """
        Get the scored property for a given renter.
        """
        return _property.get_observed_price(self.noise_level), _property


class ActualFairPriceSimulation(BaseSimulation):
    """Simulation where renters see the actual fair price."""

    def _get_scored_property(
        self, renter: Renter, _property: Property
    ) -> tuple[float, Property]:
        """
        Get the scored property for a given renter.
        """
        return _property.fair_price, _property


class NoisyFairPriceWithLandlordScoreSimulation(NoisyFairPriceSimulation):
    """Simulation where renters see noisy fair price and landlord quality score."""

    def _get_scored_property(
        self, renter: Renter, _property: Property
    ) -> tuple[float, Property]:
        """
        Get the scored property for a given renter.
        """
        noisy_fair_price = _property.get_observed_price(self.noise_level)
        landlord_score = LANDLORD_WEIGHT * _property.landlord_quality + (
            noisy_fair_price - MIN_RENT
        ) / (MAX_RENT - MIN_RENT)
        return landlord_score, _property


class ActualFairPriceWithLandlordScoreSimulation(ActualFairPriceSimulation):
    """Simulation where renters see actual fair price and landlord quality score."""

    def _get_scored_property(
        self, renter: Renter, _property: Property
    ) -> tuple[float, Property]:
        """
        Get the scored property for a given renter.
        """
        landlord_score = LANDLORD_WEIGHT * _property.landlord_quality + (
            _property.fair_price - MIN_RENT
        ) / (MAX_RENT - MIN_RENT)
        return landlord_score, _property
