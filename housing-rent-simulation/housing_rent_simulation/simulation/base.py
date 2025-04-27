from typing import List, Dict, Tuple
from dataclasses import dataclass
from housing_rent_simulation.models.renter import Renter
from housing_rent_simulation.models.property import Property


@dataclass
class SimulationResult:
    """Results of a simulation run."""

    total_assignments: int
    total_revenue: float
    average_price: float
    assignments: List[Tuple[int, int, float]]  # (property_id, renter_id, price)


class BaseSimulation:
    """Base class for housing market simulations."""

    def __init__(self, renters: List[Renter], properties: List[Property]):
        """
        Initialize the simulation with renters and properties.

        Args:
            renters: List of renters in the simulation
            properties: List of properties in the simulation
        """
        self.renters = renters
        self.properties = properties
        self._reset_simulation()

    def _reset_simulation(self) -> None:
        """Reset the simulation state."""
        for renter in self.renters:
            renter.assigned_property = None
        for property in self.properties:
            property.assigned_renter = None
            property.max_possible_price = None

    def _get_property_bids(self) -> Dict[int, List[Renter]]:
        """
        Get all bids for each property.

        Returns:
            Dictionary mapping property IDs to lists of bidding renters
        """
        bids: Dict[int, List[Renter]] = {p.id: [] for p in self.properties}

        for renter in self.renters:
            if renter.assigned_property is None:  # Only consider unassigned renters
                for property in self.properties:
                    if property.is_available() and renter.bid_on_property(property):
                        bids[property.id].append(renter)

        return bids

    def _assign_property(self, property: Property, bidders: List[Renter]) -> None:
        """
        Assign the most suitable renter to a property.

        Args:
            property: The property to assign
            bidders: List of renters bidding on the property
        """
        if not bidders:
            return

        # Sort bidders by job stability and income (descending)
        sorted_bidders = sorted(
            bidders, key=lambda r: (r.job_stability, r.income), reverse=True
        )

        best_renter = sorted_bidders[0]
        property.assign_renter(best_renter.id, best_renter.max_price)
        best_renter.assigned_property = property.id

    def run_simulation(self) -> SimulationResult:
        """
        Run the simulation and return the results.

        Returns:
            SimulationResult containing the results of the simulation
        """
        self._reset_simulation()
        assignments = []

        while True:
            bids = self._get_property_bids()
            if not any(bids.values()):  # No more bids
                break

            # Sort properties by number of bids (descending)
            sorted_properties = sorted(
                self.properties, key=lambda p: len(bids[p.id]), reverse=True
            )

            for property in sorted_properties:
                if property.is_available() and bids[property.id]:
                    self._assign_property(property, bids[property.id])
                    assignments.append(
                        (
                            property.id,
                            property.assigned_renter,
                            property.max_possible_price,
                        )
                    )

        # Calculate results
        total_revenue = sum(
            p.max_possible_price
            for p in self.properties
            if p.max_possible_price is not None
        )
        total_assignments = len(assignments)
        average_price = (
            total_revenue / total_assignments if total_assignments > 0 else 0
        )

        return SimulationResult(
            total_assignments=total_assignments,
            total_revenue=total_revenue,
            average_price=average_price,
            assignments=assignments,
        )
