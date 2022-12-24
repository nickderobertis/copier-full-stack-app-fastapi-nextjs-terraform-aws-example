import os
from pathlib import Path

from pydantic import BaseSettings


def settings_to_tf_env_str(settings: BaseSettings, prefix: str = "TF_VAR_") -> str:
    """
    Convert settings to Terraform environment variable string.
    """
    outputs: list[str] = []
    for k, v in settings._iter():
        if isinstance(v, BaseSettings):
            outputs.append(
                settings_to_tf_env_str(v, prefix=f"{prefix}{v.Config.env_prefix}")
            )
        else:
            var_name = f"{prefix}{k}".upper()
            outputs.append(f"{var_name}={v}")
    return "\n".join(outputs)


def settings_to_tf_env_file(settings: BaseSettings, out_path: os.PathLike) -> None:
    """
    Convert settings to Terraform environment variable file.
    """
    with open(out_path, "w") as f:
        f.write(settings_to_tf_env_str(settings))


if __name__ == "__main__":
    from settings.main import SETTINGS

    tf_env_out_path = Path(__file__).parent.parent / ".env.terraform"
    settings_to_tf_env_file(settings=SETTINGS, out_path=tf_env_out_path)
