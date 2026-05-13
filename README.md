# AP Physics C: Mechanics — TI-Nspire CX II / CX II CAS Python Solver

Python port of the [TI-Nspire TI-BASIC solver](https://github.com/ChasesClaw/AP_Physics_C_TI_Nspire) for the Python app on the **TI-Nspire CX II** family (CX II, CX II CAS, CX II-T). Same chained-solver design, same equation coverage, same FRQ-extra additions as the TI-84 port (rolling `v`, spring `x` inversion, second derivative at a point).

One file:

- [physc.py](physc.py) — the program

## Install (Student Software or handheld)

**Requires:** TI-Nspire OS 5.2 or later. Check via `doc → Settings → Status` on the handheld, or `Help → About` in the Student Software. If you don't see "Add Python" in the page-type list, update from [education.ti.com → Downloads](https://education.ti.com).

1. Open the TI-Nspire CX II CAS Student Software.
2. Create a new document.
3. `doc → Insert → Add Python → New…`
4. Name it `physc`, type = Python.
5. Paste the full contents of `physc.py` into the editor.
6. Press the **Run** button (or `ctrl+R`).
7. The Python Shell opens. The main menu prints immediately.

You can also save the document; the Python file lives inside the TNS file.

## Why this over the TI-BASIC version on the same calculator

The TI-BASIC version (`physc_chained_solver.ti.txt`) works fine after the Local-cap fix, but the Python version has real advantages on the same hardware:

- No `Local` cap, no `Menu` line limits, no special-character paste issues. Paste-and-go.
- Chained solver routes are actual function returns instead of `Goto`/`Lbl` dispatch — readable and easier to extend.
- Bundles the three FRQ extras that the TI-BASIC version doesn't have:
  - Kinematics → rolling v(h) — solves `mgh = ½mv² + ½Iω²` with the rolling constraint in one shot
  - Energy → x from spring U — inverts `(½)kx² = U` for x
  - Calculus → d²/du² f(u) at t — one-step second derivative

## Usage rules

- **SI units only.**
- **Angles in radians.** Numeric prompts accept expressions such as `pi`, `pi/6`, and `2*pi`.
- **Function entries use `u`.** Examples: `3u+5`, `3*u**2+4`, `sin(2u)`, `exp(-u)`. Allowed names: `u, sin, cos, tan, asin, acos, atan, sqrt, exp, pi, g`.
- **Implicit multiplication is accepted.** `3u`, `2pi`, `2sin(u)`, and `(u+1)(u-1)` are converted automatically.
- **Sign prompts.** When the program asks `sgn 1=+,-1=-:` for ± square-root branches, type `-1` for the negative root, anything else (including blank) for `+`.

## Main menu

1. Smart solver — solve from givens, solve one target, derivation guidance, or backward proof
2. Full equation menus — opens the older topic menus
3. Quit

### Smart solver

All-from-givens mode can either prompt you through a variable list or accept known values on one line. For the guided prompts, type a number, a symbol, or leave the prompt blank if that value is unknown. For the one-line input, type comma-separated knowns and then press Enter on a blank line when done:

```
m=5,v0=0,a=2,t=4
```

It also accepts symbolic givens such as:

```
mass=m,k=k,x=x
```

Then it chains through common Mechanics equations. If the values are numeric, it prints computed answers. If some values are symbols, it prints formula paths it can build from the givens. Use `Wnc` for nonconservative work.

Solve-one-target mode asks what variable you want. You can type targets like `v`, `a`, `x`, `F`, `force`, `W`, `K`, `p`, `T`, or `period`. It then shows each possible path with the required inputs, such as `Newton 2nd law: Fnet=m*a need m,a`. After you choose a path, enter numbers like `5` or `pi/6`, symbols like `m`, or press Enter if the value is unknown. If a needed value is unknown, the program tries to solve that missing value first before returning to the original target.

Derivation mode asks for givens/keywords and a goal. Use plain words or variables, for example `spring compressed x, mass m`, `collision, objects stick`, `rolling disk from height h`, or `force-time graph, impulse J`. Goal examples include `derive speed`, `find graph slope`, `compare periods`, `show vf`, or `show friction distance`. It then suggests useful principle paths such as energy, momentum/impulse, graph linearization, rolling constraints, oscillation proportionality, and MCQ checks.

Backward proof mode asks for a given answer/expression, such as `d=h/mu` or `v=x*sqrt(k/m)`, plus an optional plain-language problem type. It matches common AP Mechanics forms and prints the steps that connect the givens to that answer.

### Full equation menus

1. Kinematics — v, x, a, t, projectile, **rolling v(h)**
2. Forces — Fnet, normal, friction, incline, spring, Atwood, banking, loop, drag
3. Energy/Work/Power — W, K, U_g, U_s, P, work–KE, conservation, rolling K, **x from spring U**
4. Momentum — p, J, vf, CoM (n=2–4), v_cm, elastic, inelastic, restitution, F=dp/dt
5. Rotation — I (8 shapes), τ, α, angular kinematics, circular motion, K_rot, L, conservation of L
6. Oscillations — spring, pendulum, physical pendulum, ω, x(t), v(t), a(t), vmax/amax, energy
7. Gravitation — F, g, U, v_orbit, T_orbit, v_esc, total bound-orbit energy
8. Calculus tools — ∫F(t)dt, ∫F(x)dx, ∫F(t)v(t)dt, ∫a(t)dt, ∫v(t)dt, df/du, **d²f/du²**, U from F, F from U
9. Derivation helpers — reusable symbolic setup, graph, and MCQ reasoning patterns
10. Back

## How chained solving works

When an equation needs `a` or `I` you haven't entered, the program calls `get_a()` or `get_I()` which open a sub-menu of every way to find that variable, run the side calculation, print the intermediate value, and return it to the caller. The caller plugs it back in.

Example for `v² = v0² + 2a(x−x0)` when you don't know `a`:

```
Kinematics > Find v > v^2=v0^2+2adx
v0: 0
x0: 0
x: 4
[get_a menu]
> incline
theta rad: 0.5236
mu: 0.2
a = 3.20
sgn 1=+,-1=-: 1
dx = 4
v = 5.06
```

## Numerical accuracy

- `nint`: Simpson's rule with 120 intervals (smooth integrands hit ~10⁻⁶ relative error).
- `dfx`: central difference, h = 1e-4.
- `d2fx`: centered second difference, h = 1e-3.

## Compared with the CAS-edition TI-BASIC version

| | TI-BASIC (.ti.txt) | Python (.py) |
|---|---|---|
| Symbolic CAS (`solve`, `d()`) | Yes (CAS only) | No — numerical |
| Rolling v from height | No | Yes |
| Spring x from U | No | Yes |
| Second derivative | No | Yes (numerical) |
| Paste-fragility | Local cap, menu limits, char encoding | None |
| Available on non-CAS Nspire CX II | No | **Yes** |

If you have the CAS edition and want exact symbolic answers for the quadratic-time and projectile-from-height problems, the TI-BASIC version's `solve()` calls are still the cleanest path for those specific routes. For everything else, the Python version is faster and more reliable.

## Limits

- Vectors stay 1D — project onto axes yourself.
- Derivation helpers are formula/setup guidance tools, not full written derivations. AP graders still need your handwritten algebra and reasoning.
- `eval` inside `mkf()` is sandboxed to math names only.
