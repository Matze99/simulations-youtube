from dataclasses import dataclass
from housing_rent_simulation.models.renter import Renter
from housing_rent_simulation.models.property import Property


@dataclass
class SimulationResult:
    """Results of a simulation run."""

    @dataclass
    class Assignment:
        """An assignment of a renter to a property."""

        property_id: int
        renter_id: int
        price: float

    total_assignments: int
    total_revenue: float
    average_price: float
    assignments: list[Assignment]


class BaseSimulation:
    """Base class for housing market simulations."""

    def __init__(self, renters: list[Renter], properties: list[Property]):
        """
        Initialize the simulation with renters and properties.

        Args:
            renters: List of renters in the simulation
            properties: List of properties in the simulation
        """
        self.renters = renters
        self.properties = properties
        self._reset_simulation()

    def _get_scored_property(
        self, renter: Renter, _property: Property
    ) -> tuple[float, Property]:
        """
        Get the scored property for a given renter.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    def get_ranked_properties(self, renter: Renter) -> list[tuple[float, Property]]:
        """
        Get properties sorted by their score for a given renter.

        Args:
            renter: The renter to get the scored properties for

        Returns:
            List of properties sorted by their score
        """
        scored_properties = sorted(
            [
                self._get_scored_property(renter, _property)
                for _property in self.properties
                if renter.can_afford(_property)
            ],
            key=lambda x: x[0],
            reverse=True,
        )

        return [property for _, property in scored_properties]

    def _reset_simulation(self) -> None:
        """Reset the simulation state."""
        for renter in self.renters:
            renter.assigned_property = None
        for _property in self.properties:
            _property.assigned_renter = None
            _property.max_possible_price = None

    def _get_property_ranks(self) -> dict[int, list[int]]:
        """
        Get the ranks of each property for each renter.

        Returns:
            Dictionary mapping property IDs to lists of ranks
        """
        ranks: dict[int, list[int]] = {p.id: [] for p in self.properties}

        for renter in self.renters:
            ranked_properties = self.get_ranked_properties(renter)
            for i, _property in enumerate(ranked_properties):
                ranks[_property.id].append(i)

        return ranks

    def get_average_rank(self) -> dict[int, float]:
        """
        Get the average rank of each property.
        """
        ranks = self._get_property_ranks()
        return {
            property_id: sum(ranks[property_id]) / len(ranks[property_id])
            for property_id in ranks
        }
