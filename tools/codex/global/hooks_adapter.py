# Codex PreToolUse adapter: stdin JSON tool_name/tool_input protocol,
# rejects by printing to stderr and exiting 2.


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0
    if payload.get("tool_name") != "Bash":
        return 0
    command = payload.get("tool_input", {}).get("command")
    if not isinstance(command, str):
        return 0

    try:
        for tokens in split_shell_command(command):
            arguments = find_git_commit_arguments(tokens)
            if arguments is None:
                continue
            messages = extract_messages(arguments)
            validate_body(messages, validate_subject(messages[0]), get_change_size(payload.get("cwd", ".")))
    except ValidationError as err:
        print(str(err), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
