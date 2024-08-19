"""Setup configuration for lice2."""

from simple_toml_settings import TOMLSettings


class Settings(TOMLSettings):
    """Settings for lice2."""

    default_license: str = "bsd3"
    organization: str = ""


settings = Settings.get_instance(
    "lice", xdg_config=True, auto_create=True, schema_version="1"
)
