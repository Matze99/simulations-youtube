import random
from typing import List
from housing_rent_simulation.models.renter import Renter
from housing_rent_simulation.models.property import Property
from housing_rent_simulation.simulation.scenarios import (
    NoisyFairPriceSimulation,
    ActualFairPriceSimulation,
    NoisyFairPriceWithLandlordScoreSimulation,
    ActualFairPriceWithLandlordScoreSimulation,
)


def generate_random_renters(count: int) -> List[Renter]:
    """Generate a list of random renters."""
    renters = []
    for i in range(count):
        min_price = random.uniform(500, 1000)
        max_price = random.uniform(min_price * 1.5, min_price * 2.5)
        income = random.uniform(max_price * 10, max_price * 20)
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


def generate_random_properties(count: int) -> List[Property]:
    """Generate a list of random properties."""
    properties = []
    for i in range(count):
        fair_price = random.uniform(800, 2000)
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


def run_simulations(renters: List[Renter], properties: List[Property]) -> None:
    """Run all simulation scenarios and display results."""
    scenarios = [
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

    for name, simulation in scenarios:
        result = simulation.run_simulation()
        print(f"\n{name}")
        print("-" * 30)
        print(f"Total Assignments: {result.total_assignments}")
        print(f"Total Revenue: ${result.total_revenue:,.2f}")
        print(f"Average Price: ${result.average_price:,.2f}")

        # Print some example assignments
        print("\nExample Assignments:")
        for prop_id, renter_id, price in result.assignments[:3]:
            print(f"Property {prop_id} -> Renter {renter_id} at ${price:,.2f}")


def main():
    """Main entry point for the simulation."""
    # Generate random renters and properties
    renters = generate_random_renters(100)
    properties = generate_random_properties(50)

    # Run all simulation scenarios
    run_simulations(renters, properties)


if __name__ == "__main__":
    main()
