import pytest
from housing_rent_simulation.models.renter import Renter
from housing_rent_simulation.models.property import Property


def test_renter_creation():
    """Test renter creation and basic properties."""
    renter = Renter(
        id=1, min_price=1000, max_price=2000, income=50000, job_stability=0.8
    )

    assert renter.id == 1
    assert renter.min_price == 1000
    assert renter.max_price == 2000
    assert renter.income == 50000
    assert renter.job_stability == 0.8
    assert renter.assigned_property is None


def test_renter_can_afford():
    """Test renter's ability to afford different prices."""
    renter = Renter(
        id=1, min_price=1000, max_price=2000, income=50000, job_stability=0.8
    )

    assert renter.can_afford(1500) is True
    assert renter.can_afford(500) is False
    assert renter.can_afford(2500) is False
    assert renter.can_afford(1000) is True
    assert renter.can_afford(2000) is True


def test_property_creation():
    """Test property creation and basic properties."""
    property = Property(id=1, fair_price=1500, listed_price=1600, landlord_quality=0.9)

    assert property.id == 1
    assert property.fair_price == 1500
    assert property.listed_price == 1600
    assert property.landlord_quality == 0.9
    assert property.assigned_renter is None
    assert property.max_possible_price is None


def test_property_validation():
    """Test property attribute validation."""
    # Test invalid landlord quality
    with pytest.raises(ValueError):
        Property(id=1, fair_price=1500, listed_price=1600, landlord_quality=1.5)

    # Test invalid prices
    with pytest.raises(ValueError):
        Property(id=1, fair_price=-100, listed_price=1600, landlord_quality=0.9)

    with pytest.raises(ValueError):
        Property(id=1, fair_price=1500, listed_price=-100, landlord_quality=0.9)


def test_property_assignment():
    """Test property assignment to renters."""
    property = Property(id=1, fair_price=1500, listed_price=1600, landlord_quality=0.9)

    assert property.is_available() is True

    property.assign_renter(renter_id=1, price=1700)

    assert property.is_available() is False
    assert property.assigned_renter == 1
    assert property.max_possible_price == 1700

    # Test double assignment
    with pytest.raises(ValueError):
        property.assign_renter(renter_id=2, price=1800)


def test_property_observed_price():
    """Test property's observed price calculation."""
    property = Property(id=1, fair_price=1500, listed_price=1600, landlord_quality=0.9)

    # Test without noise
    assert property.get_observed_price() == 1500

    # Test with noise (we can't predict the exact value, but it should be different)
    observed_price = property.get_observed_price(noise_level=0.1)
    assert observed_price != 1500
    # The noise should be within reasonable bounds
    assert 1350 <= observed_price <= 1650
