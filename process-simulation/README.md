# Chemical Reaction Kinetics Simulation

This project simulates the concentration changes of chemical species over time in a series of reactions. It uses the `odeint` function from the SciPy library to solve a system of differential equations derived from the reaction kinetics. The reactions are modeled using mass-action kinetics, and the concentrations are analyzed as a function of time.

## Assumptions:
1. Volume of Reactor = 10 litres
2. K = 1.5
3. K = k1/k2; k3/k4; k5/k6
4. The value of Activation Energy (Ea) and molar flow rate also an assumption
5. Data taken every 10 minutes for 3 hours (180 Minutes). This value can be modified with your needs.

## Reactions Considered

The chemical reactions considered in this simulation are:

1. **Reaction 1:**
   $\{
   2A + B \leftrightarrow C
   \}$

2. **Reaction 2:**
   $\{
   C + D \leftrightarrow 3E
   \}$

3. **Reaction 3:**
   $\{
   E + A \leftrightarrow 4F
   \}$

These reactions include both forward and reverse processes, governed by rate constants.

## Differential Equations

The rate of change of concentration for each species _A_, _B_, _C_, _D_, _E_, and _F_ is determined by the following differential equations:

$\{
\frac{d[A]}{dt} = -2k_{1f} [A]^2 [B] + 2k_{1r} [C] - k_{3f} [E] [A] + k_{3r} [F]^4
\}$

$\{
\frac{d[B]}{dt} = -k_{1f} [A]^2 [B] + k_{1r} [C]
\}$

$\{
\frac{d[C]}{dt} = k_{1f} [A]^2 [B] - k_{1r} [C] - k_{2f} [C] [D] + k_{2r} [E]^3
\}$

$\{
\frac{d[D]}{dt} = -k_{2f} [C] [D] + k_{2r} [E]^3
\}$

$\{
\frac{d[E]}{dt} = 3k_{2f} [C] [D] - 3k_{2r} [E]^3 - k_{3f} [E] [A] + k_{3r} [F]^4
\}$

$\{
\frac{d[F]}{dt} = k_{3f} [E] [A] - k_{3r} [F]^4
\}$

## Project Structure

- `concentration-over-time.py`: Contains the primary code for setting up the simulation, defining the differential equations, and running the solver.
- `README.md`: This document, providing an overview and instructions.

## Running the Simulation

To run the simulation and plot the concentration profiles:

1. Ensure your environment is activated.
2. Run the script:
   ```sh
   python concentration-over-time.py
   ```

The output will include a plot showing the concentration of each species over time.

## Dependencies

- Python 3.10
- NumPy
- SciPy
- Matplotlib

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
