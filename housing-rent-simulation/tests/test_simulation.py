import pytest
from housing_rent_simulation.models.renter import Renter
from housing_rent_simulation.models.property import Property
from housing_rent_simulation.simulation.scenarios import (
    NoisyFairPriceSimulation,
    ActualFairPriceSimulation,
    NoisyFairPriceWithLandlordScoreSimulation,
    ActualFairPriceWithLandlordScoreSimulation,
)


@pytest.fixture
def sample_renters():
    """Create sample renters for testing."""
    return [
        Renter(id=1, min_price=1000, max_price=2000, income=50000, job_stability=0.8),
        Renter(id=2, min_price=1500, max_price=2500, income=60000, job_stability=0.9),
        Renter(id=3, min_price=800, max_price=1800, income=40000, job_stability=0.7),
    ]


@pytest.fixture
def sample_properties():
    """Create sample properties for testing."""
    return [
        Property(id=1, fair_price=1500, listed_price=1600, landlord_quality=0.9),
        Property(id=2, fair_price=2000, listed_price=2100, landlord_quality=0.8),
        Property(id=3, fair_price=1200, listed_price=1300, landlord_quality=0.7),
    ]


def test_noisy_fair_price_simulation(sample_renters, sample_properties):
    """Test the noisy fair price simulation."""
    simulation = NoisyFairPriceSimulation(
        sample_renters, sample_properties, noise_level=0.1
    )
    result = simulation.run_simulation()

    assert result.total_assignments > 0
    assert result.total_revenue > 0
    assert result.average_price > 0
    assert len(result.assignments) == result.total_assignments


def test_actual_fair_price_simulation(sample_renters, sample_properties):
    """Test the actual fair price simulation."""
    simulation = ActualFairPriceSimulation(sample_renters, sample_properties)
    result = simulation.run_simulation()

    assert result.total_assignments > 0
    assert result.total_revenue > 0
    assert result.average_price > 0
    assert len(result.assignments) == result.total_assignments


def test_noisy_fair_price_with_landlord_score(sample_renters, sample_properties):
    """Test the noisy fair price with landlord score simulation."""
    simulation = NoisyFairPriceWithLandlordScoreSimulation(
        sample_renters, sample_properties, noise_level=0.1
    )
    result = simulation.run_simulation()

    assert result.total_assignments > 0
    assert result.total_revenue > 0
    assert result.average_price > 0
    assert len(result.assignments) == result.total_assignments


def test_actual_fair_price_with_landlord_score(sample_renters, sample_properties):
    """Test the actual fair price with landlord score simulation."""
    simulation = ActualFairPriceWithLandlordScoreSimulation(
        sample_renters, sample_properties
    )
    result = simulation.run_simulation()

    assert result.total_assignments > 0
    assert result.total_revenue > 0
    assert result.average_price > 0
    assert len(result.assignments) == result.total_assignments


def test_simulation_comparison(sample_renters, sample_properties):
    """Compare results across different simulation scenarios."""
    scenarios = [
        NoisyFairPriceSimulation(sample_renters, sample_properties, noise_level=0.1),
        ActualFairPriceSimulation(sample_renters, sample_properties),
        NoisyFairPriceWithLandlordScoreSimulation(
            sample_renters, sample_properties, noise_level=0.1
        ),
        ActualFairPriceWithLandlordScoreSimulation(sample_renters, sample_properties),
    ]

    results = [sim.run_simulation() for sim in scenarios]

    # All simulations should produce some assignments
    assert all(r.total_assignments > 0 for r in results)

    # The actual price simulations should generally have higher revenue
    # (since they have perfect information)
    assert results[1].total_revenue >= results[0].total_revenue
    assert results[3].total_revenue >= results[2].total_revenue
