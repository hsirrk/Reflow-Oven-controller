$NOLIST
$MODN76E003
$LIST

;  N76E003 pinout:
;                               -------
;       PWM2/IC6/T0/AIN4/P0.5 -|1    20|- P0.4/AIN5/STADC/PWM3/IC3
;               TXD/AIN3/P0.6 -|2    19|- P0.3/PWM5/IC5/AIN6
;               RXD/AIN2/P0.7 -|3    18|- P0.2/ICPCK/OCDCK/RXD_1/[SCL]
;                    RST/P2.0 -|4    17|- P0.1/PWM4/IC4/MISO
;        INT0/OSCIN/AIN1/P3.0 -|5    16|- P0.0/PWM3/IC3/MOSI/T1
;              INT1/AIN0/P1.7 -|6    15|- P1.0/PWM2/IC2/SPCLK
;                         GND -|7    14|- P1.1/PWM1/IC1/AIN7/CLO
;[SDA]/TXD_1/ICPDA/OCDDA/P1.6 -|8    13|- P1.2/PWM0/IC0
;                         VDD -|9    12|- P1.3/SCL/[STADC]
;            PWM5/IC7/SS/P1.5 -|10   11|- P1.4/SDA/FB/PWM1
;                               -------
;

DSEG ; Before the state machine!
FSM1_state: ds 1
temp_soak: ds 1
time_soak: ds 1
temp_3: ds 1
temp_refl: ds 1
time_refl: ds 1

FSM1:
	mov a, FSM1_state
	
FSM1_state0:
	cjne a, #0, FSM1_state1
	mov pwm, #0
	jb PB6, FSM1_state0_done
	jnb PB6, $ ; Wait for key release
	mov FSM1_state, #1
FSM1_state0_done:
	ljmp FSM1
	
FSM1_state1:
	cjne a, #1, FSM1_state2
	mov pwm, #100
	mov sec, #0
	mov a, temp_soak
	clr c
	subb a, temp
	jnc FSM1_state1_done
	mov FSM1_state, #2
FSM1_state1_done:
	ljmp FSM1
	
FSM1_state2:
	cjne a, #2, FSM1_state3
	mov pwm, #20
	mov a, #time_soak
	clr c
	subb a, sec
	jnc FSM1_state2_done
	mov FSM1_state, #3
FSM1_state2_done:
	ljmp FSM1
	
FSM1_state3:
	cjne a, #3, FSM1_state4
	mov pwm, #100
	mov sec, #0
	mov a, #temp_3
	clr c
	subb a, 
	