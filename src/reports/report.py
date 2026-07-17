import numpy as np
import matplotlib.pyplot as plt

def test_report():
    # 1. Create data using NumPy
    x = np.linspace(0, 10, 100)  # 100 evenly spaced points between 0 and 10
    y = np.sin(x)                # Compute the sine of each point

    # 2. Plot the graph
    plt.plot(x, y, label="Sine Wave")

    # 3. Add details
    plt.title("My First NumPy Plot")
    plt.xlabel("X Axis")
    plt.ylabel("Y Axis")
    plt.grid(True)
    plt.legend()

    # 4. Display the graph
    plt.show()