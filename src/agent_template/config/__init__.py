"""Settings, read once, validated at startup.

Belongs here: the settings model and its loading. Environment variable names are
documented in `.env.example`; values never are.

Read configuration here and pass it down. A module that reaches for `os.environ`
in the middle of a call cannot be tested without mutating the process.
"""
