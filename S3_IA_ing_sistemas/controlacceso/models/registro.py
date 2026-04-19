from datetime import datetime
from dataclasses import dataclass, asdict
import json


@dataclass
class Registro:
    nombre_empleado: str
    ingresa_computador: bool
    fecha_hora_entrada: str = None
    marca_computador: str = None
    serial_computador: str = None
    persona_autoriza: str = None

    def __post_init__(self):
        if self.fecha_hora_entrada is None:
            self.fecha_hora_entrada = datetime.now().isoformat()
        if self.ingresa_computador:
            if not all([self.marca_computador, self.serial_computador, self.persona_autoriza]):
                raise ValueError("Si ingresa con computador, marca, serial y autorizador son obligatorios")

    def to_dict(self):
        return asdict(self)

    def to_line(self):
        return json.dumps(self.to_dict(), ensure_ascii=False)

    @staticmethod
    def from_line(line):
        return Registro(**json.loads(line))