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
        self.renters_map = {r.id: r for r in renters}
        self.properties = properties
        self.properties_map = {p.id: p for p in properties}
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
                if renter.can_afford(_property.listed_price)
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
            property_id: sum(ranks[property_id]) / (len(ranks[property_id]) + 1e-6)
            for property_id in ranks
        }

    def _get_renter_ranks(self) -> dict[int, list[int]]:
        """
        Get the ranks of each renter for each property they can afford.

        Returns:
            Dictionary mapping renter IDs to lists of ranks
        """
        renter_ranks: dict[int, list[int]] = {r.id: [] for r in self.renters}

        for _property in self.properties:
            # Get all renters who can afford this property
            eligible_renters = [
                renter
                for renter in self.renters
                if renter.can_afford(_property.listed_price)
            ]

            # Sort renters by their score for this property
            scored_renters = sorted(
                [
                    (renter.calculate_attractiveness_score(), renter)
                    for renter in eligible_renters
                ],
                key=lambda x: x[0],
                reverse=True,
            )

            # Record ranks
            for i, (_, renter) in enumerate(scored_renters):
                renter_ranks[renter.id].append(i)

        return renter_ranks

    def match_renters_to_properties(self) -> SimulationResult:
        """
        Match renters to properties minimizing both property and renter ranks.

        Returns:
            SimulationResult containing the assignments and statistics
        """
        self._reset_simulation()

        # Get ranks for both properties and renters
        property_ranks = self._get_property_ranks()
        property_ranks_mapping = {
            k: {r_id: i for (i, r_id) in enumerate(v)}
            for k, v in property_ranks.items()
        }
        renter_ranks = self._get_renter_ranks()
        renter_ranks_mapping = {
            k: {p_id: i for (i, p_id) in enumerate(v)} for k, v in renter_ranks.items()
        }

        # Create a list of all possible assignments with their combined rank
        possible_assignments = []
        for renter in self.renters:
            for _property in self.properties:
                if renter.can_afford(_property.listed_price):
                    # Calculate combined rank (lower is better)
                    property_rank = property_ranks_mapping.get(
                        _property.id, dict()
                    ).get(renter.id, float("inf") - 1000)
                    renter_rank = renter_ranks_mapping.get(renter.id, dict()).get(
                        _property.id, float("inf") - 1000
                    )
                    combined_rank = property_rank + 3 * renter_rank

                    possible_assignments.append((combined_rank, renter, _property))

        # Sort assignments by combined rank
        possible_assignments.sort(key=lambda x: x[0])

        # Make assignments
        assignments = []
        assigned_renters = set()
        assigned_properties = set()

        for _, renter, _property in possible_assignments:
            if (
                renter.id not in assigned_renters
                and _property.id not in assigned_properties
            ):

                # Make the assignment
                renter.assigned_property = _property
                _property.assigned_renter = renter
                _property.max_possible_price = renter.max_price

                assignments.append(
                    SimulationResult.Assignment(
                        property_id=_property.id,
                        renter_id=renter.id,
                        price=_property.listed_price,
                    )
                )

                assigned_renters.add(renter.id)
                assigned_properties.add(_property.id)

        return assignments
