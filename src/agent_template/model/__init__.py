"""The single seam to the LLM provider.

The one surface present in all thirteen production repositories surveyed: every
call to a model goes through here, and nothing else in the package imports a
provider SDK.

The payoff is not elegance. It is that swapping a provider, adding a retry,
capping a token budget, or pinning a model version is one file — and that a
grep for the SDK name returns exactly this directory.
"""
