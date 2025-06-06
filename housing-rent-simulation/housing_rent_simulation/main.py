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
from housing_rent_simulation.constants import MIN_RENT, MAX_RENT, MIN_INCOME, MAX_INCOME


def generate_random_renters(count: int) -> list[Renter]:
    """Generate a list of random renters."""
    renters = []
    for i in range(count):
        min_price = MIN_RENT
        income = random.uniform(MIN_INCOME, MAX_INCOME)
        max_price = income / 3
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
        landlord_quality = random.uniform(0.0, 1.0)
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

    # Create two figures
    figure1 = plt.figure(figsize=(15, 10))
    figure1.suptitle(
        "Landlord Quality vs Average Rank Across Different Scenarios", fontsize=16
    )

    figure2 = plt.figure(figsize=(15, 10))
    figure2.suptitle(
        "Landlord Quality vs Maximum Possible Rent Across Different Scenarios",
        fontsize=16,
    )

    for idx, (name, simulation) in enumerate(scenarios, 1):
        # Run the simulation to get assignments
        result = simulation.match_renters_to_properties()

        # Get average ranks
        avg_ranks = simulation.get_average_rank()

        # landlord score vs average rank
        landlord_scores, average_ranks = [], []
        for _id, avg_rank in avg_ranks.items():
            landlord_scores.append(simulation.properties_map[_id].landlord_quality)
            average_ranks.append(avg_rank)

        # Create subplot for rank vs quality
        ax1 = figure1.add_subplot(2, 2, idx)
        ax1.scatter(landlord_scores, average_ranks, alpha=0.6)
        ax1.set_title(name)
        ax1.set_xlabel("Landlord Quality Score")
        ax1.set_ylabel("Average Rank")
        ax1.grid(True, alpha=0.3)

        # landlord score vs max possible rent
        landlord_scores, max_rents = [], []
        combined_results = []
        for assignment in result.assignments:
            _property = simulation.properties_map[assignment.property_id]
            renter = simulation.renters_map[assignment.renter_id]
            combined_results.append((_property.landlord_quality, renter.max_price))
        combined_results.sort(key=lambda x: x[0])
        landlord_scores, max_rents = zip(*combined_results)

        # Create subplot for max rent vs quality
        ax2 = figure2.add_subplot(2, 2, idx)
        ax2.plot(landlord_scores, max_rents, alpha=0.6)
        ax2.set_title(name)
        ax2.set_xlabel("Landlord Quality Score")
        ax2.set_ylabel("Maximum Possible Rent ($)")
        ax2.grid(True, alpha=0.3)

    plt.figure(figure1.number)
    plt.tight_layout()
    plt.figure(figure2.number)
    plt.tight_layout()
    plt.show()


def run_debug():
    renters = [
        Renter(id=0, min_price=1000, max_price=3000, income=10000, job_stability=0.5),
        Renter(id=1, min_price=1000, max_price=3000, income=10000, job_stability=0.5),
        Renter(id=2, min_price=1000, max_price=9000, income=20000, job_stability=0.5),
    ]
    properties = [
        Property(id=0, fair_price=3000, listed_price=3000, landlord_quality=0),
        Property(id=1, fair_price=1500, listed_price=1500, landlord_quality=1),
    ]

    simulation = ActualFairPriceWithLandlordScoreSimulation(renters, properties)
    result = simulation.match_renters_to_properties()

    for assignment in result.assignments:
        renter = simulation.renters_map[assignment.renter_id]
        _property = simulation.properties_map[assignment.property_id]
        print(
            f"assigning renter {assignment.renter_id} to property {assignment.property_id}: {renter.max_price} - {_property.landlord_quality}"
        )


def run_debug2():
    renters = generate_random_renters(100)
    properties = generate_random_properties(100)

    simulation = ActualFairPriceWithLandlordScoreSimulation(renters, properties)
    result = simulation.match_renters_to_properties()

    values = []
    for assignment in result.assignments:
        renter = simulation.renters_map[assignment.renter_id]
        _property = simulation.properties_map[assignment.property_id]
        values.append(
            (renter.id, _property.id, renter.max_price, _property.landlord_quality)
        )

    values.sort(key=lambda x: x[3])
    for renter_id, property_id, max_price, landlord_quality in values:
        print(
            f"assigning renter {renter_id} to property {property_id}: {max_price} - {landlord_quality}"
        )


def main():
    """Main entry point for the simulation."""
    # Generate random renters and properties
    renters = generate_random_renters(200)
    properties = generate_random_properties(180)

    # Run all simulation scenarios
    run_simulations(renters, properties)


if __name__ == "__main__":
    # run_debug()
    # run_debug2()
    main()
