import discord
from discord import app_commands
import random
from typing import List, Optional
from teams import format_teams, generate_teams, TeamsContainer
from loguru import logger
import os
import sys
from tempfile import TemporaryDirectory
import subprocess
from shutil import which
from pathlib import Path

BOT_VERSION = "0.2.0"

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

adjectives = []
nouns = []
nouns_plural = []
verbs = []

rusty_sussy_path = None


@client.event
async def on_ready():
    await tree.sync()
    logger.info(f"Bot logged in as {client.user}")


@tree.command(name="bone-teams", description="Generate teams from a channel")
@app_commands.describe(
    team_size="Number of members per team",
    channel="The channel to pull team members from",
)
async def teams(
    interaction: discord.Interaction,
    channel: discord.VoiceChannel,
    team_size: Optional[int] = None,
    team_count: Optional[int] = None,
):
    logger.info(
        f"Running 'bone-teams' for '{interaction.user.display_name}' "
        f"with `channel`: {channel}, `team-size`: {team_size}, `team-count`: {team_count}"
    )

    if len(channel.members) == 0:
        logger.info(f"Channel: {channel} has no members, sending error message")
        await interaction.response.send_message(
            f"No members in {channel.name}", ephemeral=True
        )
        return

    if not team_size and team_count:
        team_count = 2

    t = generate_teams(channel.members, team_size, team_count)
    name_teams(t)
    response = format_teams(t)

    logger.info(f"Teams generated, sending response")
    await interaction.response.send_message(response)


@tree.command(
    name="bone-about",
    description="Names and shames the people responsible for this bot",
)
async def about(interaction: discord.Interaction):
    logger.info(f"Running 'bone-about' for {interaction.user.display_name}")
    await interaction.response.send_message(
        f""" Bone Bot v{BOT_VERSION}
Code by: <@277914802071011328>
Art by: <@551533880432263201>
Contribute to the problem @ <https://github.com/The-Dogghouse/bone-bot>
Our versioning scheme <https://0ver.org/>
    """
    )  # Links are in <> to supress the embed


def name_teams(t: TeamsContainer):
    for team in t.teams:
        team.name = (
            f"{random.choice(adjectives).title()} {random.choice(nouns_plural).title()}"
        )

    if t.extras is not None:
        t.extras.name = (
            f"{random.choice(adjectives).title()} {random.choice(nouns_plural).title()}"
        )


@tree.command(name="bone-sus", description="Bring the crew-mates in on an image")
@app_commands.describe(
    image="Image to sussify", width="Number of horizontal crew-mates per row"
)
async def bone_sus(
    interaction: discord.Interaction, image: discord.Attachment, width: Optional[int]
):
    await interaction.response.defer(thinking=True)
    logger.info(
        f"Running 'bone-sus' for {interaction.user.display_name} with `image`: `{image}`, `width`: `{width}`"
    )

    if rusty_sussy_path is None:
        await interaction.followup.send(
            "`rusty-sussy` not installed sussy baka!", ephemeral=True
        )
        return

    if width is None:
        width = 21  # the default from `rusty-sussy`

    if not image.content_type or not image.content_type.startswith("image/"):
        await interaction.followup.send(
            "I need an image you sussy baka!", ephemeral=True
        )
        return

    with TemporaryDirectory() as tmp_dir:
        input_path = tmp_dir + "/" + image.filename
        output_path = tmp_dir + "/output.gif"

        logger.info(f"Saving input image `{image.filename}` to `{input_path}`")

        image_bytes = await image.read()
        with open(input_path, "wb") as f:
            f.write(image_bytes)

        logger.info(f"Input image saved to `{input_path}`, running `rusty-sussy`")

        sussy_result = subprocess.run(
            [
                rusty_sussy_path,
                f"--input={input_path}",
                f"--output={output_path}",
                f"--width={width}",
            ],
            capture_output=True,
        )

        if sussy_result.returncode != 0:
            logger.error(
                f"Failed running 'bone-sus' for {interaction.user.display_name} with "
                "`image`: `{image}`, "
                "`width`: `{width}`, "
                "`stderr`: `{sussy_result.stderr}`, "
                "`stdout`: `{sussy_result.stdout}`"
            )
            await interaction.followup.send(f"Error sussing image!", ephemeral=True)
            return

        logger.info(
            f"Successfully sussed `{input_path}`, into `{output_path}`, replying to {interaction.user.display_name}"
        )

        with open(output_path, "rb") as f:
            discord_file = discord.File(f, filename="sussed.gif")
            await interaction.followup.send(file=discord_file)


def read_file(file: str) -> List[str]:
    logger.info(f"Reading `{file}`")
    with open(file) as file:
        return [line.rstrip() for line in file]


def find_sussy():
    logger.info("Detecting `rusty-sussy` path")

    logger.info("Checking PATH for `rusty-sussy`")
    candidate = which("rusty-sussy")
    if candidate is not None:
        logger.info("Detected `rusty-sussy` in PATH")
        return "rusty-sussy"

    candidate = Path("./rusty-sussy")
    logger.info(f"Checking `{candidate}` for `rusty-sussy`")
    # make sure this isn't the project directory
    if candidate.exists() and candidate.is_file():
        logger.info("Detected `rusty-sussy` in local root")
        return "./rusty-sussy"

    candidate = Path("rusty-sussy/target/release/rusty-sussy")
    logger.info(f"Checking `{candidate}` for `rusty-sussy`")
    if candidate.exists() and candidate.is_file():
        logger.info(f"Detected `rusty-sussy` in `{candidate}`")
        return str(candidate)
    return None


if __name__ == "__main__":
    logger.info(f"Starting Bone Bot v{BOT_VERSION}")

    token = ""
    if "BONE_TOKEN" in os.environ:
        token = os.environ["BONE_TOKEN"]
        if len(token) > 255 and token.find("VmFwb3Jlb24") != -1:
            logger.error("Specify the real token please")
            sys.exit(1)
    else:
        logger.error(
            "Specify the Discord token in the `BONE_TOKEN` environment variable"
        )
        sys.exit(1)

    logger.info("Reading in words")
    adjectives = read_file("resources/adjectives.txt")
    nouns = read_file("resources/nouns.txt")
    nouns_plural = read_file("resources/nouns-plural.txt")
    verbs = read_file("resources/verbs.txt")

    rusty_sussy_path = find_sussy()

    client.run(token=token)
