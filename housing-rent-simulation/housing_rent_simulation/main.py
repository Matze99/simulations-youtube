import random

import matplotlib.pyplot as plt

from housing_rent_simulation.models.renter import Renter
from housing_rent_simulation.models.property import Property
from housing_rent_simulation.simulation.base import BaseSimulation
from housing_rent_simulation.simulation.scenarios import (
    NoisyFairPriceSimulation,
    ActualFairPriceSimulation,
    NoisyFairPriceWithLandlordScoreSimulation,
    ActualFairPriceWithLandlordScoreSimulation,
)
from housing_rent_simulation.constants import MIN_RENT, MAX_RENT


def generate_random_renters(count: int) -> list[Renter]:
    """Generate a list of random renters."""
    renters = []
    for i in range(count):
        min_price = random.uniform(MIN_RENT, MAX_RENT)
        max_price = random.uniform(min_price * 1.5, min_price * 2.5)
        income = random.uniform(max_price * 2, max_price * 10)
        job_stability = random.uniform(0.5, 1.0)
        renters.append(
            Renter(
                id=i,
                min_price=min_price,
                max_price=max_price,
                income=income,
                job_stability=job_stability,
            )
        )
    return renters


def generate_random_properties(count: int) -> list[Property]:
    """Generate a list of random properties."""
    properties = []
    for i in range(count):
        fair_price = random.uniform(MIN_RENT, MAX_RENT)
        listed_price = random.uniform(fair_price * 0.9, fair_price * 1.1)
        landlord_quality = random.uniform(0.5, 1.0)
        properties.append(
            Property(
                id=i,
                fair_price=fair_price,
                listed_price=listed_price,
                landlord_quality=landlord_quality,
            )
        )
    return properties


def run_simulations(renters: list[Renter], properties: list[Property]) -> None:
    """Run all simulation scenarios and display results."""
    scenarios: list[tuple[str, BaseSimulation]] = [
        (
            "Noisy Fair Price",
            NoisyFairPriceSimulation(renters, properties, noise_level=0.1),
        ),
        ("Actual Fair Price", ActualFairPriceSimulation(renters, properties)),
        (
            "Noisy Fair Price + Landlord Score",
            NoisyFairPriceWithLandlordScoreSimulation(
                renters, properties, noise_level=0.1
            ),
        ),
        (
            "Actual Fair Price + Landlord Score",
            ActualFairPriceWithLandlordScoreSimulation(renters, properties),
        ),
    ]

    print("\nHousing Rent Simulation Results")
    print("=" * 50)

    figure = plt.figure(figsize=(15, 10))
    figure.suptitle(
        "Landlord Quality vs Average Rank Across Different Scenarios", fontsize=16
    )

    for idx, (name, simulation) in enumerate(scenarios, 1):
        result = simulation.get_average_rank()

        # landlord score vs average rank
        landlord_scores, average_ranks = [], []
        for _id, avg_rank in result.items():
            landlord_scores.append(simulation.properties_map[_id].landlord_quality)
            average_ranks.append(avg_rank)

        # Create subplot
        ax = figure.add_subplot(2, 2, idx)
        ax.scatter(landlord_scores, average_ranks, alpha=0.6)
        ax.set_title(name)
        ax.set_xlabel("Landlord Quality Score")
        ax.set_ylabel("Average Rank")
        ax.grid(True, alpha=0.3)

        # print(f"\n{name}")
        # print("-" * 30)
        # print(f"Total Assignments: {result.total_assignments}")
        # print(f"Total Revenue: ${result.total_revenue:,.2f}")
        # print(f"Average Price: ${result.average_price:,.2f}")

        # # Print some example assignments
        # print("\nExample Assignments:")
        # for assignment in result.assignments[:3]:
        #     print(
        #         f"Property {assignment.property_id} -> Renter {assignment.renter_id} at ${assignment.price:,.2f}"
        #     )

    plt.tight_layout()
    plt.show()


def main():
    """Main entry point for the simulation."""
    # Generate random renters and properties
    renters = generate_random_renters(200)
    properties = generate_random_properties(160)

    # Run all simulation scenarios
    run_simulations(renters, properties)


if __name__ == "__main__":
    main()
