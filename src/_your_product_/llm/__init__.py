"""The provider seam — the strongest convention in the corpus (9 of 10 repos).

Every model call goes through here, and nothing else imports a provider SDK.
The payoff: swapping provider, adding a retry or capping a budget is one file,
and grepping for the SDK name returns exactly this directory.
"""
