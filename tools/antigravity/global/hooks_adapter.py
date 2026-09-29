# Antigravity PreToolUse adapter: toolCall/args protocol, responds with a
# JSON {"decision": "allow"|"deny", "reason"?: str} line on stdout.


def respond(decision: str, reason: str | None = None) -> None:
    payload: dict[str, str] = {"decision": decision}
    if reason:
        payload["reason"] = reason
    print(json.dumps(payload))
    sys.exit(0)


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        respond("allow")

    tool_call = payload.get("toolCall", {})
    if tool_call.get("name") != "run_command":
        respond("allow")

    args = tool_call.get("args", {})
    command = args.get("CommandLine")
    if not isinstance(command, str):
        respond("allow")

    cwd = args.get("Cwd")
    if not cwd:
        workspace_paths = payload.get("workspacePaths", [])
        cwd = workspace_paths[0] if workspace_paths else "."

    try:
        for tokens in split_shell_command(command):
            arguments = find_git_commit_arguments(tokens)
            if arguments is None:
                continue
            messages = extract_messages(arguments)
            validate_body(messages, validate_subject(messages[0]), get_change_size(cwd))
    except ValidationError as err:
        respond("deny", str(err))

    respond("allow")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
