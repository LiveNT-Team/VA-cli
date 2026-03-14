from dataclasses import dataclass


@dataclass(frozen=True)
class VoiceCommand:
    id: str
    name: str
    description: str
    exec: str
    phrase: str
    shell: bool

    def __str__(self) -> str:
        return (
            f"[bold]ID:[/] {self.id}\n"
            f"[bold]Name:[/] {self.name}\n"
            f"[bold]Description:[/] {self.description}\n"
            f"[bold]Shell:[/] {self.shell}\n"
            f"[bold]Exec:[/] {self.exec}\n"
            f"[bold]Phrase:[/] {self.phrase}"
        )


__all__ = ("VoiceCommand",)
