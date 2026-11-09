# Preguntas para la defensa oral

**¿Un ataque del 51 % permite robar monedas de cualquier usuario?**  
En PoW, la mayoría del poder de minería da ventaja estadística para acumular trabajo. El atacante puede intentar reorganizar bloques, revertir un pago propio o censurar transacciones. Los nodos todavía verifican la autorización de cada gasto y las reglas de emisión.

**¿En qué se diferencian Sybil y Eclipse?**  
Sybil multiplica las identidades de un actor. Eclipse monopoliza las conexiones de un nodo y controla qué información le llega. Las identidades Sybil pueden facilitar el aislamiento. Su peso en consenso depende del protocolo.

**¿Eclipse altera el consenso de todos los nodos?**  
El alcance directo es la visión de la víctima. El atacante puede ocultarle bloques o retrasar la información que recibe mientras el resto de la red opera con normalidad.

**¿Una firma válida garantiza que la operación era legítima?**  
Una firma válida demuestra autorización criptográfica con la clave correspondiente. Quien roba esa clave puede firmar una operación que el titular jamás aprobó.

**¿Por qué se ejecuta un contrato vulnerable si los nodos son honestos?**  
Los nodos aplican las reglas del protocolo y ejecutan el código publicado. La intención del desarrollador solo influye en el resultado si quedó expresada correctamente en ese código.

**¿Qué es la reentrada (reentrancy)?**  
Durante una llamada externa, el receptor puede devolver el control al contrato original invocando otra operación antes de que termine la anterior. Si hay una ruta de retorno, el estado relevante sigue pendiente y las comprobaciones permiten la operación, el contrato puede procesar un segundo retiro sobre un saldo desactualizado.

**¿Qué ocurrió con The DAO?**  
En 2016, la reentrada en un contrato de The DAO permitió desviar ether. Parte de la comunidad adoptó después una bifurcación que habilitó la recuperación de fondos. La otra rama continuó como Ethereum Classic. El incidente inicial afectó la lógica de un contrato.

**¿Todas las blockchains sufren un ataque del 51 % de igual manera?**  
El ejemplo del 51 % corresponde al poder de minería en PoW. En prueba de participación (PoS) y en protocolos tolerantes a fallos bizantinos (BFT), cambian el recurso o los votos relevantes, los umbrales y las reglas de finalidad.

**¿Los hashes garantizan inmutabilidad absoluta?**  
Los hashes permiten detectar cambios en los datos comprometidos. La resistencia a reemplazar un historial depende también de las reglas de consenso, de la distribución de recursos y de sus supuestos de seguridad.

**¿Qué controles reducen el riesgo en los contratos?**  
Aplicar autorización explícita y privilegios mínimos. Revisar y probar operaciones adversas. Actualizar el estado antes de llamadas externas mediante el patrón de verificaciones, efectos e interacciones (checks-effects-interactions) y complementar con guardas de reentrada cuando proceda. Las auditorías ayudan a detectar fallos residuales.

**¿Cuántas confirmaciones hacen seguro un pago PoW?**  
El riesgo depende de los recursos del adversario, las condiciones de la red y el valor del pago. Más confirmaciones suelen reducir la probabilidad de reversión cuando la potencia honesta domina. Un doble gasto puede ocurrir sin mayoría y disponer de una mayoría tampoco vuelve instantánea una reorganización.

Las fuentes primarias están en el [guion de exposición](guion_integrante7.md#fuentes).
