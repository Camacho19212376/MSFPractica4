"""
Práctica: Sistema endocrino
Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

Nombre del alumno: Tchandra Yahoel Camacho Llanes
Número de control: 19212376
Correo institucional: l19212376@tijuana.tecnm.mx

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""

import control as ctrl
import numpy as np
import matplotlib.pyplot as plt

# TIEMPO
x0, t0, tend, dt = 0, 0, 10, 1e-3
N = round((tend - t0) / dt) + 1
t = np.linspace(t0, tend, N)

# SEÑAL DE ENTRADA (ESCALÓN UNITARIO)
u = np.ones_like(t)

# FUNCIÓN DEL SISTEMA
def endocrino(R1, L, R2, C):
    num = [R2]
    den = [C*L*R1, C*R1*R2 + L, R1 + R2]
    return ctrl.tf(num, den)

# COMPONENTES
R1, L = 1e3, 10e-3

# --- CONTROL ---
R2_control = 100e3
C_control = 1e-6
sys_control = endocrino(R1, L, R2_control, C_control)
print(f"Funcion de transferencia (Control):\n{sys_control}\n")

# --- CASO ---
R2_caso = 1e3
C_caso = 1000e-6
sys_caso = endocrino(R1, L, R2_caso, C_caso)
print(f"Funcion de transferencia (Caso):\n{sys_caso}\n")

# RESPUESTAS A ESCALÓN
_, Ve = ctrl.forced_response(sys_control, t, u, x0)
_, Vs = ctrl.forced_response(sys_caso, t, u, x0)

# CONTROLADOR PI
def controlador(kP, kI, sys):
    Cr = 1e-6
    Re = 1 / (kI * Cr)
    Rr = kP * Re

    numPI = [Rr*Cr, 1]
    denPI = [Re*Cr, 0]

    print(f"Cr = {Cr} F")
    print(f"Re = {Re} Ohms")
    print(f"Rr = {Rr} Ohms\n")

    PI = ctrl.tf(numPI, denPI)
    sistema_total = ctrl.series(PI, sys)
    sistema_cerrado = ctrl.feedback(sistema_total, 1, sign=-1)

    return sistema_cerrado

# PARÁMETROS PI
kP, kI, kD = 132.813, 3266.138, 0.181

PI_sys = controlador(kP, kI, sys_caso)

# RESPUESTA CON CONTROLADOR (CORREGIDO: usa u, no Ve)
_, PI = ctrl.forced_response(PI_sys, t, u, x0)

# GRÁFICA
fig1 = plt.figure(figsize=(6,4))

colors = np.array([
    [10,196,224],
    [133,64,157],
    [238,167,39]
]) / 255

plt.plot(t, Ve, '-', linewidth=1, color=colors[0], label='Vs(t): Control')
plt.plot(t, Vs, '-', linewidth=1, color=colors[1], label='Vs(t): Caso')
plt.plot(t, PI, ':', linewidth=2, color=colors[2], label='PID(t): Caso')

plt.title('Control vs Caso')
plt.xlim(0,10); plt.xticks(np.arange(0,11,1))
plt.ylim(0,1.1); plt.yticks(np.arange(0,1.2,0.1))

plt.xlabel('t [s]', fontsize=11)
plt.ylabel('V(t) [V]', fontsize=11)

plt.legend(bbox_to_anchor=(0.5,-0.2), loc='center', ncol=3, fontsize=9, frameon=True)

plt.tight_layout()
plt.savefig('s_endocrino_python.pdf', bbox_inches='tight')
plt.show()