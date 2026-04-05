import numpy as np
import pandas as pd

def generate_demand_data(num_products=5, weeks=100, seed=42):
	"""
	Generate simulated demand data with trend, seasonality, noise,
	and external influencing factors.

	Parameters:
	- num_products: number of distinct products
	- weeks: number of time periods
	- seed: random seed for reproducibility

	Returns:
	- pandas DataFrame with demand and external signals
	"""

	# -------------------------------
	# Set random seed for reproducibility
	# -------------------------------
	np.random.seed(seed)

	# Generate product labels (e.g., A, B, C...)
	products = [chr(65 + i) for i in range(num_products)]

	# Container to store all generated data
	data = []

	# -------------------------------
	# Loop through each product
	# -------------------------------
	for p in products:

		# Base demand level (randomized per product)
		base = np.random.randint(20, 50)

		# Linear upward trend over time
		trend = np.linspace(0, 10, weeks)

		# Seasonal pattern (cyclical demand fluctuations)
		seasonality = 10 * np.sin(np.arange(weeks) * 2 * np.pi / 12)

		# Random noise (normal distribution)
		noise = np.random.normal(0, 5, weeks)

		# Combine all components into initial demand signal
		demand = base + trend + seasonality + noise

		# -------------------------------
		# Add higher volatility to selected products
		# -------------------------------
		if p in ['C', 'E']:
			demand += np.random.normal(0, 10, weeks)

		# -------------------------------
		# Generate external signals
		# -------------------------------

		# Supply shock: rare binary event (10% chance)
		supply_shock = np.random.choice([0, 1], size=weeks, p=[0.9, 0.1])

		# Event indicator: promotional or external demand trigger
		event = (np.random.rand(weeks) < 0.1).astype(int)

		# Cost signal: continuous variable (e.g., production cost)
		cost = np.random.normal(50, 5, weeks)

		# -------------------------------
		# Apply external effects to demand
		# -------------------------------
		# - Supply shock reduces demand
		# - Event increases demand
		# - Higher cost slightly reduces demand
		demand = demand * (1 - 0.3 * supply_shock) + 5 * event - 0.2 * cost

		# -------------------------------
		# Store results for each time step
		# -------------------------------
		for t in range(weeks):
			data.append([
				p,						# Product ID
				t,						# Time index (week)
				max(0, demand[t]),		# Demand (non-negative)
				supply_shock[t],		# Supply shock indicator
				event[t],				# Event indicator
				cost[t]					# Cost value
			])

	# -------------------------------
	# Convert to pandas DataFrame
	# -------------------------------
	df = pd.DataFrame(data, columns=[
		'product',
		'week',
		'demand',
		'supply_shock',
		'event',
		'cost'
	])

	return df