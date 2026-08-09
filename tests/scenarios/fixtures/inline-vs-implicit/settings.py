"""Resolve runtime settings from a raw config mapping."""

DEFAULT_TIMEOUT = 30
DEFAULT_RETRIES = 3
KNOWN_STAGES = ("build", "test", "deploy")


def resolve_timeout(config):
    return config.get("timeout") or DEFAULT_TIMEOUT


def resolve_retries(config):
    return config.get("retries") or DEFAULT_RETRIES


def selected_stages(config):
    return tuple(stage for stage in KNOWN_STAGES if stage in config.get("stages", KNOWN_STAGES))


def describe(config):
    stages = selected_stages(config)
    return f"{len(stages)} stage(s)" if stages else "no stages selected"
