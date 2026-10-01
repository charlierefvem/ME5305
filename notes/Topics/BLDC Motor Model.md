---
title: BLDC Motor Model
type: topic
tags:
  - ME5305
  - BLDC
  - modeling
source:
  course: ME5305
  legacy: Legacy Overleaf Derivation/ch2_simple_bldc.tex
status: publication-ready
---

This note extends the one-phase thought experiment in [[Motor Theory Fundamentals]] to a deliberately simple three-phase model. The model is detailed enough to reason about terminal voltage, phase current, back-EMF, torque, and driver selection without becoming a full machine-design model.

## Model Assumptions

Unless stated otherwise, assume:

- a sinusoidal-back-EMF permanent-magnet synchronous motor,
- one rotor pole pair, so $\theta_e=\theta_m$ and $\omega_e=\omega_m$,
- three identical stator phases displaced by $120^\circ$ electrical,
- a balanced wye connection with a defined conceptual neutral point that need not be externally accessible,
- constant per-phase resistance $R_s$ and inductance $L_s$,
- negligible mutual inductance, saliency, magnetic saturation, and iron loss, and
- phase-to-neutral voltages and phase currents unless a different quantity is named explicitly.

These assumptions are teaching approximations. They are not a claim that all commercial motors have identical parameters or perfectly sinusoidal waveforms.

## Three-Phase Geometry

The three stator magnetic axes are separated by $120^\circ$ electrical. With the phase sequence $a$-$b$-$c$, the permanent-magnet flux linkages can be represented as

$$
\begin{aligned}
\lambda_{\mathrm{pm},a} &= \psi_m\cos\theta_e,\\
\lambda_{\mathrm{pm},b} &= \psi_m\cos\left(\theta_e-\frac{2\pi}{3}\right),\\
\lambda_{\mathrm{pm},c} &= \psi_m\cos\left(\theta_e+\frac{2\pi}{3}\right).
\end{aligned}
$$

> [!figure] Figure 1
> ![Cross-sectional view of an idealized three-phase permanent-magnet motor.](images/BLDC/PMSM_model_three_phase.pdf)
>
> *Idealized three-phase permanent-magnet motor with phase axes separated by $120^\circ$ electrical. The figure assumes one pole pair, so $\theta_e=\theta_m$.*

Differentiating the flux linkages gives the three-phase back-EMFs:

$$
\begin{aligned}
e_a &=-\psi_m\omega_e\sin\theta_e,\\
e_b &=-\psi_m\omega_e\sin\left(\theta_e-\frac{2\pi}{3}\right),\\
e_c &=-\psi_m\omega_e\sin\left(\theta_e+\frac{2\pi}{3}\right).
\end{aligned}
$$

As defined in [[Motor Theory Fundamentals]], the phase-peak back-EMF constant referenced to mechanical speed is $K_e=p\psi_m$. Thus $K_e=\psi_m$ for the one-pole-pair model used here.

## Per-Phase Electrical Model

Each phase is modeled as a series resistance, inductance, and speed-dependent back-EMF source:

$$
v_{xn}=R_s i_x+L_s\frac{di_x}{dt}+e_x,
\qquad x\in\{a,b,c\}.
$$

The subscript $n$ denotes the motor neutral point. A three-phase inverter controls the terminal-node voltages relative to its own reference, not the phase-to-neutral voltages $v_{xn}$ directly. The distinction matters when the motor neutral is not externally connected.

> [!figure] Figure 2
> ![Complete per-phase equivalent circuit and its corresponding lumped winding representation.](images/BLDC/phase_equiv_circuit.pdf)
>
> *Complete per-phase equivalent circuit (left) and corresponding lumped winding representation (right). The lumped symbol represents the full terminal behavior of $R_s$, $L_s$, and $e_x$; it is not an ideal inductor.*

The three equations are

$$
\begin{aligned}
v_{an}&=R_s i_a+L_s\frac{di_a}{dt}+e_a,\\
v_{bn}&=R_s i_b+L_s\frac{di_b}{dt}+e_b,\\
v_{cn}&=R_s i_c+L_s\frac{di_c}{dt}+e_c.
\end{aligned}
$$

### Wye Connection

> [!figure] Figure 3
> ![Balanced three-wire wye connection showing terminal and neutral node potentials and positive phase-current directions.](images/BLDC/wye.pdf)
>
> *Balanced three-wire wye connection. The quantities $v_a$, $v_b$, $v_c$, and $v_n$ are node potentials measured relative to a common reference. Positive phase current is directed from each motor terminal toward the shared neutral node $n$.*

The phase-to-neutral voltages are therefore

$$
v_{an}=v_a-v_n,
\qquad
v_{bn}=v_b-v_n,
\qquad
v_{cn}=v_c-v_n.
$$

For a balanced three-wire wye connection,

$$
i_a+i_b+i_c=0.
$$

Line current equals winding current in a wye connection. The line-to-line terminal voltages are differences between terminal-node potentials; for example,

$$
v_{ab}=v_a-v_b=v_{an}-v_{bn}.
$$

## Torque from Three-Phase Power

The instantaneous converted power is

$$
p_{\mathrm{conv}}=e_a i_a+e_b i_b+e_c i_c=T_e\omega_m.
$$

Choose balanced sinusoidal currents aligned with the back-EMFs, where $\hat I>0$ is their common peak magnitude:

$$
\begin{aligned}
i_a &=-\hat I\sin\theta_e,\\
i_b &=-\hat I\sin\left(\theta_e-\frac{2\pi}{3}\right),\\
i_c &=-\hat I\sin\left(\theta_e+\frac{2\pi}{3}\right).
\end{aligned}
$$

Substituting the phase back-EMFs and currents gives

$$
\begin{aligned}
p_{\mathrm{conv}}
&=\psi_m\omega_e\hat I\left[
\sin^2\theta_e+
\sin^2\left(\theta_e-\frac{2\pi}{3}\right)+
\sin^2\left(\theta_e+\frac{2\pi}{3}\right)
\right]\\
&=\frac{3}{2}\psi_m\omega_e\hat I.
\end{aligned}
$$

Although the main geometry uses $p=1$, restoring the general relationship $\omega_e=p\omega_m$ at this point gives the electromagnetic torque

$$
T_e=\frac{3}{2}p\psi_m\hat I=\frac{3}{2}K_e\hat I.
$$

Thus an ideal balanced sinusoidal current set produces constant electromagnetic torque. The factor $3/2$ belongs to the phase-peak definitions used here; it must not be copied into a calculation that uses a different current or back-EMF convention.

## Mechanical Motion

When acceleration matters, a minimal mechanical model is

$$
J\frac{d\omega_m}{dt}=T_e-T_L-b\omega_m,
$$

$$
\frac{d\theta_m}{dt}=\omega_m,
$$

where $J$ is combined rotor-and-load inertia, $T_L$ is load torque, and $b$ is a simple viscous-friction coefficient. This lecture sequence does not attempt a detailed friction, compliance, thermal, or load model.

## Delta Connection

> [!figure] Figure 4
> ![Balanced three-wire delta connection showing terminal-node potentials, line currents, and winding currents.](images/BLDC/delta.pdf)
>
> *Balanced three-wire delta connection. The quantities $v_u$, $v_v$, and $v_w$ are terminal-node potentials measured relative to a common reference. The line currents $i_u$, $i_v$, and $i_w$ are positive into the motor, while winding currents $i_a$, $i_b$, and $i_c$ follow the directions shown.*

With the displayed winding-current directions, phase $a$ connects from terminal $u$ to $v$, phase $b$ from $v$ to $w$, and phase $c$ from $w$ to $u$. Their winding voltages are therefore

$$
v_{uv}=v_u-v_v,
\qquad
v_{vw}=v_v-v_w,
\qquad
v_{wu}=v_w-v_u.
$$

Applying Kirchhoff's current law at the three terminals gives

$$
\begin{aligned}
i_u &= i_a-i_c,\\
i_v &= i_b-i_a,\\
i_w &= i_c-i_b.
\end{aligned}
$$

These relationships also give $i_u+i_v+i_w=0$ for the three-wire connection.

Thus each delta winding is driven by a line-to-line voltage, and line current is not the same as winding current. By contrast, line current equals winding current in a wye connection, while phase-to-neutral voltage is not generally the same as line-to-line terminal voltage.

This distinction affects the interpretation of resistance, inductance, back-EMF constant, torque constant, and current rating. Use the connection and measurement convention stated by the motor manufacturer.

## Extending Beyond One Pole Pair

For $p$ pole pairs,

$$
\theta_e=p\theta_m,
\qquad
\omega_e=p\omega_m.
$$

The waveform equations retain their form when expressed in electrical angle, but sensor transitions and commutation cycles occur $p$ times per mechanical revolution.

## Limits of This Model

The model is useful for choosing and reasoning about a small-motor driver, but it omits effects that matter in higher-performance design:

- mutual inductance and the full inductance matrix,
- position-dependent inductance and reluctance torque,
- magnetic saturation and cross-coupling,
- nonsinusoidal back-EMF and cogging torque,
- inverter dead time and semiconductor voltage drops,
- winding and semiconductor temperature dependence, and
- mechanical compliance, nonlinear friction, and detailed losses.

## Related Notes

- [[Motor Theory Fundamentals]]
- [[Three-Phase Inverters]]
- [[Hall-Effect Sensors Encoders and Commutation]]
