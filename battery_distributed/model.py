from dataclasses import dataclass, field


@dataclass()
class Maquina:
    id: str
    quantidade_AAA: int = field(default=0)
    quantidade_AA: int = field(default=0)
    quantidade_C: int = field(default=0)
    quantidade_D: int = field(default=0)
    quantidade_V9: int = field(default=0)
