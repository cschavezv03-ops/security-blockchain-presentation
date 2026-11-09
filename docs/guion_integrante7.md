# Integrante 7 · Ataques y vulnerabilidades en blockchain

Tecnologías de Seguridad · EPN

El recorrido dura **6:20**. Quedan **40 s** para pausas y cambios de diapositiva dentro del límite de 7:00. Los tiempos de la izquierda son acumulados y los de la derecha se cuentan desde el inicio de cada clip.

## 01 · ¿Blockchain es invulnerable? (00:00–00:40)

Clip `01_amenazas.mp4` · 40 s

**00:00 · +00:00**  
*Cadena de tres bloques con enlaces verdes.*

> Ya vimos cómo una blockchain mantiene la integridad de un registro compartido.

**00:08 · +00:08**  
*Escudo sobre la cadena y tres capas debajo.*

> La criptografía ayuda a proteger ese registro. Sin embargo, el sistema también depende de la red entre pares, del consenso y de los contratos que ejecuta.

**00:20 · +00:20**  
*Alertas sucesivas en red, consenso y contratos.*

> En cada capa hay una pregunta distinta. ¿Quién le informa al nodo? ¿Qué historial se selecciona? ¿Qué operaciones permite el código de la aplicación?

**00:32 · +00:32**  
*Tesis fija y énfasis en la red P2P.*

> La integridad del registro es solo una parte de la seguridad. Empecemos por la red.


## 02 · La red P2P: Sybil → Eclipse (00:40–01:40)

Clip `02_sybil_eclipse.mp4` · 60 s

**00:40 · +00:00**  
*Un actor crea ocho identidades numeradas.*

> En un ataque Sybil, un actor se presenta con muchas identidades para ganar influencia. El poder de consenso depende de las reglas de cada red.

**00:52 · +00:12**  
*Ocho conexiones honestas se sustituyen por enlaces controlados.*

> Ahora enfoquémonos en un nodo. Si sus ocho conexiones terminan en pares controlados por el mismo atacante, este puede decidir qué información le llega.

**01:04 · +00:24**  
*Red honesta en bloque 520 y nodo aislado en bloque 500.*

> Ese aislamiento es un ataque Eclipse. En este ejemplo, la red honesta ya conoce el bloque quinientos veinte. El nodo aislado se quedó en el quinientos. Desde su perspectiva, todavía está viendo una cadena con bloques válidos.

**01:22 · +00:42**  
*Firma válida ≠ información completa.*

> Puede verificar hashes y firmas con normalidad. Una firma válida autentica lo que recibió. La información que sus pares le ocultaron queda fuera de esa verificación.

**01:34 · +00:54**  
*Enlaces heterogéneos reconectan al nodo.*

> Diversificar y aleatorizar la selección de pares dificulta que alguien monopolice todas sus conexiones.


## 03 · Consenso: reorganizaciones y doble gasto (01:40–03:00)

Clip `03_consenso.mp4` · 80 s

**01:40 · +00:00**  
*Ejemplo PoW con 49 % de recursos honestos y 51 % del atacante.*

> En prueba de trabajo, o Proof of Work, quien controla más de la mitad del poder de minería tiene ventaja estadística para acumular trabajo más rápido.

**01:52 · +00:12**  
*Bloque 101-B incluye el pago y Bob entrega el producto.*

> Supongamos que Alice paga cinco monedas a Bob. El pago aparece en el bloque ciento uno B. Bob ve una confirmación y entrega un producto. El bloque cien es el punto común del ejemplo.

**02:08 · +00:28**  
*Desde el bloque 100 surge una rama con un gasto conflictivo.*

> Alice, que aquí controla la mayoría de recursos, construye otra rama desde el bloque cien. En ella gasta los mismos fondos hacia otro destino. Cada rama se valida por separado y solo admite uno de esos pagos.

**02:24 · +00:44**  
*La rama alternativa supera el trabajo acumulado y se selecciona.*

> Cuando la rama alternativa válida supera en trabajo acumulado a la rama visible, los nodos reorganizan la cadena. El pago a Bob pierde sus confirmaciones. Bob ya entregó el producto, pero el historial seleccionado contiene el gasto conflictivo.

**02:40 · +01:00**  
*El escudo conserva las verificaciones de firmas y reglas.*

> Los nodos siguen exigiendo firmas autorizadas y respetando las reglas de emisión. La ventaja del atacante afecta la selección entre ramas válidas.

**02:51 · +01:11**  
*Esperar confirmaciones y valorar el riesgo de la red.*

> Más confirmaciones reducen el riesgo en condiciones normales. En prueba de participación, o Proof of Stake, cambian las condiciones del ataque.


## 04 · El consenso funciona… pero el contrato falla (03:00–04:20)

Clip `04_contratos.mp4` · 80 s

**03:00 · +00:00**  
*Usuario, contrato y nodos. Se destaca la lógica de negocio.*

> Pasemos a los contratos inteligentes, o smart contracts. El usuario solicita una operación y los nodos ejecutan el código publicado. La lógica del contrato decide quién puede hacerla y en qué condiciones.

**03:15 · +00:15**  
*Comparación entre comprobar el saldo y autorizar primero al solicitante.*

> Imaginemos una función de retiro que comprueba que hay saldo suficiente. Si omite verificar quién solicita el retiro, cualquier usuario podría activarlo. La corrección empieza por comprobar que el solicitante tiene permiso sobre esos fondos.

**03:31 · +00:31**  
*A llama a B, B vuelve a A y el saldo de ejemplo sigue en 10.*

> El segundo fallo es la reentrada, o reentrancy. A llama al contrato B para enviarle fondos y deja para después el cambio de saldo. La llamada entrega temporalmente el control a B. B vuelve a invocar el retiro antes de que la primera ejecución termine. Si la nueva llamada pasa las comprobaciones, encuentra el mismo saldo y puede provocar otro envío.

**03:57 · +00:57**  
*Verificar, actualizar el estado e interactuar, con una guarda adicional.*

> La defensa ordena las operaciones. Primero se comprueban permisos y saldo, luego se actualiza el estado y por último se llama afuera. También pueden usarse guardas.

**04:08 · +01:08**  
*Transacción válida ≠ operación legítima. Puente a The DAO.*

> Los nodos pueden coincidir en el resultado aunque la aplicación permita operaciones que el desarrollador jamás quiso autorizar. Veamos qué ocurrió en The DAO.


## 05 · The DAO — Ethereum, 2016 (04:20–05:20)

Clip `05_the_dao.mp4` · 60 s

**04:20 · +00:00**  
*Línea de tiempo de 2016 y glifo genérico de contrato.*

> The DAO fue un proyecto construido sobre Ethereum en dos mil dieciséis. Su contrato permitía retirar fondos y contenía una vulnerabilidad de reentrada.

**04:32 · +00:12**  
*Retiro, llamada externa y reentrada con el estado pendiente.*

> El mecanismo se parece al que acabamos de ver. Durante un retiro, el código cedía el control a una llamada externa antes de completar una actualización. Una nueva llamada podía entrar mientras el contrato todavía tenía el registro anterior.

**04:49 · +00:29**  
*Las llamadas repetidas desvían fondos del contrato.*

> Las llamadas repetidas permitieron desviar una cantidad importante de ether. Las transacciones se ejecutaron según el código del contrato y las reglas del protocolo. El error estaba en la lógica de retiro de la aplicación.

**05:05 · +00:45**  
*Respuesta comunitaria y bifurcación Ethereum / Ethereum Classic.*

> Después, parte de la comunidad adoptó una bifurcación que habilitó la recuperación de fondos. Quienes siguieron la otra rama continuaron en Ethereum Classic.

**05:15 · +00:55**  
*Consenso correcto ≠ código seguro.*

> La ejecución descentralizada reproduce el resultado del código, incluidos sus errores.


## 06 · Seguridad por capas (05:20–06:20)

Clip `06_prevencion.mp4` · 60 s

**05:20 · +00:00**  
*Red y diversidad de pares.*

> ¿Cómo reducimos estos riesgos? En la red entre pares conviene diversificar las conexiones y aleatorizar su selección. Así es más difícil que un solo actor aísle un nodo y controle lo que ve.

**05:34 · +00:14**  
*Consenso, recursos distribuidos, validación y finalidad.*

> En consenso importan la distribución de recursos y la validación independiente. El nivel de confirmación o finalidad que necesitamos depende del protocolo y del riesgo de aceptar la operación.

**05:47 · +00:27**  
*Claves, almacenamiento seguro y autorización.*

> Las claves requieren almacenamiento seguro y controles de autorización. Si alguien obtiene una clave privada, puede producir firmas válidas por acciones que el titular jamás aprobó.

**05:59 · +00:39**  
*Contratos, auditoría, pruebas y orden de interacción.*

> En contratos hay que revisar permisos, probar casos adversos, auditar la lógica y aplicar patrones seguros. Actualizar el estado antes de interactuar reduce ciertos riesgos de reentrada.

**06:10 · +00:50**  
*Se reúnen las cuatro capas y queda la conclusión.*

> Una blockchain puede preservar la integridad del registro y seguir expuesta. La seguridad del sistema exige proteger red, consenso, claves y aplicaciones.

## Fuentes

- [NISTIR 8202 — Blockchain Technology Overview](https://csrc.nist.gov/pubs/ir/8202/final) · integridad y supuestos del consenso.
- [Heilman et al. — Eclipse Attacks on Bitcoin’s Peer-to-Peer Network](https://www.usenix.org/sites/default/files/sec15_full_proceedings.pdf) · aislamiento del nodo y contramedidas, p. 129 del volumen.
- [Satoshi Nakamoto — Bitcoin: A Peer-to-Peer Electronic Cash System](https://bitcoin.org/bitcoin.pdf) · PoW y confirmaciones probabilísticas, §§4–5, 11.
- [Ethereum.org — Smart contract security](https://ethereum.org/developers/docs/smart-contracts/security/) · controles y pruebas.
- [OWASP — Smart Contract Top 10](https://scs.owasp.org/sctop10/) · riesgos de autorización y reentrada.
- [Solidity — Security Considerations](https://docs.soliditylang.org/en/latest/security-considerations.html) · llamadas externas y checks-effects-interactions.
- [Ethereum Foundation — Critical Update Re: DAO Vulnerability](https://blog.ethereum.org/en/2016/06/17/critical-update-re-dao-vulnerability) · descripción contemporánea del incidente.
- [Ethereum Foundation — Hard Fork Completed](https://blog.ethereum.org/en/2016/07/20/hard-fork-completed) · implementación de la respuesta al incidente.
- [Ethereum.org — Ethereum forks](https://ethereum.org/ethereum-forks/) · DAO fork y continuidad de Ethereum Classic.
