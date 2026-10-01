---
title: BLDC Notation and Signal Glossary
type: reference
tags:
  - ME5305
  - BLDC
  - notation
  - motor-drivers
source:
  course: ME5305
status: publication-ready
---

This glossary collects the mathematical notation, signal names, and register terminology used in the ME5305 BLDC notes. Device data sheets may use different pin and register names; translate those names at the hardware boundary rather than changing the physical meaning of the quantities below.

## Naming and Notation Conventions

> [!table]
> | Entity Type                                   | Visual Style                                            | Example                                                                                         | Usage Context                                                                                                                                                           |
> | :-------------------------------------------- | :------------------------------------------------------ | :---------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
> | Coordinate- or Phase-Axis Labels              | Upright lowercase font with no accent                   | $\mathrm{a}$, $\mathrm{b}$, $\mathrm{c}$                                                        | Labels for coordinate or phase axes in figures                                                                                                                          |
> | Time-Varying Scalar Quantities and Components | Italic font with conventional letter case and no accent | $i_a$, $e_a$, $T_{e,a}$                                                                         | Instantaneous scalar variables and scalar components                                                                                                                    |
> | Constant Parameters or Coefficients           | Italic font with conventional letter case and no accent | $R_s$, $L_s$, $\psi_m$, $p$                                                                     | Scalar parameters and constants                                                                                                                                         |
> | Unit-Direction Vectors                        | Bold upright font with a hat accent                     | $\hat{\mathbf{a}}$, $\hat{\mathbf{b}}$, $\hat{\mathbf{c}}$                                      | Unit vectors represented as geometric objects; an independent set may form a basis                                                                                      |
> | Geometric Vectors                             | Italic font with an arrow accent                        | $\vec{i}_s=\frac{2}{3}\left(i_a\hat{\mathbf{a}}+i_b\hat{\mathbf{b}}+i_c\hat{\mathbf{c}}\right)$ | Geometric vectors; vector arrows are drawn with a heavier stroke in figures                                                                                             |
> | Linear-Algebra Vectors                        | Bold upright lowercase font with no accent              | $\mathbf{i}_{abc}=\begin{bmatrix}i_a&i_b&i_c\end{bmatrix}^{\mathsf T}$                          | Multicomponent column arrays                                                                                                                                            |
> | Matrices                                      | Bold upright uppercase font with no accent              | $\mathbf{M}=\begin{bmatrix}M_{11}&M_{12}\\M_{21}&M_{22}\end{bmatrix}$                           | Linear transformations and other matrices                                                                                                                               |
> | Peak or Amplitude Scalars                     | Italic uppercase font with a hat accent                 | $v_a(t)=\hat V_a\sin(\omega_e t)$                                                               | Peak values that must be distinguished from corresponding instantaneous variables; established magnitude parameters such as $\psi_m$ retain their conventional notation |
>
> Standard naming and notation conventions used in the collection of notes regarding BLDC and PMSMS motors.

## Signal and Register Names

For phase index $x\in\{a,b,c\}$:

> [!table]
> | Symbol | Meaning |
> | --- | --- |
> | $H_x(t)$ | Binary Hall-sensor signal for phase channel $x$ |
> | $\mathrm{DIR}$ | Requested commutation direction |
> | $S_x\in\{1,0,Z\}$ | Abstract leg-state request: high-side, low-side, or high impedance |
> | $d$ | Block-commutation duty request, with $0\le d\le1$ |
> | $d_x$ | High-side PWM duty ratio for phase $x$, with $0\le d_x\le1$ |
> | $m$ | Normalized sinusoidal modulation depth, with $0\le m\le1$ for the waveform convention used here |
> | $\mathrm{PSC}$ | STM32 timer prescaler value |
> | $\mathrm{ARR}$ | STM32 timer auto-reload value that sets the counter limit |
> | $\mathrm{CNT}(t)$ | Instantaneous timer counter value |
> | $\mathrm{CCR}_x$ | Compare-register value assigned to phase $x$ |
> | $\mathrm{EN}_x(t)$ | Per-leg gate-driver enable; low requests both switches off |
> | $\mathrm{IN}_x(t)$ | Binary PWM input to the complementary gate-driver logic |
> | $\mathrm{G}_{\mathrm H,x}$, $\mathrm{G}_{\mathrm L,x}$ | High-side and low-side MOSFET gate nodes for phase $x$ |
> | $v_{\mathrm{GS,H},x}(t)$ | High-side MOSFET gate-source voltage |
> | $v_{\mathrm{GS,L},x}(t)$ | Low-side MOSFET gate-source voltage |
> | $R_{\mathrm{sh},x}$ | Current-shunt resistor associated with phase leg or motor lead $x$ |
> | $R_\mathrm{sh}$ | Single current-shunt resistor in the common DC-link return |
> | $\mathrm{S}_{\mathrm L,x}$ | Low-side current-sense node connected to the driver amplifier input |
> | $\mathrm{CS}_x$ | Conditioned current-sense output from the driver to the controller |
> | $v_x(t)$ | Inverter pole potential for phase $x$, measured relative to GND |
> | $V_\mathrm{DC}$ | DC-bus voltage |
>
> A glossary of symbols used in the collection of notes regarding BLDC and PMSMS motors.

## Usage Rules

- $S_x$ is an abstract three-state command, not a physical MCU pin voltage.
- $\mathrm{EN}_x$ and $\mathrm{IN}_x$ are the assumed physical driver-interface signals; a specific driver may encode the same requests differently.
- Upright multi-letter labels identify pins, logic signals, or register names. Italic symbols identify mathematical quantities.
- Time arguments may be omitted in block diagrams when the signal character is clear, but are retained in waveform plots and equations when needed.
- $Z$ means that neither switch is intentionally commanded on; current may still flow through MOSFET channels or body diodes.
