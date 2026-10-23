# Body — Procedures and Helpers

The `body/` area holds written workflows and optional helper scripts.

- A **workflow** is Markdown telling an agent how to handle a recurring task.
  The agent must be able to read it; support for slash commands or automatic
  invocation varies by host.
- A **script** is executable code. It can only run when the user or host
  explicitly runs it with the necessary permissions.
- A **tool** is a capability supplied by the host. The tools registry documents
  verified host tools; it does not install or activate them.
- **Design preferences** describe how the person likes technical or visual
  work to be approached; they are guidance, not a guarantee of output.

Do not describe an item in a registry as an available tool until its presence
and behavior have been verified in the actual host environment.
