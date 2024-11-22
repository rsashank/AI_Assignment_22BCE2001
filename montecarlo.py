import numpy as np
import matplotlib.pyplot as plt

P_A = {"yes": 0.8, "no": 0.2}
P_C = {"yes": 0.5, "no": 0.5}
P_G_given_A_C = {
    ("yes", "yes"): {"Good": 0.9, "OK": 0.1},
    ("yes", "no"): {"Good": 0.7, "OK": 0.3},
    ("no", "yes"): {"Good": 0.6, "OK": 0.4},
    ("no", "no"): {"Good": 0.3, "OK": 0.7},
}
P_J_given_G = {
    "Good": {"yes": 0.8, "no": 0.2},
    "OK": {"yes": 0.2, "no": 0.8},
}
P_S_given_G = {
    "Good": {"yes": 0.7, "no": 0.3},
    "OK": {"yes": 0.3, "no": 0.7},
}

def monte_carlo_simulation(target_query, evidence, num_samples=10000):
    count_target_true = 0
    count_evidence_satisfied = 0

    for _ in range(num_samples):
        aptitude = "yes" if np.random.rand() < P_A["yes"] else "no"
        coding = "yes" if np.random.rand() < P_C["yes"] else "no"
        
        grade_probs = P_G_given_A_C[(aptitude, coding)]
        grade = "Good" if np.random.rand() < grade_probs["Good"] else "OK"
        
        job_probs = P_J_given_G[grade]
        job = "yes" if np.random.rand() < job_probs["yes"] else "no"
        
        startup_probs = P_S_given_G[grade]
        startup = "yes" if np.random.rand() < startup_probs["yes"] else "no"
        
        node_states = {"A": aptitude, "C": coding, "G": grade, "J": job, "S": startup}
        
        if all(node_states[key] == value for key, value in evidence.items()):
            count_evidence_satisfied += 1
            if node_states[target_query] == "yes":
                count_target_true += 1

    if count_evidence_satisfied == 0:
        return 0

    return count_target_true / count_evidence_satisfied

def convergence_analysis(actual_value, evidence, target_query):
    sample_sizes = np.logspace(2, 5, num=15, dtype=int)
    results = []

    print(f"Actual Value: {actual_value:.3f}\n")
    print("Convergence Analysis:")

    for num_samples in sample_sizes:
        estimated_value = monte_carlo_simulation(target_query, evidence, num_samples)
        closeness = (1 - abs(estimated_value - actual_value) / actual_value) * 100
        results.append((num_samples, estimated_value))
        print(f"With {num_samples} samples: P({target_query}=True | Evidence) ≈ {estimated_value:.3f}, Closeness: {closeness:.2f}%")

    x, y = zip(*results)
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, marker="o", label="Estimated Probability")
    plt.axhline(y=actual_value, color="r", linestyle="--", label="Actual Probability")
    plt.xscale("log")
    plt.xlabel("Number of Samples (log scale)")
    plt.ylabel(f"P({target_query}=True | Evidence)")
    plt.title("Convergence Analysis of Monte Carlo Simulation")
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    P_actual = (
        P_G_given_A_C[("yes", "yes")]["Good"] * P_S_given_G["Good"]["yes"]
        + P_G_given_A_C[("yes", "yes")]["OK"] * P_S_given_G["OK"]["yes"]
    )

    convergence_analysis(actual_value=P_actual, evidence={"A": "yes", "C": "yes"}, target_query="S")
