import os

from dataclasses import dataclass, field

MACHINE_SESSION_MAX_INACTIVE_SECS = int(os.environ.get("MACHINE_SESSION_MAX_INACTIVE_SECS", "10"))

@dataclass()
class Machine:
    id: str
    aaa_count: int = field(default=0)
    aa_count: int = field(default=0)
    c_count: int = field(default=0)
    d_count: int = field(default=0)
    v9_count: int = field(default=0)


@dataclass
class MachineSession(Machine):
    inactive_countdown: int = field(default=MACHINE_SESSION_MAX_INACTIVE_SECS)
