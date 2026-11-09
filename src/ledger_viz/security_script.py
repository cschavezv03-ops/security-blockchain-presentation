"""Fuente única para los tiempos, los visuales y el texto oral del integrante 7."""

from dataclasses import dataclass
from itertools import accumulate
from typing import Final


@dataclass(frozen=True)
class Beat:
    seconds: int
    visual: str
    speech: str


@dataclass(frozen=True)
class Clip:
    id: str
    topic: str
    title: str
    beats: tuple[Beat, ...]

    @property
    def seconds(self) -> int:
        return sum(beat.seconds for beat in self.beats)


CLIPS: Final = (
    Clip(
        "amenazas",
        "PANORAMA",
        "¿Blockchain es invulnerable?",
        (
            Beat(
                8,
                "Cadena de tres bloques con enlaces verdes.",
                "Ya vimos cómo una blockchain mantiene la integridad de un registro compartido.",
            ),
            Beat(
                12,
                "Escudo sobre la cadena y tres capas debajo.",
                "La criptografía ayuda a proteger ese registro. Sin embargo, el sistema también "
                "depende de la red entre pares, del consenso y de los contratos que ejecuta.",
            ),
            Beat(
                12,
                "Alertas sucesivas en red, consenso y contratos.",
                "En cada capa hay una pregunta distinta. ¿Quién le informa al nodo? ¿Qué historial "
                "se selecciona? ¿Qué operaciones permite el código de la aplicación?",
            ),
            Beat(
                8,
                "Tesis fija y énfasis en la red P2P.",
                "La integridad del registro es solo una parte de la seguridad. Empecemos por "
                "la red.",
            ),
        ),
    ),
    Clip(
        "sybil_eclipse",
        "RED ENTRE PARES",
        "La red P2P: Sybil → Eclipse",
        (
            Beat(
                12,
                "Un actor crea ocho identidades numeradas.",
                "En un ataque Sybil, un actor se presenta con muchas identidades para ganar "
                "influencia. El poder de consenso depende de las reglas de cada red.",
            ),
            Beat(
                12,
                "Ocho conexiones honestas se sustituyen por enlaces controlados.",
                "Ahora enfoquémonos en un nodo. Si sus ocho conexiones terminan en pares "
                "controlados "
                "por el mismo atacante, este puede decidir qué información le llega.",
            ),
            Beat(
                18,
                "Red honesta en bloque 520 y nodo aislado en bloque 500.",
                "Ese aislamiento es un ataque Eclipse. En este ejemplo, la red honesta ya conoce "
                "el bloque quinientos veinte. El nodo aislado se quedó en el quinientos. Desde su "
                "perspectiva, todavía está viendo una cadena con bloques válidos.",
            ),
            Beat(
                12,
                "Firma válida ≠ información completa.",
                "Puede verificar hashes y firmas con normalidad. Una firma válida autentica lo "
                "que recibió. La información que sus pares le ocultaron queda fuera de esa "
                "verificación.",
            ),
            Beat(
                6,
                "Enlaces heterogéneos reconectan al nodo.",
                "Diversificar y aleatorizar la selección de pares dificulta que alguien "
                "monopolice todas sus conexiones.",
            ),
        ),
    ),
    Clip(
        "consenso",
        "PRUEBA DE TRABAJO",
        "Consenso: reorganizaciones y doble gasto",
        (
            Beat(
                12,
                "Ejemplo PoW con 49 % de recursos honestos y 51 % del atacante.",
                "En prueba de trabajo, o Proof of Work, quien controla más de la mitad del poder "
                "de minería tiene ventaja estadística para acumular trabajo más rápido.",
            ),
            Beat(
                16,
                "Bloque 101-B incluye el pago y Bob entrega el producto.",
                "Supongamos que Alice paga cinco monedas a Bob. El pago aparece en el bloque "
                "ciento uno B. Bob ve una confirmación y entrega un producto. El bloque cien es "
                "el punto común del ejemplo.",
            ),
            Beat(
                16,
                "Desde el bloque 100 surge una rama con un gasto conflictivo.",
                "Alice, que aquí controla la mayoría de recursos, construye otra rama desde el "
                "bloque cien. En ella gasta los mismos fondos hacia otro destino. Cada rama se "
                "valida por separado y solo admite uno de esos pagos.",
            ),
            Beat(
                16,
                "La rama alternativa supera el trabajo acumulado y se selecciona.",
                "Cuando la rama alternativa válida supera en trabajo acumulado a la rama visible, "
                "los nodos reorganizan la cadena. El pago a Bob pierde sus confirmaciones. Bob "
                "ya entregó el producto, pero el historial seleccionado contiene el gasto "
                "conflictivo.",
            ),
            Beat(
                11,
                "El escudo conserva las verificaciones de firmas y reglas.",
                "Los nodos siguen exigiendo firmas autorizadas y respetando las reglas de emisión. "
                "La ventaja del atacante afecta la selección entre ramas válidas.",
            ),
            Beat(
                9,
                "Esperar confirmaciones y valorar el riesgo de la red.",
                "Más confirmaciones reducen el riesgo en condiciones normales. En prueba de "
                "participación, o Proof of Stake, cambian las condiciones del ataque.",
            ),
        ),
    ),
    Clip(
        "contratos",
        "APLICACIONES",
        "El consenso funciona… pero el contrato falla",
        (
            Beat(
                15,
                "Usuario, contrato y nodos. Se destaca la lógica de negocio.",
                "Pasemos a los contratos inteligentes, o smart contracts. El usuario solicita una "
                "operación y los nodos ejecutan el código publicado. La lógica del contrato decide "
                "quién puede hacerla y en qué condiciones.",
            ),
            Beat(
                16,
                "Comparación entre comprobar el saldo y autorizar primero al solicitante.",
                "Imaginemos una función de retiro que comprueba que hay saldo suficiente. Si omite "
                "verificar quién solicita el retiro, cualquier usuario podría activarlo. La "
                "corrección empieza por comprobar que el solicitante tiene permiso sobre esos "
                "fondos.",
            ),
            Beat(
                26,
                "A llama a B, B vuelve a A y el saldo de ejemplo sigue en 10.",
                "El segundo fallo es la reentrada, o reentrancy. A llama al contrato B para "
                "enviarle "
                "fondos y deja para después el cambio de saldo. La llamada entrega "
                "temporalmente el "
                "control a B. B vuelve a invocar el retiro antes de que la primera ejecución "
                "termine. "
                "Si la nueva llamada pasa las comprobaciones, encuentra el mismo saldo y puede "
                "provocar otro envío.",
            ),
            Beat(
                11,
                "Verificar, actualizar el estado e interactuar, con una guarda adicional.",
                "La defensa ordena las operaciones. Primero se comprueban permisos y saldo, luego "
                "se actualiza el estado y por último se llama afuera. También pueden usarse "
                "guardas.",
            ),
            Beat(
                12,
                "Transacción válida ≠ operación legítima. Puente a The DAO.",
                "Los nodos pueden coincidir en el resultado aunque la aplicación permita "
                "operaciones que el desarrollador jamás quiso autorizar. Veamos qué ocurrió "
                "en The DAO.",
            ),
        ),
    ),
    Clip(
        "the_dao",
        "CASO HISTÓRICO",
        "The DAO — Ethereum, 2016",
        (
            Beat(
                12,
                "Línea de tiempo de 2016 y glifo genérico de contrato.",
                "The DAO fue un proyecto construido sobre Ethereum en dos mil dieciséis. Su "
                "contrato permitía retirar fondos y contenía una vulnerabilidad de reentrada.",
            ),
            Beat(
                17,
                "Retiro, llamada externa y reentrada con el estado pendiente.",
                "El mecanismo se parece al que acabamos de ver. Durante un retiro, el código "
                "cedía el control a una llamada externa antes de completar una actualización. "
                "Una nueva llamada podía entrar mientras el contrato todavía tenía el registro "
                "anterior.",
            ),
            Beat(
                16,
                "Las llamadas repetidas desvían fondos del contrato.",
                "Las llamadas repetidas permitieron desviar una cantidad importante de ether. "
                "Las transacciones se ejecutaron según el código del contrato y las reglas del "
                "protocolo. El error estaba en la lógica de retiro de la aplicación.",
            ),
            Beat(
                10,
                "Respuesta comunitaria y bifurcación Ethereum / Ethereum Classic.",
                "Después, parte de la comunidad adoptó una bifurcación que habilitó la "
                "recuperación "
                "de fondos. Quienes siguieron la otra rama continuaron en Ethereum Classic.",
            ),
            Beat(
                5,
                "Consenso correcto ≠ código seguro.",
                "La ejecución descentralizada reproduce el resultado del código, incluidos "
                "sus errores.",
            ),
        ),
    ),
    Clip(
        "prevencion",
        "DEFENSAS",
        "Seguridad por capas",
        (
            Beat(
                14,
                "Red y diversidad de pares.",
                "¿Cómo reducimos estos riesgos? En la red entre pares conviene diversificar las "
                "conexiones y aleatorizar su selección. Así es más difícil que un solo actor aísle "
                "un nodo y controle lo que ve.",
            ),
            Beat(
                13,
                "Consenso, recursos distribuidos, validación y finalidad.",
                "En consenso importan la distribución de recursos y la validación independiente. "
                "El nivel de confirmación o finalidad que necesitamos depende del protocolo y del "
                "riesgo de aceptar la operación.",
            ),
            Beat(
                12,
                "Claves, almacenamiento seguro y autorización.",
                "Las claves requieren almacenamiento seguro y controles de autorización. Si "
                "alguien "
                "obtiene una clave privada, puede producir firmas válidas por acciones que el "
                "titular jamás aprobó.",
            ),
            Beat(
                11,
                "Contratos, auditoría, pruebas y orden de interacción.",
                "En contratos hay que revisar permisos, probar casos adversos, auditar la lógica "
                "y aplicar patrones seguros. Actualizar el estado antes de interactuar reduce "
                "ciertos riesgos de reentrada.",
            ),
            Beat(
                10,
                "Se reúnen las cuatro capas y queda la conclusión.",
                "Una blockchain puede preservar la integridad del registro y seguir expuesta. "
                "La seguridad del sistema exige proteger red, consenso, claves y aplicaciones.",
            ),
        ),
    ),
)

SOURCES: Final = (
    (
        "NISTIR 8202 — Blockchain Technology Overview",
        "https://csrc.nist.gov/pubs/ir/8202/final",
        "integridad y supuestos del consenso",
    ),
    (
        "Heilman et al. — Eclipse Attacks on Bitcoin’s Peer-to-Peer Network",
        "https://www.usenix.org/sites/default/files/sec15_full_proceedings.pdf",
        "aislamiento del nodo y contramedidas, p. 129 del volumen",
    ),
    (
        "Satoshi Nakamoto — Bitcoin: A Peer-to-Peer Electronic Cash System",
        "https://bitcoin.org/bitcoin.pdf",
        "PoW y confirmaciones probabilísticas, §§4–5, 11",
    ),
    (
        "Ethereum.org — Smart contract security",
        "https://ethereum.org/developers/docs/smart-contracts/security/",
        "controles y pruebas",
    ),
    (
        "OWASP — Smart Contract Top 10",
        "https://scs.owasp.org/sctop10/",
        "riesgos de autorización y reentrada",
    ),
    (
        "Solidity — Security Considerations",
        "https://docs.soliditylang.org/en/latest/security-considerations.html",
        "llamadas externas y checks-effects-interactions",
    ),
    (
        "Ethereum Foundation — Critical Update Re: DAO Vulnerability",
        "https://blog.ethereum.org/en/2016/06/17/critical-update-re-dao-vulnerability",
        "descripción contemporánea del incidente",
    ),
    (
        "Ethereum Foundation — Hard Fork Completed",
        "https://blog.ethereum.org/en/2016/07/20/hard-fork-completed",
        "implementación de la respuesta al incidente",
    ),
    (
        "Ethereum.org — Ethereum forks",
        "https://ethereum.org/ethereum-forks/",
        "DAO fork y continuidad de Ethereum Classic",
    ),
)


def timestamp(seconds: int) -> str:
    minutes, remainder = divmod(seconds, 60)
    return f"{minutes:02d}:{remainder:02d}"


def notes(clip: Clip) -> str:
    starts = accumulate((beat.seconds for beat in clip.beats), initial=0)
    return "\n\n".join(
        f"{timestamp(start)}  {beat.speech}"
        for start, beat in zip(starts, clip.beats, strict=False)
    )


def markdown() -> str:
    lines = [
        "# Integrante 7 · Ataques y vulnerabilidades en blockchain",
        "",
        "Tecnologías de Seguridad · EPN",
        "",
        (
            "El recorrido dura **6:20**. Quedan **40 s** para pausas y cambios de "
            "diapositiva dentro del límite de 7:00. Los tiempos de la izquierda son "
            "acumulados y los de la derecha se cuentan desde el inicio de cada clip."
        ),
    ]
    elapsed = 0
    for index, clip in enumerate(CLIPS, 1):
        end = elapsed + clip.seconds
        lines.extend(
            (
                "",
                f"## {index:02d} · {clip.title} ({timestamp(elapsed)}–{timestamp(end)})",
                "",
                f"Clip `{index:02d}_{clip.id}.mp4` · {clip.seconds} s",
                "",
            )
        )
        for beat in clip.beats:
            local = elapsed - end + clip.seconds
            lines.extend(
                (
                    f"**{timestamp(elapsed)} · +{timestamp(local)}**  ",
                    f"*{beat.visual}*",
                    "",
                    f"> {beat.speech}",
                    "",
                )
            )
            elapsed += beat.seconds
    lines.extend(("## Fuentes", ""))
    lines.extend(f"- [{title}]({url}) · {scope}." for title, url, scope in SOURCES)
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    print(markdown(), end="")  # noqa: T201
