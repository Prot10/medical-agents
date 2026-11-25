"""Agent mode: a physician works a case exactly as the agent does.

The physician receives the presentation the agent receives, orders tools from the catalogue the
agent is given, reads the observations the agent would read and submits the same structured
assessment. Nothing here re-implements the harness: ``engine`` drives the policy loop, the model
adapter, the environment and the transcript codec with the physician standing where the model
server stands.
"""
