"""
story.py - Narrative text for Docker Quest
Theme: Container breach forensics. A Containment Specialist auditing a corp's
       infrastructure after a container escape and data exfiltration event.
"""

INTRO_STORY = """
The breach notification came in at [bold cyan]3:11 AM[/bold cyan].

[bold white]Fourteen months of transaction records.[/bold white] Exfiltrated from a containerized
microservice running inside a corp's "air-gapped" datacenter. The attacker
didn't break the encryption. They didn't social-engineer the credentials.
They broke containment — found a misconfigured container, escaped the namespace,
traversed the host filesystem, and walked out with everything.

By the time the SIEM triggered, the container had been stopped and deleted.
The image was still in the registry. The compose files were still on the server.
The logs were still there, if you knew how to read them.

[bold white]You are a Containment Specialist.[/bold white]

[bold magenta]Independent contractor. Infrastructure forensics. You've done this six times in the
last two years — corps that thought "containerized" meant "secured." It doesn't.
A container is an isolation boundary, not a vault. The difference matters
when someone is determined to find out where the boundary is weak.[/bold magenta]

You've been handed access to a mirror of the client's container environment.
Every image, every volume, every network configuration, every compose file.
Your job: understand exactly how the breach happened, and map every misconfiguration
that made it possible.

The client's legal team is watching everything you touch.
Every command you run is being logged.

[bold cyan]The environment is live. The containers are waiting. Start from the surface.[/bold cyan]
"""

ZONE_INTROS = {
    "surface_layer": """
[bold cyan]== THE SURFACE LAYER ==[/bold cyan]

Every breach investigation starts here — with what's running.

Before you can understand what went wrong, you need to understand what the
attacker saw when they first got a foothold in this environment. What images
were available? What containers were running? What was the corp pulling from
which registries, and when?

[yellow]docker pull[/yellow] — download an image from a registry.
[yellow]docker run[/yellow] — create and start a container from an image.
[yellow]docker ps[/yellow] — list running containers.
[yellow]docker images[/yellow] — list locally cached images.

[italic]"The first thing an attacker does after getting access is the same thing
you're doing now: figure out what's here."[/italic]
""",
    "image_vault": """
[bold cyan]== THE IMAGE VAULT ==[/bold cyan]

Images are the blueprints. Containers are the instances.

The compromised service was running from an image that had [bold white]four years[/bold white] of
accumulated layers. Base image last updated in 2020. Packages patched some of them,
skipped others. A dependency in layer 3 had a known CVE — exploitable, local privilege
escalation, patch available since 2021.

They never rebuilt the image. The layer was just sitting there.

[yellow]docker inspect[/yellow] — show detailed metadata for an image or container.
[yellow]docker history[/yellow] — show the layer-by-layer build history of an image.
[yellow]docker tag[/yellow] — create a new tag pointing to an existing image.
[yellow]docker rmi[/yellow] — remove an image from local storage.

[italic]"An image is not a static thing. It's a stack of decisions, each one
recorded in a layer, each layer immutable, each one potentially a mistake."[/italic]
""",
    "container_grid": """
[bold cyan]== THE CONTAINER GRID ==[/bold cyan]

Containers don't exist in isolation. They have lifecycle states, they produce logs,
they contain files, and — critically — they can be entered while they're running.

The attacker had [yellow]exec[/yellow] access to the compromised container through a debugging
endpoint that was left open in production. They didn't need to exploit the CVE
directly — they walked in through the front door.

[yellow]docker exec[/yellow] — execute a command inside a running container.
[yellow]docker logs[/yellow] — view stdout/stderr from a container.
[yellow]docker cp[/yellow] — copy files between container and host.
[yellow]docker stop[/yellow] / [yellow]docker rm[/yellow] — stop and remove containers.

[italic]"The exec endpoint was for developer convenience. In production,
'developer convenience' means 'attacker convenience.'"[/italic]
""",
    "port_matrix": """
[bold cyan]== THE PORT MATRIX ==[/bold cyan]

Containers are isolated — until you open a port.

The compromised service had three ports published. One of them was documented.
The other two were from a compose file override that was committed to the repo,
reverted, and then manually applied to the production server. The revert didn't
touch the running containers.

Port 9229. Node.js debug protocol. Unauthenticated. Published to [bold red]0.0.0.0[/bold red].

[yellow]-p host:container[/yellow] — publish a container port to the host.
[yellow]docker port[/yellow] — show port mappings for a running container.
[yellow]-P[/yellow] — publish all EXPOSE'd ports to random host ports.
[yellow]EXPOSE[/yellow] — document a container's intended ports (doesn't publish them).

[italic]"EXPOSE is documentation. -p is reality. The breach happened because
someone confused the two."[/italic]
""",
    "volume_sanctum": """
[bold cyan]== THE VOLUME SANCTUM ==[/bold cyan]

Volumes are how containers persist data. They're also how the host filesystem
ends up inside a container.

The bind mount audit is the most damning part of the report so far. Three
microservices had [yellow]-v /:/host[/yellow] in their run configuration — the entire host
filesystem mounted read-write into each container. Someone thought it was a
"convenience for debugging" during the initial deployment. Nobody removed it.

[yellow]docker volume create[/yellow] — create a named volume.
[yellow]-v name:path[/yellow] — mount a named volume.
[yellow]-v /host/path:/container/path[/yellow] — bind mount from host.
[yellow]docker volume ls[/yellow] / [yellow]docker volume inspect[/yellow] — list and examine volumes.

[italic]"A bind mount of the root filesystem is not a misconfiguration.
It's an open door with a neon sign."[/italic]
""",
    "network_forge": """
[bold cyan]== THE NETWORK FORGE ==[/bold cyan]

Containers on the same Docker network can reach each other by name.
By default, every container on the default bridge network can reach every
other container on that network.

The compromised container was on the default bridge. So was the internal
payment service. Direct TCP access. No authentication layer between them.

[yellow]docker network ls[/yellow] — list networks.
[yellow]docker network create[/yellow] — create a custom network.
[yellow]docker network connect[/yellow] — connect a container to a network.
[yellow]docker network inspect[/yellow] — examine network configuration and connected containers.

[italic]"Network segmentation exists for a reason. 'Default bridge' means
everyone is in the same room."[/italic]
""",
    "build_engine": """
[bold cyan]== THE BUILD ENGINE ==[/bold cyan]

Every image starts with a Dockerfile. Every Dockerfile is a record of every
decision made during the build. The decisions are immutable once committed to
a layer.

The Dockerfile for the compromised service had [yellow]RUN chmod 777 /app[/yellow] in layer 7.
It had [yellow]USER root[/yellow] throughout. It had credentials baked into a [yellow]RUN[/yellow] instruction
— removed in a later [yellow]RUN[/yellow], but still present in the intermediate layer,
readable with [yellow]docker history[/yellow].

[yellow]FROM[/yellow] — set the base image.
[yellow]RUN[/yellow] — execute a command during build; creates a new layer.
[yellow]COPY[/yellow] / [yellow]ADD[/yellow] — add files to the image.
[yellow]WORKDIR[/yellow] / [yellow]USER[/yellow] / [yellow]CMD[/yellow] / [yellow]ENTRYPOINT[/yellow] — runtime configuration.

[italic]"The Dockerfile is a confession. You just have to know how to read it."[/italic]
""",
    "compose_matrix": """
[bold cyan]== THE COMPOSE MATRIX ==[/bold cyan]

Docker Compose is how you run systems, not just containers.
Multiple services, shared networks, volume definitions, environment files —
all declared in a single YAML and applied with a single command.

The production compose file was version-controlled. The overrides were not.
A [yellow]docker-compose.override.yml[/yellow] on the production server, never committed,
never reviewed, quietly enabling the debug ports and the bind mounts every
time someone ran [yellow]docker compose up[/yellow].

[yellow]docker compose up[/yellow] / [yellow]docker compose down[/yellow] — start/stop the full stack.
[yellow]docker compose logs[/yellow] — aggregate logs from all services.
[yellow]docker compose exec[/yellow] — exec into a running compose service.
[yellow]docker compose ps[/yellow] — show running compose services.

[italic]"The override file was invisible in the repo and omnipresent on the server.
That's not an accident. That's a methodology."[/italic]
""",
    "registry_core": """
[bold cyan]== THE REGISTRY CORE ==[/bold cyan]

The registry is where images live between builds and deployments.
It's also where the attacker pulled the updated backdoored image from —
after pushing it with the same tag as the legitimate service.

The push happened [bold white]six hours before the breach[/bold white]. Nobody noticed a new push to
a production tag. There were no alerts configured for registry write events.
The CI/CD pipeline pulled and deployed it automatically.

The final zone. The complete picture.

[yellow]docker push[/yellow] / [yellow]docker pull[/yellow] — exchange images with a registry.
[yellow]docker login[/yellow] — authenticate to a registry.
[yellow]docker tag[/yellow] — create a new reference to an image.
[yellow]docker system df[/yellow] / [yellow]docker system prune[/yellow] — audit and clean up disk usage.

[italic]"The registry is not just storage. It's the distribution mechanism.
Whoever controls the registry controls what runs."[/italic]
""",
}

ZONE_COMPLETIONS = {
    "surface_layer": """
[bold green]THE SURFACE LAYER — MAPPED.[/bold green]

You know what was running. You know what images were cached locally and which
registries they came from. You've run [cyan]docker ps -a[/cyan] and seen the stopped containers
that nobody cleaned up, still holding their logs, still holding their filesystem
state until someone runs [cyan]docker rm[/cyan].

They didn't run [cyan]docker rm[/cyan].

[bold cyan]The Image Vault is next. The layers tell the full story.[/bold cyan]
""",
    "image_vault": """
[bold green]THE IMAGE VAULT — AUDITED.[/bold green]

Layer by layer. [cyan]docker history[/cyan] showed the full build sequence.
[cyan]docker inspect[/cyan] surfaced the exposed ports, the volumes, the environment variables
baked in at build time. The base image tag was [cyan]latest[/cyan] — meaning the build was
non-reproducible, meaning you can't guarantee the image on the server matches
what the Dockerfile would produce today.

The CVE in layer 3 is now a line item in the report.

[bold cyan]The Container Grid: what was running, what was accessible, what was entered.[/bold cyan]
""",
    "commit_ledger": """
[bold green]THE COMMIT LEDGER — READ.[/bold green]

Every commit. Every author. Every timestamp. Every message.

[bold cyan]The Container Grid: what was running, what was accessible, what was entered.[/bold cyan]
""",
    "container_grid": """
[bold green]THE CONTAINER GRID — CLEARED.[/bold green]

You can move through running containers now. [cyan]docker exec[/cyan], [cyan]docker logs[/cyan],
[cyan]docker cp[/cyan] — the full toolkit for reading a container's state without stopping it.

The debug endpoint logs confirmed it: seventeen distinct exec sessions in
the forty-eight hours before the breach. All from the same source IP.
All authenticated with a valid token that was rotated [bold white]after[/bold white] the breach.

[bold cyan]The Port Matrix. Why was port 9229 published to the world?[/bold cyan]
""",
    "port_matrix": """
[bold green]THE PORT MATRIX — MAPPED.[/bold green]

Every port. Every binding. The difference between [cyan]EXPOSE[/cyan] (documentation)
and [cyan]-p[/cyan] (actual publication to the host). The difference between binding to
[cyan]127.0.0.1[/cyan] (local only) and [cyan]0.0.0.0[/cyan] (every interface, including public).

Port 9229 was bound to [cyan]0.0.0.0[/cyan]. The entire internet could reach
the Node.js debugger. This is in the report. This is one of the findings.

[bold cyan]The Volume Sanctum. The bind mounts that shouldn't exist.[/bold cyan]
""",
    "volume_sanctum": """
[bold green]THE VOLUME SANCTUM — EXCAVATED.[/bold green]

Named volumes, bind mounts, tmpfs — you know the difference between all of them now.
You know that [cyan]-v /:/host[/cyan] is not a convenience feature; it's a complete erasure
of the container's isolation boundary.

Three services. All with root filesystem mounts. All with read-write access.
The attacker had a choice of three doors. They picked the least-monitored one.

[bold cyan]The Network Forge. Who could talk to whom, and why.[/bold cyan]
""",
    "network_forge": """
[bold green]THE NETWORK FORGE — CHARTED.[/bold green]

The default bridge. Custom networks. DNS resolution between containers.
The fact that services on the same custom network can reach each other by
service name — which is useful in development and catastrophic when the
compromised container is on the same network as the payment service.

Two services that should never have been able to reach each other
had been talking to each other for [bold white]eight months[/bold white].

[bold cyan]The Build Engine. Read the Dockerfile like a confession.[/bold cyan]
""",
    "build_engine": """
[bold green]THE BUILD ENGINE — DECODED.[/bold green]

FROM. RUN. COPY. WORKDIR. USER. CMD. ENTRYPOINT.

The Dockerfile is a recipe. Every [cyan]RUN[/cyan] instruction creates a layer.
Every layer is permanent. The credentials that were added in layer 5 and
"removed" in layer 6 are still readable in layer 5 — [cyan]docker history[/cyan] can
pull the intermediate layers if the cache is intact.

The cache was intact.

[bold cyan]The Compose Matrix. The override file that changed everything.[/bold cyan]
""",
    "compose_matrix": """
[bold green]THE COMPOSE MATRIX — RECONSTRUCTED.[/bold green]

The compose file was clean. The override was not. [cyan]docker compose up[/cyan] merges both
automatically — the override is applied silently, on top of the base config,
with no indication in the logs that it's running a different configuration
than what's in the repository.

The override was the mechanism. The registry push was the payload.

[bold cyan]The Registry Core. Final phase. Complete the picture.[/bold cyan]
""",
    "registry_core": """
[bold yellow]★ ★ ★  THE REGISTRY CORE — BREACH FULLY RECONSTRUCTED.  ★ ★ ★[/bold yellow]

[bold white]The report is complete.[/bold white]

Timeline:
  [cyan]T-72h[/cyan]  Attacker discovers exposed port 9229 via internet scan.
  [cyan]T-48h[/cyan]  Seventeen exec sessions via the debug endpoint. Reconnaissance.
  [cyan]T-6h[/cyan]   Backdoored image pushed to registry under the same production tag.
  [cyan]T-4h[/cyan]   CI/CD pipeline deploys the new image automatically.
  [cyan]T-0[/cyan]    Container reads /host (thanks to the bind mount),
          reaches the payment service (thanks to shared network),
          and exfiltrates 14 months of transaction records.
  [cyan]T+3h[/cyan]   SIEM triggers. Container stopped. Data already gone.

Root causes: [bold white]nine distinct misconfigurations.[/bold white] All documented.
All preventable. All present in the Dockerfile, the compose file, the
override, or the runtime configuration. None of them were secrets.
They were just never audited.

[bold magenta]The container is not the threat. The configuration is the threat.
Now you know how to read the configuration.[/bold magenta]

[bold yellow]CONTAINMENT SPECIALIST STATUS: GRANDMASTER.  BREACH: FULLY DOCUMENTED.[/bold yellow]
""",
}

BOSS_INTROS = {
    "surface_layer": "[bold red]⚠  ENVIRONMENT AUDIT: The Initial Survey[/bold red]\nWhat was running when the breach happened? Prove you can read a live container environment from scratch.",
    "image_vault": "[bold red]⚠  IMAGE FORENSICS: The Layer Audit[/bold red]\nFour years of layers. One CVE buried in layer 3. Find the commands to expose it.",
    "container_grid": "[bold red]⚠  LIVE CONTAINER ACCESS: The Exec Challenge[/bold red]\nThe debug endpoint is open. Prove you can navigate a running container the way the attacker did.",
    "port_matrix": "[bold red]⚠  PORT ANALYSIS: The 0.0.0.0 Problem[/bold red]\nPort 9229. Published everywhere. Prove you understand why that matters.",
    "volume_sanctum": "[bold red]⚠  BIND MOUNT AUDIT: The Open Door[/bold red]\nThree services with root filesystem mounts. Demonstrate you understand exactly what that means.",
    "network_forge": "[bold red]⚠  NETWORK SEGMENTATION: The Default Bridge Problem[/bold red]\nThe payment service was reachable from the compromised container. Prove you understand how Docker networking allowed it.",
    "build_engine": "[bold red]⚠  DOCKERFILE ANALYSIS: The Confession[/bold red]\nCredentials baked into layer 5. Removed in layer 6. Still readable. Prove you know how.",
    "compose_matrix": "[bold red]⚠  COMPOSE OVERRIDE: The Silent Configuration[/bold red]\ndocker compose up reads the override automatically. Prove you know the full compose command set.",
    "registry_core": "[bold red]★  REGISTRY AUDIT: The Final Phase[/bold red]\nThe backdoored image was pushed six hours before the breach. Complete the picture — registry operations, system audit, and the commands that close the case.",
}

ACHIEVEMENT_DESCRIPTIONS = {
    "first_blood": ("First Container Inspected", "Read your first docker object. The environment acknowledged your access."),
    "navigator": ("Surface Mapped", "Cleared the Surface Layer. You know what was running, what was cached, and what the attacker saw first."),
    "archivist": ("Image Auditor", "Cleared the Image Vault. Layer by layer. CVEs don't hide from docker history."),
    "seeker": ("Container Operative", "Cleared the Container Grid. exec, logs, cp — you move through running containers like you own them."),
    "pipe_dream": ("Port Analyst", "Cleared the Port Matrix. You know the difference between EXPOSE and reality."),
    "necromancer": ("Volume Archaeologist", "Cleared the Volume Sanctum. Bind mounts are not conveniences. You know what they actually are."),
    "warden": ("Network Auditor", "Cleared the Network Forge. The default bridge is not a security boundary. Documented."),
    "scriptor": ("Build Analyst", "Cleared the Build Engine. The Dockerfile is a confession. You read it fluently."),
    "networked": ("Compose Specialist", "Cleared the Compose Matrix. You found the override. You understand why it mattered."),
    "grandmaster": ("CONTAINMENT SPECIALIST: GRANDMASTER", "Cleared the Registry Core. The breach is fully documented. Nine misconfigurations. All preventable. None of them secrets."),
    "streak_3": ("Clean Run", "3 correct in a row. Your docker knowledge is starting to flow."),
    "streak_5": ("Cached Layer", "5 in a row. You're building knowledge the way Docker builds images — incrementally, reproducibly."),
    "streak_10": ("IMMUTABLE LAYER", "10 in a row. Your understanding is now a permanent layer. Cannot be overwritten. Cannot be removed."),
    "no_hints": ("No Hints Needed", "Cleared a zone without hints. The man page is already in your head."),
    "speed_demon": ("Sub-5 Command", "Answered in under 5 seconds. The command was already running before you finished reading the prompt."),
    "level_10": ("Junior Specialist", "Level 10. docker ps is starting to feel like reading the news."),
    "level_20": ("Senior Specialist", "Level 20. You read Dockerfiles the way other people read error messages — quickly and without surprise."),
    "level_30": ("Master Containment Specialist", "Maximum level. You understand containers from image layers to compose orchestration. Courts have accepted your audit reports."),
    "completionist": ("Full Environment Audited", "Every zone. Every challenge. Total container forensics achieved."),
    "boss_slayer": ("Misconfiguration Found", "Beat your first boss challenge. The container thought it was hidden. It wasn't."),
}
