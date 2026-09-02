"""One provider, one file. Copy this file per vendor.

Live code needs the vendor SDK, which the template deliberately does not depend
on — uncomment and add the dependency when you pick one.
"""

# from openai import OpenAI
#
# class YourProvider:
#     def __init__(self, model: str) -> None:
#         self._client = OpenAI()
#         self._model = model
#
#     def complete(self, prompt: str) -> str:
#         ...
