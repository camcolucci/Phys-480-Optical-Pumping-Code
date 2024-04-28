from sympy import symbols, Eq, solve

#85/87
slopes = [477.5073245694178, 691.7362061112542,]
Fs = [3, 2]
isotopes = ["85","87"]
for i in range(2):
    slope = slopes[i] # Slope in kHz/Gauss
    mu_B = 1.39962557  # Bohr magneton in MHz/Gauss

    # Conversion of slope from kHz/Gauss to MHz/Gauss
    slope_MHZ = slope / 1000  # Convert kHz to MHz

    g_F = slope_MHZ / mu_B

    # Constants for the atomic state
    g_J = 2.0023  # g_J for electrons
    F = Fs[i]
    J = 1/2

    # Symbol for nuclear spin I
    I = symbols('I', real=True, positive=True)

    # Equation for g_F based on nuclear and electronic spins
    equation = Eq(g_F, g_J * (F*(F+1) + J*(J+1) - I*(I+1)) / (2*F*(F+1)))

    # Solve the equation for I
    I_solution = solve(equation, I)
    print(f"{isotopes[i]}:\ng_F={g_F}\nI={I_solution}")
