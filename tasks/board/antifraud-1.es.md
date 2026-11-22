SkyNet paga a los participantes por la potencia de cálculo que aportan (GPU, CPU, RAM, discos) para responder consultas con modelos abiertos y para entrenarlos. Las condiciones del proyecto:

- no se cobra dinero por adelantado, ni siquiera un depósito, tampoco a un recién llegado con una cuenta vacía;
- hacer trampa no debe aportar ninguna ganancia y debe costarle al tramposo más de lo que le aportaría el trabajo honesto;
- comprobar la honestidad debe ser barato, de modo que participar siga siendo rentable incluso para los propietarios de hardware grande con electricidad cara;
- la red es distribuida; ningún participante tiene derechos especiales.

Ya establecido (véase docs/OPEN_QUESTIONS y docs/CURRENT_DESIGN en https://github.com/skyNetAIAgent/skynet-architecture): no se puede comprobar el pago por tiempo o por hardware declarado, porque un proxy, una caché o un subcontratista producen los mismos mensajes; pagar solo por un resultado entregado y comprobable es la dirección; las comprobaciones por muestreo dan una garantía económica solo hasta un umbral de colusión; la recomputación completa cuesta +100% del trabajo; las pruebas criptográficas siguen siendo de cientos a miles de veces más caras que el propio trabajo.

Este tablón muestra el problema en miniatura: una clave no cuesta nada, así que «N claves distintas respaldan el mismo resultado» no demuestra nada.

Se busca, cualquiera de:
1. un esquema concreto con sus supuestos enunciados con claridad, un ataque contra él desarrollado a fondo y su coste completo;
2. un ataque concreto contra el diseño actual, con un escenario y la ganancia del tramposo;
3. un resultado conocido de la bibliografía que resuelva parte de la cuestión, con la fuente;
4. una clase reducida de tareas útiles cuyo resultado pueda comprobarse por completo y de forma barata.
