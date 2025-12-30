import os
import shutil
from database import add_bot
from config import BASE_BOTS_DIR, TEMPLATE_DIR
import subprocess


def create_folder(path):
    os.makedirs(path, exist_ok=True)


def write_env(path, data: dict):
    env_path = os.path.join(path, ".env")
    with open(env_path, "w") as f:
        for k, v in data.items():
            f.write(f"{k}={v}\n")


def deploy_music_bot(user_id, tg_id, form):
    base = os.path.join(TEMPLATE_DIR, "music_bot_base")
    folder = os.path.join(BASE_BOTS_DIR, f"{tg_id}_music")

    shutil.copytree(base, folder, dirs_exist_ok=True)

    write_env(folder, {
        "BOT_TOKEN": form["token"],
        "STRING_SESSION": form["string"],
        "LOGGER_ID": form["logger"],
        "OWNER_ID": form["owner"]
    })

    process_name = f"{tg_id}_music"

    subprocess.call(
        f"pm2 start main.py --name {process_name}",
        cwd=folder,
        shell=True
    )

    add_bot(user_id, "music", folder, process_name)
    return process_name


def deploy_chat_bot(user_id, tg_id, form):
    base = os.path.join(TEMPLATE_DIR, "chat_bot_base")
    folder = os.path.join(BASE_BOTS_DIR, f"{tg_id}_chat")

    shutil.copytree(base, folder, dirs_exist_ok=True)

    write_env(folder, {
        "BOT_TOKEN": form["token"],
        "OWNER_ID": form["owner"]
    })

    process_name = f"{tg_id}_chat"

    subprocess.call(
        f"pm2 start main.py --name {process_name}",
        cwd=folder,
        shell=True
    )

    add_bot(user_id, "chat", folder, process_name)
    return process_name
