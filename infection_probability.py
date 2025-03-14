import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Fixed sensitivity
sensitivity = 0.99

# Define prevalence values (from 0.001% to 50%)
prevalence_values = np.linspace(0.00001, 0.5, 500)  # Convert to fraction

# Define specificity values
specificity_values = [0.99, 0.999, 0.9999, 0.99999]  # 99%, 99.9%, 99.99%, 99.999%

# Function to compute probability of infection given a positive test using Bayes' Theorem
def bayes_theorem(prevalence, sensitivity, specificity):
    false_positive_rate = 1 - specificity
    P_positive = (sensitivity * prevalence) + (false_positive_rate * (1 - prevalence))
    P_infected_given_positive = (sensitivity * prevalence) / P_positive
    return P_infected_given_positive

# Compute results for different specificities
results = {}
for specificity in specificity_values:
    probabilities = [bayes_theorem(prev, sensitivity, specificity) for prev in prevalence_values]
    results[f"Specificity {specificity*100:.3f}%"] = probabilities

# Convert to DataFrame for easy export and visualization
df = pd.DataFrame(results, index=prevalence_values)
df.index.name = "Prevalence"

# Visualization
plt.figure(figsize=(10, 6))
for specificity, probabilities in results.items():
    plt.plot(prevalence_values * 100, probabilities, label=specificity)

plt.xlabel("Infection Prevalence (%)")
plt.ylabel("P(Infected | Positive Test)")
plt.title("Probability of Infection Given a Positive Test")
plt.legend()
plt.grid()
plt.show()
