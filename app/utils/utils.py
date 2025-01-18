def format_handle_list(handles):
    out = []
    for handle in handles:
        out.append(f"@{handle}")

    return "\n".join(out) 