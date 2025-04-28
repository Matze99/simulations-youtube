# Housing Rent Simulation

This project simulates different scenarios of housing rental markets where
renters and landlords interact under various information conditions.

## Overview

The simulation models a housing market with the following key components:

- **Renters**: Each renter has:
  - Minimum and maximum price they can pay
  - Income level
  - Job stability score

- **Properties**: Each property has:
  - Fair market price
  - Listed price
  - Landlord quality score

## Desired Outcome

For each scenario, the simulation should determine the average rank assinged by
the renter to the property in relation to the rank of the property.

The

## Simulation Scenarios

The simulation runs through four different scenarios where renters have varying
levels of information:

1. **Noisy Fair Price**: Renters see a noisy estimate of the fair price
2. **Actual Fair Price**: Renters see the exact fair price
3. **Noisy Fair Price + Landlord Score**: Renters see a noisy fair price
   combined with landlord quality score
4. **Actual Fair Price + Landlord Score**: Renters see the exact fair price
   combined with landlord quality score

## Simulation Process

In each simulation:

1. Renters rank properties they can afford based on available information and
   bid on them
2. For each property calculate the average rank

3. Each renter is ranked for every property they bid on
4. assign renters and properties to minimize the proerty and renter ranks

## Installation

```bash
pip install -e .
```

## Running the Simulation

```bash
python -m housing_rent_simulation.main
```

## Running Tests

```bash
pytest tests/
```

## Project Structure

```
housing_rent_simulation/
├── __init__.py
├── models/
│   ├── __init__.py
│   ├── renter.py
│   └── property.py
├── simulation/
│   ├── __init__.py
│   ├── base.py
│   └── scenarios.py
└── main.py
tests/
├── __init__.py
├── test_models.py
└── test_simulation.py
```
