import os
from typing import Annotated
from typer import Typer, Option, BadParameter
from rich.console import Console
from dataclasses import asdict

from core.config import Config
from services.voice_commands_manager import VoiceCommandsManager
from services.speech_recognizer import SpeechRecognizer
from services.listener import Listener
from repositories.voice_commands import VoiceCommands

CONFIG_PATH = "test.ini"
app = Typer()
console = Console()


@app.command()
def new(
    name: Annotated[str, Option("--name", "-n")],
    description: Annotated[str, Option("--description", "-d")],
    phrase: Annotated[str, Option("--phrase", "-ph")],
    exec: Annotated[str, Option("--exec", "-e")],
    shell: Annotated[bool, Option("--shell", "-sh")] = False,
    config_path: Annotated[str, Option("--config", "-cfg")] = CONFIG_PATH,
):
    config = Config(config_path)
    voice_commands_manager = VoiceCommandsManager(
        voice_commands=VoiceCommands(config=config)
    )
    voice_commands_manager.new_voice_command(
        name=name,
        description=description,
        exec=exec,
        phrase=phrase,
        shell=shell,
    )
    console.print("[green]Command was just created[/]")


@app.command()
def update(
    id: str,
    name: Annotated[str | None, Option("--name", "-n")] = None,
    description: Annotated[str | None, Option("--description", "-d")] = None,
    phrase: Annotated[str | None, Option("--phrase", "-ph")] = None,
    exec: Annotated[str | None, Option("--exec", "-e")] = None,
    shell: Annotated[bool | None, Option("--shell", "-sh")] = None,
    config_path: Annotated[str, Option("--config", "-cfg")] = CONFIG_PATH,
):
    config = Config(config_path)
    voice_commands_manager = VoiceCommandsManager(
        voice_commands=VoiceCommands(config=config)
    )
    if voice_commands_manager.update_voice_command(
        id=id,
        name=name,
        description=description,
        exec=exec,
        phrase=phrase,
        shell=shell,
    ):
        console.print("[green]Command was just updated[/]")
    else:
        console.print("[red]Command was not found[/]")


@app.command()
def delete(
    id: str,
    config_path: Annotated[str, Option("--config", "-cfg")] = CONFIG_PATH,
):
    config = Config(config_path)
    voice_commands_manager = VoiceCommandsManager(
        voice_commands=VoiceCommands(config=config)
    )
    if voice_commands_manager.delete_voice_command(id=id):
        console.print("[green]Command was just deleted[/]")
    else:
        console.print("[red]Command was not found[/]")


@app.command()
def find(
    id: str | None = None,
    phrase: Annotated[str | None, Option("--phrase", "-ph")] = None,
    config_path: Annotated[str, Option("--config", "-cfg")] = CONFIG_PATH,
):
    config = Config(config_path)
    voice_commands_manager = VoiceCommandsManager(
        voice_commands=VoiceCommands(config=config)
    )
    if id:
        voice_command = voice_commands_manager.get_voice_command_by_id(id=id)

    else:
        if not phrase:
            raise BadParameter("--phrase or --id is required")

        voice_command = voice_commands_manager.get_voice_command_by_phrase(
            phrase=phrase
        )

    if not voice_command:
        return console.print("[red]Command was not found[/]")

    console.print(
        f"Name: {voice_command.name}"
        f"Description: {voice_command.description}"
        f"Shell: {voice_command.shell}"
        f"Exec: {voice_command.exec}"
        f"Phrase: {voice_command.phrase}"
    )


@app.command()
def list(
    page_number: Annotated[int, Option("--page", "-p")],
    config_path: Annotated[str, Option("--config", "-cfg")] = CONFIG_PATH,
    is_raw: Annotated[bool, Option("--raw", "-r", is_flag=True)] = False,
):
    commands_per_page = 10
    page_number = abs(page_number)
    page_index = page_number - 1
    config = Config(config_path)
    voice_commands_manager = VoiceCommandsManager(
        voice_commands=VoiceCommands(config=config)
    )
    if voice_commands_list := voice_commands_manager.get_voice_commands_list():
        for voice_command in voice_commands_list[
            page_index
            * commands_per_page : min(
                max(0, page_index * commands_per_page + commands_per_page),
                len(voice_commands_list) - 1,
            )
        ]:
            if is_raw:
                print(asdict(voice_command))
            else:
                console.print(
                    f"Name: {voice_command.name}"
                    f"Description: {voice_command.description}"
                    f"Shell: {voice_command.shell}"
                    f"Exec: {voice_command.exec}"
                    f"Phrase: {voice_command.phrase}\n"
                )
    else:
        return console.print("[red]No defined commands[/]")


@app.command()
def activate(config_path: Annotated[str, Option("--config", "-cfg")] = CONFIG_PATH):
    config = Config(config_path)
    listener = Listener(config, callback=audio_callback)
    speech_recognizer = SpeechRecognizer(config)
    voice_commands_manager = VoiceCommandsManager(VoiceCommands(config))

    def audio_callback(audio):
        text = speech_recognizer.recognize_speech(audio)
        if voice_command := voice_commands_manager.get_voice_command_by_phrase(text):
            voice_commands_manager.run_voice_command(voice_command)
        else:
            console.print("[red]Unknown command[/]")

    open("active.flag", "w").close()
    console.print("[green]Started[/]")
    listener.start_listening()


@app.command()
def deactivate(config_path: Annotated[str, Option("--config", "-cfg")] = CONFIG_PATH):
    os.remove("active.flag")
    console.print("[green]Stopped[/]")


if __name__ == "__main__":
    app()
