"""HTML inventory for the full node: the agents that are online right now."""

from html import escape

ONLINE_SECONDS = 5 * 60   # an agent sends its status every 2 minutes; silent for 5 minutes = gone


def render_agents(rows, now):
    online_count = threads = ram = vram = 0
    body = []
    rows = [r for r in rows if max(0, now - r["last_seen"]) < ONLINE_SECONDS]
    for row in rows:
        age = max(0, now - row["last_seen"])
        online_count += 1
        threads += row.get("cpu_threads", 0)
        ram += row.get("ram_mb", 0)
        gpu_lines = []
        for gpu in row.get("gpus", []):
            memory = gpu["vram_mb"]
            vram += memory
            label = escape(gpu["name"]) or "Unknown GPU"
            gpu_lines.append(f"{label} ({memory:,} MiB)" if memory else label)

        key = escape(row["agent"])
        platform = " / ".join(escape(row[k]) for k in ("os", "arch") if row.get(k))
        if row["legacy"]:
            version = "Legacy version"
            count = row["result_count"]
            units = f'{count:,} result{"s" if count != 1 else ""}'
        else:
            version = escape(row["version"])
            units = f'{row["units_done"]:,}'
        seen = f"{int(age)} s ago" if age < 60 else f"{int(age // 60)} min {int(age % 60)} s ago"
        cells = (
            f'<code title="{key}">{key[:12]}</code>', platform or "—",
            escape(row.get("cpu_model", "")) or "—", row.get("cpu_threads") or "—",
            f'{row["ram_mb"]:,} MiB' if row.get("ram_mb") else "—",
            "<br>".join(gpu_lines) or "—", version, units, seen,
        )
        body.append("<tr>" + "".join(f"<td>{cell}</td>" for cell in cells) + "</tr>")

    columns = ("Public key", "OS / arch", "CPU", "Threads", "RAM", "GPU / VRAM",
               "Version", "Units / results", "Last seen")
    heading = "".join(f'<th scope="col">{label}</th>' for label in columns)
    contents = "".join(body) or f'<tr><td colspan="{len(columns)}">No agent is online right now.</td></tr>'
    totals = (("Online agents", online_count), ("CPU threads", threads),
              ("RAM (MiB)", ram), ("VRAM (MiB)", vram))
    summary = "".join(f"<div><dt>{label}</dt><dd>{value:,}</dd></div>" for label, value in totals)
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta http-equiv="refresh" content="30">
<title>SkyNet agents</title><style>
body {{ margin: 2rem auto; max-width: 95rem; padding: 0 1rem; font: 1rem/1.5 Inter, system-ui, sans-serif; color: #192b39; }}
dl {{ display: flex; flex-wrap: wrap; gap: 1rem 3rem; }}
dt, th {{ font-weight: 600; }} dd {{ margin: 0; font-size: 1.5rem; }}
.table {{ overflow-x: auto; }} table {{ width: 100%; border-collapse: collapse; }}
th, td {{ padding: .55rem .7rem; text-align: left; border-bottom: 1px solid #ced8df; }}
th {{ background: #edf2f5; white-space: nowrap; }} .online {{ color: #15664c; }}
</style></head><body><main><h1>SkyNet agents</h1><dl>{summary}</dl>
<div class="table"><table><thead><tr>{heading}</tr></thead><tbody>{contents}</tbody></table></div>
<p>Online means a status or a result in the last 5 minutes; agents send their status every 2 minutes. The page refreshes every 30 seconds. <a href="/v1/agents">View as JSON</a></p></main></body></html>""".encode("utf-8")
