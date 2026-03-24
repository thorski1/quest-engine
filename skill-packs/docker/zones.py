"""
zones.py - All zone and challenge data for Docker Quest
Challenge types: quiz, flag_quiz, fill_blank
"""

ZONES = {
    "surface_layer": {
        "id": "surface_layer",
        "name": "The Surface Layer",
        "subtitle": "Pull, Run & Inspect Running Containers",
        "color": "cyan",
        "icon": "🐳",
        "commands": ["docker pull", "docker run", "docker ps", "docker images"],
        "challenges": [
            {
                "id": "surf_1",
                "type": "quiz",
                "title": "Pull the Image",
                "flavor": "The investigation starts with what's in the local image cache. But first — what command downloads an image from a registry?",
                "lesson": (
                    "docker pull — downloads an image from a registry to local storage.\n\n"
                    "Syntax: docker pull [registry/]image[:tag]\n\n"
                    "Examples:\n"
                    "  docker pull nginx           → pulls nginx:latest from Docker Hub\n"
                    "  docker pull nginx:1.25      → pulls a specific version\n"
                    "  docker pull ghcr.io/org/app → pulls from GitHub Container Registry\n\n"
                    "If no tag is specified, Docker pulls 'latest' — which is not\n"
                    "necessarily the most recent build. It's whatever the image author\n"
                    "tagged as 'latest' at publish time."
                ),
                "answer": "pull",
                "hints": [
                    "Think about what you do before you can run an image that isn't on the system yet.",
                    "The command is one word: docker ___",
                    "The answer is: pull",
                ],
            },
            {
                "id": "surf_2",
                "type": "fill_blank",
                "title": "Run Detached",
                "flavor": "You need to start an nginx container in the background — detached mode — so it keeps running after your terminal closes. Complete the command: docker run ___ nginx",
                "lesson": (
                    "docker run -d — starts a container in detached (background) mode.\n\n"
                    "Without -d: the container runs in the foreground, attached to your terminal.\n"
                    "   Ctrl+C stops the container.\n\n"
                    "With -d: the container runs as a background process.\n"
                    "   Docker prints the container ID and returns to the prompt.\n"
                    "   The container keeps running even when the terminal closes.\n\n"
                    "Other common docker run flags:\n"
                    "  --name mycontainer  → assign a name instead of a random one\n"
                    "  --rm                → automatically remove container when it stops\n"
                    "  -it                 → interactive mode with a TTY (for shells)\n"
                    "  -e KEY=VALUE        → set an environment variable"
                ),
                "answer": "-d",
                "hints": [
                    "Detached mode uses a single flag.",
                    "It's the same flag most CLI tools use for 'daemon' or 'detach': -d",
                    "The answer is: -d",
                ],
            },
            {
                "id": "surf_3",
                "type": "quiz",
                "title": "List Running Containers",
                "flavor": "You need to see what containers are currently running on the compromised host. What command lists only the running containers?",
                "lesson": (
                    "docker ps — lists currently running containers.\n\n"
                    "Output columns:\n"
                    "  CONTAINER ID  truncated hash uniquely identifying the container\n"
                    "  IMAGE         the image the container was created from\n"
                    "  COMMAND       the process running inside the container\n"
                    "  CREATED       when the container was started\n"
                    "  STATUS        running, exited, paused, etc.\n"
                    "  PORTS         published port mappings\n"
                    "  NAMES         the container's name (random or assigned with --name)\n\n"
                    "Key flags:\n"
                    "  docker ps -a   → show ALL containers, including stopped ones\n"
                    "  docker ps -q   → show only container IDs (useful in scripts)\n"
                    "  docker ps -l   → show the most recently created container"
                ),
                "answer": "ps",
                "hints": [
                    "Think of the Unix command for listing running processes.",
                    "It's a two-letter abbreviation: docker ___",
                    "The answer is: ps",
                ],
            },
            {
                "id": "surf_4",
                "type": "flag_quiz",
                "title": "All Containers, Including Stopped",
                "flavor": "docker ps only shows running containers. The attacker's container was stopped and not yet removed. What flag shows ALL containers, including stopped ones?",
                "lesson": (
                    "docker ps -a — shows all containers, regardless of state.\n\n"
                    "States you'll see:\n"
                    "  Up X minutes/hours  → currently running\n"
                    "  Exited (0) X ago    → stopped cleanly (exit code 0)\n"
                    "  Exited (1) X ago    → stopped with an error\n"
                    "  Created             → created but never started\n"
                    "  Paused              → container process is paused\n\n"
                    "Stopped containers still occupy disk space (their writable layer\n"
                    "is preserved) until you run docker rm. In a forensics context,\n"
                    "this means their filesystem state is still readable — even after\n"
                    "they've been stopped."
                ),
                "answer": "-a",
                "hints": [
                    "It's the flag for 'all'.",
                    "Single letter flag: docker ps ___",
                    "The answer is: -a",
                ],
            },
            {
                "id": "surf_5",
                "type": "quiz",
                "title": "List Local Images",
                "flavor": "Before a container runs, its image must be local. What command lists all images currently stored on the Docker host?",
                "lesson": (
                    "docker images — lists all locally stored images.\n\n"
                    "Output columns:\n"
                    "  REPOSITORY   image name (e.g. nginx, myapp)\n"
                    "  TAG          version label (e.g. latest, 1.25, production)\n"
                    "  IMAGE ID     truncated content hash of the image\n"
                    "  CREATED      when the image was built\n"
                    "  SIZE         uncompressed size of the image on disk\n\n"
                    "Key flags:\n"
                    "  docker images -a   → also show intermediate (layer) images\n"
                    "  docker images -q   → show only image IDs\n\n"
                    "Also available: docker image ls (same output, newer syntax)\n\n"
                    "Dangling images: images with no tag (<none>:<none>). These are\n"
                    "leftover build layers that are no longer referenced."
                ),
                "answer": "images",
                "hints": [
                    "It's the plural of 'image'.",
                    "The command is: docker ___",
                    "The answer is: images",
                ],
            },
            {
                "id": "surf_6",
                "type": "fill_blank",
                "title": "Interactive Shell",
                "flavor": "You need to start an Alpine container and drop into a shell immediately — interactive, with a TTY allocated, and removed when you exit. Complete: docker run ___ alpine sh",
                "lesson": (
                    "docker run --rm -it — runs a container interactively and removes it on exit.\n\n"
                    "Breaking it down:\n"
                    "  --rm    → remove the container filesystem when the container exits\n"
                    "            (no cleanup required; nothing left behind)\n"
                    "  -i      → keep stdin open (interactive mode)\n"
                    "  -t      → allocate a pseudo-TTY (makes it behave like a terminal)\n"
                    "  -it     → shorthand combining -i and -t\n\n"
                    "Common use: quick, ephemeral shells for testing or inspection:\n"
                    "  docker run --rm -it alpine sh\n"
                    "  docker run --rm -it ubuntu bash\n"
                    "  docker run --rm -it python:3.11 python\n\n"
                    "Without --rm, every docker run leaves behind a stopped container.\n"
                    "In investigation contexts, this can be useful — stopped containers\n"
                    "preserve their filesystem state for inspection."
                ),
                "answer": "--rm -it",
                "hints": [
                    "You need three things: remove on exit, interactive, and a TTY.",
                    "Two flags combined: --rm and -it",
                    "The answer is: --rm -it",
                ],
            },
        ],
    },
    "image_vault": {
        "id": "image_vault",
        "name": "The Image Vault",
        "subtitle": "Inspect, History & Layer Analysis",
        "color": "magenta",
        "icon": "📦",
        "commands": ["docker inspect", "docker history", "docker tag", "docker rmi"],
        "challenges": [
            {
                "id": "img_1",
                "type": "quiz",
                "title": "Read the Metadata",
                "flavor": "You need to read the full metadata for a Docker image — exposed ports, environment variables, volumes, entrypoint. What command shows detailed JSON metadata for an image or container?",
                "lesson": (
                    "docker inspect — returns detailed JSON metadata for any Docker object.\n\n"
                    "Works on: images, containers, volumes, networks.\n\n"
                    "For images, inspect shows:\n"
                    "  Id              full content hash\n"
                    "  RepoTags        all tags pointing to this image\n"
                    "  Config.Env      environment variables baked in at build time\n"
                    "  Config.ExposedPorts  ports documented in the Dockerfile\n"
                    "  Config.Volumes  volume mount points defined in the Dockerfile\n"
                    "  Config.Entrypoint / Cmd  the default process\n"
                    "  RootFS.Layers   the layer content hashes\n\n"
                    "Filter with --format to extract specific fields:\n"
                    "  docker inspect --format '{{.Config.Env}}' myimage\n"
                    "  docker inspect --format '{{.Config.ExposedPorts}}' myimage"
                ),
                "answer": "inspect",
                "hints": [
                    "The command means 'look closely at the object'.",
                    "It's one word: docker ___",
                    "The answer is: inspect",
                ],
            },
            {
                "id": "img_2",
                "type": "quiz",
                "title": "Read the Layers",
                "flavor": "The CVE is in an old package installed three years ago. You need to see every build instruction that created each layer — the full layer-by-layer build history of the image. What command shows this?",
                "lesson": (
                    "docker history — shows the build history of an image, layer by layer.\n\n"
                    "Output columns:\n"
                    "  IMAGE     layer ID (or <missing> for intermediate layers not stored locally)\n"
                    "  CREATED   when this layer was created\n"
                    "  CREATED BY  the Dockerfile instruction that created the layer\n"
                    "  SIZE      how much disk space this layer adds\n"
                    "  COMMENT   optional build comment\n\n"
                    "Forensic use:\n"
                    "  Credentials added with RUN and 'removed' with a later RUN are still\n"
                    "  present in the earlier layer — docker history will show the command,\n"
                    "  and the layer content is still accessible if the build cache is intact.\n\n"
                    "  docker history --no-trunc myimage → shows full, untruncated commands"
                ),
                "answer": "history",
                "hints": [
                    "Think about what you want to see: the build history.",
                    "The command is: docker ___",
                    "The answer is: history",
                ],
            },
            {
                "id": "img_3",
                "type": "fill_blank",
                "title": "Tag an Image",
                "flavor": "You need to create a new reference to an existing image — same content, different name. Complete: docker ___ nginx:latest myrepo/nginx:audited",
                "lesson": (
                    "docker tag — creates a new tag (name:version) pointing to an existing image.\n\n"
                    "Syntax: docker tag source[:tag] target[:tag]\n\n"
                    "The image content is NOT copied. Both tags point to the same image ID.\n"
                    "Tags are just human-readable aliases for image content hashes.\n\n"
                    "Common uses:\n"
                    "  Rename before pushing to a registry:\n"
                    "    docker tag myapp:latest registry.example.com/myapp:v1.2\n\n"
                    "  Add a version tag to an existing image:\n"
                    "    docker tag myapp:latest myapp:1.0.0\n\n"
                    "  The attacker's method: re-tag a backdoored image with the same\n"
                    "  name:tag as the legitimate production image, then push it."
                ),
                "answer": "tag",
                "hints": [
                    "You're creating an alias — a new label for the same content.",
                    "The command is: docker ___",
                    "The answer is: tag",
                ],
            },
            {
                "id": "img_4",
                "type": "quiz",
                "title": "Remove an Image",
                "flavor": "You've flagged a compromised image and need to remove it from local storage. What command removes a Docker image?",
                "lesson": (
                    "docker rmi — removes one or more images from local storage.\n\n"
                    "Syntax: docker rmi image[:tag] [image2...]\n\n"
                    "You can specify by tag or by image ID:\n"
                    "  docker rmi nginx:latest\n"
                    "  docker rmi a3f9c21b8de1\n\n"
                    "You cannot remove an image if a container (running or stopped)\n"
                    "is using it. Options:\n"
                    "  docker rmi -f myimage   → force remove (untags even if containers exist)\n"
                    "  docker rm container_id  → remove the container first, then rmi\n\n"
                    "Removing all dangling images:\n"
                    "  docker image prune      → removes only dangling (<none>) images\n"
                    "  docker image prune -a   → removes all unused images"
                ),
                "answer": "rmi",
                "hints": [
                    "It's 'rm' for images — abbreviated.",
                    "Three letters: docker ___",
                    "The answer is: rmi",
                ],
            },
            {
                "id": "img_5",
                "type": "flag_quiz",
                "title": "Full History",
                "flavor": "docker history truncates long commands. What flag shows the full, untruncated output — critical when reading Dockerfile instructions that may contain credentials?",
                "lesson": (
                    "docker history --no-trunc — shows complete, untruncated layer commands.\n\n"
                    "By default, docker history truncates the CREATED BY column at ~80 chars.\n"
                    "This means a RUN instruction like:\n"
                    "  RUN export SECRET=abc123 && configure.sh && unset SECRET\n"
                    "...gets cut off before the credentials are visible.\n\n"
                    "With --no-trunc, the full instruction is shown — including any\n"
                    "credentials, API keys, or configuration values that were passed\n"
                    "as shell commands during the build.\n\n"
                    "Note: RUN commands that set variables and immediately unset them\n"
                    "do NOT prevent the values from being visible in the layer history.\n"
                    "Use build secrets (--secret) or ARG (not ENV) for sensitive values."
                ),
                "answer": "--no-trunc",
                "hints": [
                    "You want to disable truncation.",
                    "The flag is: --no-___",
                    "The answer is: --no-trunc",
                ],
            },
            {
                "id": "img_6",
                "type": "fill_blank",
                "title": "Boss: Image Prune",
                "is_boss": True,
                "title": "Boss: Clean Dangling Images",
                "flavor": "After the audit, you need to remove all dangling images (the <none>:<none> orphans left by failed builds). Complete: docker image ___",
                "lesson": (
                    "docker image prune — removes dangling images.\n\n"
                    "Dangling images: images with no tag, no name — <none>:<none>.\n"
                    "They're created when:\n"
                    "  - A build fails partway through\n"
                    "  - A new build creates a new image with the same tag,\n"
                    "    leaving the old image untagged\n\n"
                    "Flags:\n"
                    "  docker image prune        → removes only dangling images\n"
                    "  docker image prune -a     → removes ALL unused images\n"
                    "                              (any image not used by a container)\n"
                    "  docker image prune -f     → skip confirmation prompt\n\n"
                    "Related:\n"
                    "  docker system prune       → removes containers, networks, images, caches\n"
                    "  docker system prune -a    → nuclear option: removes everything unused"
                ),
                "answer": "prune",
                "hints": [
                    "You want to clean up unused images.",
                    "The subcommand is: docker image ___",
                    "The answer is: prune",
                ],
            },
        ],
    },
    "container_grid": {
        "id": "container_grid",
        "name": "The Container Grid",
        "subtitle": "Exec, Logs, Copy & Lifecycle",
        "color": "green",
        "icon": "⚙️",
        "commands": ["docker exec", "docker logs", "docker cp", "docker stop", "docker rm"],
        "challenges": [
            {
                "id": "cont_1",
                "type": "quiz",
                "title": "Enter a Running Container",
                "flavor": "The attacker used the debug endpoint to execute commands inside the running container. What docker command runs a command inside an already-running container?",
                "lesson": (
                    "docker exec — runs a command inside a running container.\n\n"
                    "Syntax: docker exec [flags] container command [args]\n\n"
                    "Common usage:\n"
                    "  docker exec mycontainer ls /app\n"
                    "  docker exec -it mycontainer bash    → interactive shell\n"
                    "  docker exec -it mycontainer sh      → if bash isn't available\n\n"
                    "Flags:\n"
                    "  -i   → keep stdin open\n"
                    "  -t   → allocate a TTY\n"
                    "  -e KEY=VALUE  → set environment variable for this exec\n"
                    "  -u user       → run as a specific user\n\n"
                    "Key distinction: docker exec runs in an ALREADY RUNNING container.\n"
                    "docker run creates a NEW container from an image.\n"
                    "The attacker used exec — no new container, no new image, no new logs."
                ),
                "answer": "exec",
                "hints": [
                    "Think: execute a command inside something that's already running.",
                    "The command is: docker ___",
                    "The answer is: exec",
                ],
            },
            {
                "id": "cont_2",
                "type": "quiz",
                "title": "Read Container Output",
                "flavor": "The compromised container wrote to stdout for weeks. That output is recoverable. What command shows the stdout/stderr output from a container?",
                "lesson": (
                    "docker logs — retrieves stdout/stderr from a container.\n\n"
                    "Works on running AND stopped containers (until the container is removed).\n\n"
                    "Syntax: docker logs [flags] container\n\n"
                    "Key flags:\n"
                    "  -f, --follow        → stream logs in real time (like tail -f)\n"
                    "  --tail N            → show only the last N lines\n"
                    "  --since TIMESTAMP   → show logs since a specific time\n"
                    "  --until TIMESTAMP   → show logs up to a specific time\n"
                    "  -t, --timestamps    → prefix each line with the timestamp\n\n"
                    "Example (forensic):\n"
                    "  docker logs --since '2024-01-15T03:00:00' --until '2024-01-15T04:00:00' mycontainer\n\n"
                    "Important: logs are only available while the container exists.\n"
                    "docker rm deletes the container and its logs permanently."
                ),
                "answer": "logs",
                "hints": [
                    "You want to read what the container wrote to stdout.",
                    "The command is: docker ___",
                    "The answer is: logs",
                ],
            },
            {
                "id": "cont_3",
                "type": "flag_quiz",
                "title": "Stream Logs Live",
                "flavor": "You need to watch a suspicious container's output in real time. What flag makes docker logs stream continuously, like tail -f?",
                "lesson": (
                    "docker logs -f (or --follow) — streams container output in real time.\n\n"
                    "Without -f: docker logs prints existing output and exits.\n"
                    "With -f: docker logs prints existing output then streams new lines as they appear.\n"
                    "  Ctrl+C exits the log stream without stopping the container.\n\n"
                    "Combine with other flags:\n"
                    "  docker logs -f --tail 100 mycontainer\n"
                    "  → show last 100 lines then stream new output\n\n"
                    "  docker logs -f -t mycontainer\n"
                    "  → stream with timestamps\n\n"
                    "In investigation contexts, -f lets you watch a container react\n"
                    "to inputs in real time — useful for behavioral analysis."
                ),
                "answer": "-f",
                "hints": [
                    "It's the 'follow' flag.",
                    "Single letter: docker logs ___",
                    "The answer is: -f",
                ],
            },
            {
                "id": "cont_4",
                "type": "fill_blank",
                "title": "Copy Evidence Out",
                "flavor": "There's a log file inside the container at /app/audit.log that you need on the host. Complete: docker cp mycontainer:/app/audit.log ___",
                "lesson": (
                    "docker cp — copies files between container and host filesystem.\n\n"
                    "Syntax:\n"
                    "  docker cp container:src_path host_dest_path\n"
                    "  docker cp host_src_path container:dest_path\n\n"
                    "Works on running AND stopped containers.\n\n"
                    "Examples:\n"
                    "  docker cp mycontainer:/app/logs/error.log ./evidence/\n"
                    "  docker cp ./config.json mycontainer:/app/config.json\n\n"
                    "In forensics: docker cp from a stopped container is how you\n"
                    "extract files from a container's writable layer without\n"
                    "starting the container or modifying its state.\n\n"
                    "The container must exist (not removed). Running is not required."
                ),
                "answer": ".",
                "hints": [
                    "You want to copy to the current directory on the host.",
                    "A single character represents 'current directory'.",
                    "The answer is: . (dot)",
                ],
            },
            {
                "id": "cont_5",
                "type": "quiz",
                "title": "Stop a Container",
                "flavor": "You need to stop a running container — gracefully, giving the process time to shut down. What command stops a running container?",
                "lesson": (
                    "docker stop — stops a running container gracefully.\n\n"
                    "Mechanism:\n"
                    "  1. Sends SIGTERM to the main process (PID 1) inside the container.\n"
                    "  2. Waits for the process to exit (default: 10 seconds).\n"
                    "  3. If the process hasn't exited, sends SIGKILL.\n\n"
                    "Flags:\n"
                    "  -t N  → change the timeout (seconds) before SIGKILL\n"
                    "         docker stop -t 30 mycontainer\n\n"
                    "vs docker kill:\n"
                    "  docker kill sends SIGKILL immediately — no graceful shutdown.\n"
                    "  Use docker stop unless the container is unresponsive.\n\n"
                    "The container's filesystem state is preserved after stop.\n"
                    "Use docker rm to delete it, docker start to restart it."
                ),
                "answer": "stop",
                "hints": [
                    "The command means what it says.",
                    "The command is: docker ___",
                    "The answer is: stop",
                ],
            },
            {
                "id": "cont_6",
                "type": "fill_blank",
                "title": "Boss: Interactive Exec",
                "is_boss": True,
                "title": "Boss: Shell Into a Container",
                "flavor": "You need an interactive bash shell inside a running container called 'target'. Complete: docker exec ___ target bash",
                "lesson": (
                    "docker exec -it — opens an interactive terminal session inside a running container.\n\n"
                    "Breakdown:\n"
                    "  -i   → keep stdin open (so you can type commands)\n"
                    "  -t   → allocate a pseudo-TTY (so it behaves like a terminal)\n\n"
                    "Without -it, the command runs and exits without interaction.\n"
                    "With -it, you get a full shell session inside the container.\n\n"
                    "Common patterns:\n"
                    "  docker exec -it mycontainer bash\n"
                    "  docker exec -it mycontainer sh        → if bash isn't installed\n"
                    "  docker exec -it -u root mycontainer bash  → as root\n\n"
                    "This is exactly what the attacker did — exec'd into the container\n"
                    "through the exposed debug endpoint, which accepted exec requests\n"
                    "without authentication."
                ),
                "answer": "-it",
                "hints": [
                    "You need interactive mode AND a TTY.",
                    "Combine -i and -t into one flag.",
                    "The answer is: -it",
                ],
            },
        ],
    },
    "port_matrix": {
        "id": "port_matrix",
        "name": "The Port Matrix",
        "subtitle": "Port Mapping & Network Exposure",
        "color": "yellow",
        "icon": "🔌",
        "commands": ["docker run -p", "docker port", "EXPOSE", "-P"],
        "challenges": [
            {
                "id": "port_1",
                "type": "fill_blank",
                "title": "Map a Port",
                "flavor": "You need to run nginx and make it accessible on host port 8080, forwarding to the container's port 80. Complete: docker run ___ nginx",
                "lesson": (
                    "docker run -p hostPort:containerPort — publishes a container port to the host.\n\n"
                    "Syntax: -p [hostIP:]hostPort:containerPort\n\n"
                    "Examples:\n"
                    "  docker run -p 8080:80 nginx\n"
                    "     → host port 8080 → container port 80\n"
                    "     → accessible via localhost:8080\n\n"
                    "  docker run -p 127.0.0.1:8080:80 nginx\n"
                    "     → only accessible from localhost (not external network)\n\n"
                    "  docker run -p 0.0.0.0:8080:80 nginx\n"
                    "     → explicitly accessible from all network interfaces\n"
                    "     → equivalent to the default (no IP specified)\n\n"
                    "The breach: port 9229 was published without specifying 127.0.0.1,\n"
                    "defaulting to 0.0.0.0 — meaning it was reachable from the internet."
                ),
                "answer": "-p 8080:80",
                "hints": [
                    "The flag is -p, followed by hostPort:containerPort.",
                    "Host port first, container port second, colon between them.",
                    "The answer is: -p 8080:80",
                ],
            },
            {
                "id": "port_2",
                "type": "quiz",
                "title": "What Does EXPOSE Do?",
                "flavor": "The Dockerfile had EXPOSE 9229. A junior developer thought this meant the port was secured behind Docker's internal network. What does EXPOSE actually do?",
                "lesson": (
                    "EXPOSE — documents which ports a container intends to use. Nothing more.\n\n"
                    "EXPOSE does NOT:\n"
                    "  - publish the port to the host\n"
                    "  - make the port accessible from outside the container\n"
                    "  - configure any firewall rules\n"
                    "  - provide any security\n\n"
                    "EXPOSE DOES:\n"
                    "  - document the port in the image metadata (visible in docker inspect)\n"
                    "  - enable the -P flag (publish all exposed ports to random host ports)\n"
                    "  - serve as communication between image author and operator\n\n"
                    "To actually publish a port: use -p when running the container.\n\n"
                    "Common misconception: 'I added EXPOSE so the port is available.'\n"
                    "Reality: EXPOSE is a comment. -p is the action."
                ),
                "answer": "documents",
                "hints": [
                    "EXPOSE is informational only — it tells you something, but doesn't do something.",
                    "Think: it _______ the port. It doesn't open or secure it.",
                    "The answer is: documents (it documents/declares the port)",
                ],
            },
            {
                "id": "port_3",
                "type": "quiz",
                "title": "Show Port Mappings",
                "flavor": "You need to quickly see which host ports are mapped to which container ports for a running container. What command shows this?",
                "lesson": (
                    "docker port — shows port mappings for a specific container.\n\n"
                    "Syntax:\n"
                    "  docker port container            → show all port mappings\n"
                    "  docker port container 80         → show what host port maps to container port 80\n"
                    "  docker port container 80/tcp     → specify protocol\n\n"
                    "Example output:\n"
                    "  80/tcp -> 0.0.0.0:8080\n"
                    "  9229/tcp -> 0.0.0.0:9229\n\n"
                    "This is how you confirm what's actually published — not what EXPOSE\n"
                    "declares, but what -p has made real. The 0.0.0.0 binding on port 9229\n"
                    "is visible immediately."
                ),
                "answer": "port",
                "hints": [
                    "The command is named after what it shows.",
                    "docker ___  mycontainer",
                    "The answer is: port",
                ],
            },
            {
                "id": "port_4",
                "type": "flag_quiz",
                "title": "Publish All Exposed Ports",
                "flavor": "What single flag tells docker run to automatically publish all EXPOSE'd ports to random host ports?",
                "lesson": (
                    "docker run -P — publishes all EXPOSE'd ports to random ephemeral host ports.\n\n"
                    "Lowercase -p: you specify the mapping (host:container)\n"
                    "Uppercase -P: Docker picks the host ports automatically\n\n"
                    "Example:\n"
                    "  Dockerfile has: EXPOSE 80 443\n"
                    "  docker run -P myimage\n"
                    "  → 80/tcp → 0.0.0.0:32768\n"
                    "  → 443/tcp → 0.0.0.0:32769\n\n"
                    "Use docker port to find out which host ports were assigned.\n\n"
                    "Warning: -P binds to 0.0.0.0 (all interfaces) by default.\n"
                    "This means all published ports are externally accessible unless\n"
                    "you have an external firewall blocking them."
                ),
                "answer": "-P",
                "hints": [
                    "It's the uppercase version of -p.",
                    "A single uppercase letter flag.",
                    "The answer is: -P",
                ],
            },
            {
                "id": "port_5",
                "type": "fill_blank",
                "title": "Boss: Localhost Only",
                "is_boss": True,
                "title": "Boss: Bind to Localhost Only",
                "flavor": "You need to publish port 9229 but ONLY on localhost — not exposed to the network. Complete: docker run -p ___:9229 myapp",
                "lesson": (
                    "Binding to 127.0.0.1 restricts a published port to localhost only.\n\n"
                    "Syntax: docker run -p [bindIP:]hostPort:containerPort\n\n"
                    "  -p 9229:9229              → binds to 0.0.0.0 (all interfaces, including public)\n"
                    "  -p 127.0.0.1:9229:9229    → binds to localhost only (not externally accessible)\n\n"
                    "This is the correct way to expose debugging or admin ports:\n"
                    "bind to 127.0.0.1 so only processes on the same host can connect.\n\n"
                    "The fix for the breach:\n"
                    "  Change: -p 9229:9229\n"
                    "  To:     -p 127.0.0.1:9229:9229\n"
                    "  Or better: remove the port mapping entirely from production."
                ),
                "answer": "127.0.0.1:9229",
                "hints": [
                    "You need to specify localhost explicitly as the bind address.",
                    "Format: bindIP:hostPort — use the loopback address.",
                    "The answer is: 127.0.0.1:9229",
                ],
            },
        ],
    },
    "volume_sanctum": {
        "id": "volume_sanctum",
        "name": "The Volume Sanctum",
        "subtitle": "Volumes, Bind Mounts & Data Persistence",
        "color": "blue",
        "icon": "💾",
        "commands": ["docker volume", "-v", "--mount", "bind mounts"],
        "challenges": [
            {
                "id": "vol_1",
                "type": "quiz",
                "title": "Create a Named Volume",
                "flavor": "You need to create a named Docker volume to store persistent data independent of any container lifecycle. What command creates a named volume?",
                "lesson": (
                    "docker volume create — creates a named volume.\n\n"
                    "Syntax: docker volume create [name]\n\n"
                    "Named volumes vs bind mounts:\n"
                    "  Named volume: managed by Docker, stored in Docker's storage area\n"
                    "                (/var/lib/docker/volumes/ on Linux)\n"
                    "                portable, works on Docker Desktop across platforms\n\n"
                    "  Bind mount: maps a specific host filesystem path into the container\n"
                    "              depends on host filesystem structure\n"
                    "              more control, more risk\n\n"
                    "You can also create volumes implicitly:\n"
                    "  docker run -v mydata:/app/data myimage\n"
                    "  → creates 'mydata' volume automatically if it doesn't exist"
                ),
                "answer": "create",
                "hints": [
                    "The subcommand follows 'docker volume'.",
                    "docker volume ___  myvolume",
                    "The answer is: create",
                ],
            },
            {
                "id": "vol_2",
                "type": "fill_blank",
                "title": "Mount a Named Volume",
                "flavor": "Run an nginx container and mount the named volume 'webdata' to /usr/share/nginx/html inside the container. Complete: docker run ___ nginx",
                "lesson": (
                    "Mount a named volume with -v name:containerPath\n\n"
                    "Syntax: -v volumeName:containerPath[:options]\n\n"
                    "  docker run -v webdata:/usr/share/nginx/html nginx\n\n"
                    "Options (append after a second colon):\n"
                    "  :ro   → read-only mount\n"
                    "  :rw   → read-write (default)\n\n"
                    "Example:\n"
                    "  docker run -v webdata:/usr/share/nginx/html:ro nginx\n"
                    "  → nginx can read files but not modify them\n\n"
                    "Named volumes persist when the container is removed.\n"
                    "Running a new container with the same volume name reattaches\n"
                    "to the same data — this is how you persist databases, uploads, etc."
                ),
                "answer": "-v webdata:/usr/share/nginx/html",
                "hints": [
                    "The -v flag takes volumeName:containerPath format.",
                    "Named volume first, then colon, then the path inside the container.",
                    "The answer is: -v webdata:/usr/share/nginx/html",
                ],
            },
            {
                "id": "vol_3",
                "type": "fill_blank",
                "title": "The Dangerous Bind Mount",
                "flavor": "This is the misconfiguration that enabled the breach. What -v argument mounts the host root filesystem to /host inside a container (read-write)?",
                "lesson": (
                    "Bind mount syntax: -v /host/path:/container/path\n\n"
                    "  -v /:/host   → mounts the entire host root filesystem into the container\n"
                    "                 at /host, with full read-write access\n\n"
                    "This is catastrophic:\n"
                    "  - The container can read any file on the host\n"
                    "  - The container can write to any file on the host\n"
                    "  - From inside the container: chroot /host gives full host access\n"
                    "  - Credentials, SSH keys, /etc/shadow — all accessible\n\n"
                    "Safer alternatives:\n"
                    "  -v /specific/path:/container/path   → only mount what's needed\n"
                    "  -v /path:/container/path:ro         → read-only if writes aren't needed\n\n"
                    "Named volumes are safer than bind mounts for most use cases.\n"
                    "Bind mounts are only appropriate when you specifically need host filesystem access."
                ),
                "answer": "-v /:/host",
                "hints": [
                    "The host path is / (root), the container path is /host.",
                    "Format: -v hostPath:containerPath",
                    "The answer is: -v /:/host",
                ],
            },
            {
                "id": "vol_4",
                "type": "quiz",
                "title": "List Volumes",
                "flavor": "You need to see all named volumes on the Docker host — including volumes from decommissioned containers that were never cleaned up. What command lists volumes?",
                "lesson": (
                    "docker volume ls — lists all named volumes on the host.\n\n"
                    "Output columns:\n"
                    "  DRIVER   the volume driver (local for standard volumes)\n"
                    "  VOLUME NAME  the name you gave it (or a hash if unnamed)\n\n"
                    "Flags:\n"
                    "  docker volume ls -q   → show only volume names\n"
                    "  docker volume ls -f dangling=true  → show unused volumes\n\n"
                    "Orphaned volumes: volumes not connected to any container.\n"
                    "They accumulate when containers are removed but volumes aren't.\n"
                    "They can contain sensitive data from decommissioned services.\n\n"
                    "Clean up with:\n"
                    "  docker volume prune     → remove all unused (dangling) volumes\n"
                    "  docker volume rm name   → remove a specific volume"
                ),
                "answer": "ls",
                "hints": [
                    "The standard Unix abbreviation for 'list'.",
                    "docker volume ___",
                    "The answer is: ls",
                ],
            },
            {
                "id": "vol_5",
                "type": "fill_blank",
                "title": "Boss: Inspect a Volume",
                "is_boss": True,
                "title": "Boss: Read Volume Metadata",
                "flavor": "You need to see where on the host filesystem the volume 'appdata' is actually stored. Complete: docker volume ___ appdata",
                "lesson": (
                    "docker volume inspect — shows detailed metadata about a named volume.\n\n"
                    "Output includes:\n"
                    "  Name        the volume name\n"
                    "  Driver      the storage driver\n"
                    "  Mountpoint  the actual host filesystem path\n"
                    "              (e.g. /var/lib/docker/volumes/appdata/_data)\n"
                    "  Labels      any labels applied at creation\n"
                    "  CreatedAt   when the volume was created\n\n"
                    "The Mountpoint is where the data physically lives on the host.\n"
                    "With root access to the host, you can read this path directly.\n\n"
                    "Forensic use: if a container is removed but the volume still exists,\n"
                    "reading the Mountpoint gives you direct access to the volume contents\n"
                    "without needing to start a new container."
                ),
                "answer": "inspect",
                "hints": [
                    "Same command used for images and containers — shows detailed metadata.",
                    "docker volume ___",
                    "The answer is: inspect",
                ],
            },
        ],
    },
    "network_forge": {
        "id": "network_forge",
        "name": "The Network Forge",
        "subtitle": "Docker Networking & Segmentation",
        "color": "red",
        "icon": "🌐",
        "commands": ["docker network", "bridge", "custom networks", "DNS"],
        "challenges": [
            {
                "id": "net_1",
                "type": "quiz",
                "title": "List Networks",
                "flavor": "You need to see every Docker network on the host — the default bridge, the host network, and any custom networks. What command lists all Docker networks?",
                "lesson": (
                    "docker network ls — lists all Docker networks.\n\n"
                    "Default networks (always present):\n"
                    "  bridge   → the default network; containers connect here if unspecified\n"
                    "  host     → removes network isolation; container uses host's network directly\n"
                    "  none     → no network access; fully isolated\n\n"
                    "Output columns:\n"
                    "  NETWORK ID  unique ID\n"
                    "  NAME        network name\n"
                    "  DRIVER      bridge, host, overlay, macvlan, none\n"
                    "  SCOPE       local or swarm\n\n"
                    "Custom networks appear in this list alongside the defaults."
                ),
                "answer": "ls",
                "hints": [
                    "Standard Unix 'list' abbreviation.",
                    "docker network ___",
                    "The answer is: ls",
                ],
            },
            {
                "id": "net_2",
                "type": "quiz",
                "title": "Default Network Driver",
                "flavor": "When you run a container without specifying a network, Docker connects it to a network using the default driver. What is the name of this default network driver?",
                "lesson": (
                    "bridge — the default Docker network driver.\n\n"
                    "The default bridge network:\n"
                    "  - All containers join it if no --network flag is specified\n"
                    "  - Containers can communicate with each other by IP address\n"
                    "  - BUT: on the default bridge, containers cannot reach each other\n"
                    "    by name (only IP) — DNS resolution doesn't work on the default bridge\n\n"
                    "Custom bridge networks (created with docker network create):\n"
                    "  - Containers CAN reach each other by name (automatic DNS)\n"
                    "  - Better network isolation between unrelated services\n"
                    "  - The recommended approach for multi-container applications\n\n"
                    "The breach: all services were on the default bridge.\n"
                    "The compromised container reached the payment service by IP.\n"
                    "They'd been on the same flat network for eighteen months."
                ),
                "answer": "bridge",
                "hints": [
                    "Think about what connects two separate networks — a physical ___.",
                    "It's the same name as the networking concept it implements.",
                    "The answer is: bridge",
                ],
            },
            {
                "id": "net_3",
                "type": "fill_blank",
                "title": "Create a Custom Network",
                "flavor": "You need to create a custom bridge network called 'backend' to isolate internal services. Complete: docker network ___ backend",
                "lesson": (
                    "docker network create — creates a custom Docker network.\n\n"
                    "Syntax: docker network create [flags] name\n\n"
                    "Default driver is bridge:\n"
                    "  docker network create backend\n"
                    "  → creates a custom bridge network named 'backend'\n\n"
                    "Specify the driver explicitly:\n"
                    "  docker network create --driver bridge backend\n\n"
                    "Custom bridge networks provide:\n"
                    "  - Automatic DNS: containers find each other by name\n"
                    "  - Isolation: containers on different networks can't communicate\n"
                    "    without explicit connection\n"
                    "  - Better security posture than the default bridge\n\n"
                    "Best practice: create separate networks for separate concerns\n"
                    "  (e.g., 'frontend' network for web services, 'backend' for databases)"
                ),
                "answer": "create",
                "hints": [
                    "The subcommand for making a new network.",
                    "docker network ___  backend",
                    "The answer is: create",
                ],
            },
            {
                "id": "net_4",
                "type": "fill_blank",
                "title": "Connect a Container",
                "flavor": "A running container named 'app' needs to be added to the 'backend' network. Complete: docker network ___ backend app",
                "lesson": (
                    "docker network connect — connects a running container to a network.\n\n"
                    "Syntax: docker network connect network container\n\n"
                    "  docker network connect backend app\n"
                    "  → container 'app' can now communicate with other containers on 'backend'\n\n"
                    "A container can be on multiple networks simultaneously.\n"
                    "This is how you connect services that span network boundaries:\n"
                    "  a web container on both 'frontend' and 'backend' networks\n"
                    "  can relay traffic between the two isolated segments.\n\n"
                    "Opposite:\n"
                    "  docker network disconnect backend app\n"
                    "  → removes the container from the network\n\n"
                    "At run time, specify the network directly:\n"
                    "  docker run --network backend myimage"
                ),
                "answer": "connect",
                "hints": [
                    "The subcommand adds a container to a network.",
                    "docker network ___",
                    "The answer is: connect",
                ],
            },
            {
                "id": "net_5",
                "type": "fill_blank",
                "title": "Boss: Inspect a Network",
                "is_boss": True,
                "title": "Boss: Audit Network Membership",
                "flavor": "You need to see every container connected to the default bridge network — the full picture of what could communicate with what. Complete: docker network ___ bridge",
                "lesson": (
                    "docker network inspect — shows detailed JSON metadata for a network.\n\n"
                    "Critical for forensics — the Containers section lists:\n"
                    "  every container currently connected to the network\n"
                    "  their names, IPv4 addresses, and MAC addresses\n\n"
                    "Example:\n"
                    "  docker network inspect bridge\n"
                    "  → shows all containers on the default bridge network\n"
                    "  → their IPs\n"
                    "  → proof that the compromised container could reach the payment service\n\n"
                    "Also shows:\n"
                    "  Subnet and gateway configuration\n"
                    "  Network options and labels\n"
                    "  IPAM configuration\n\n"
                    "Use --format to extract specific fields:\n"
                    "  docker network inspect --format '{{range .Containers}}{{.Name}} {{end}}' bridge\n"
                    "  → print just the container names on the bridge network"
                ),
                "answer": "inspect",
                "hints": [
                    "Same command used for images, containers, and volumes.",
                    "docker network ___  bridge",
                    "The answer is: inspect",
                ],
            },
        ],
    },
    "build_engine": {
        "id": "build_engine",
        "name": "The Build Engine",
        "subtitle": "Dockerfiles & Image Construction",
        "color": "magenta",
        "icon": "🔧",
        "commands": ["FROM", "RUN", "COPY", "WORKDIR", "USER", "CMD", "docker build"],
        "challenges": [
            {
                "id": "build_1",
                "type": "quiz",
                "title": "Set the Base Image",
                "flavor": "Every Dockerfile starts with a foundation. What Dockerfile instruction sets the base image for the build?",
                "lesson": (
                    "FROM — sets the base image for a Dockerfile.\n\n"
                    "Syntax: FROM image[:tag] [AS name]\n\n"
                    "Must be the first instruction in a Dockerfile (comments allowed before).\n\n"
                    "Examples:\n"
                    "  FROM ubuntu:22.04\n"
                    "  FROM python:3.11-slim\n"
                    "  FROM node:18-alpine\n"
                    "  FROM scratch           → empty base image; for statically compiled binaries\n\n"
                    "Best practices:\n"
                    "  - Use specific tags (FROM python:3.11), not 'latest'\n"
                    "    'latest' changes over time — your build is no longer reproducible\n"
                    "  - Use minimal base images (alpine, slim variants) to reduce attack surface\n"
                    "  - The breach involved FROM node:latest — the base image changed\n"
                    "    three times in four years without the team noticing"
                ),
                "answer": "FROM",
                "hints": [
                    "The first word of every Dockerfile — where you're building FROM.",
                    "All caps, one word.",
                    "The answer is: FROM",
                ],
            },
            {
                "id": "build_2",
                "type": "quiz",
                "title": "Run a Build Command",
                "flavor": "You need to add a Dockerfile instruction that executes a shell command during the build — installing packages, for example. What instruction does this?",
                "lesson": (
                    "RUN — executes a command during the image build, creating a new layer.\n\n"
                    "Two forms:\n"
                    "  Shell form:  RUN command arg1 arg2\n"
                    "               (runs in a shell: /bin/sh -c on Linux)\n"
                    "  Exec form:   RUN [\"command\", \"arg1\", \"arg2\"]\n"
                    "               (no shell; more predictable for scripts)\n\n"
                    "Common uses:\n"
                    "  RUN apt-get update && apt-get install -y curl\n"
                    "  RUN pip install -r requirements.txt\n"
                    "  RUN npm install\n\n"
                    "Each RUN creates a new layer. Combining commands reduces layer count:\n"
                    "  RUN apt-get update && \\\n"
                    "      apt-get install -y curl git && \\\n"
                    "      rm -rf /var/lib/apt/lists/*\n\n"
                    "CRITICAL: credentials passed as RUN arguments are permanently visible\n"
                    "in docker history — even if a later RUN deletes them."
                ),
                "answer": "RUN",
                "hints": [
                    "The instruction that RUNs a command during the build.",
                    "Three uppercase letters.",
                    "The answer is: RUN",
                ],
            },
            {
                "id": "build_3",
                "type": "quiz",
                "title": "Copy Files Into the Image",
                "flavor": "You need to add application files from the build context into the image. What Dockerfile instruction copies files from the host into the image?",
                "lesson": (
                    "COPY — copies files from the build context into the image.\n\n"
                    "Syntax: COPY [--chown=user:group] src... dest\n\n"
                    "Examples:\n"
                    "  COPY app.py /app/app.py\n"
                    "  COPY requirements.txt .\n"
                    "  COPY . /app/                → copies everything in build context\n"
                    "  COPY --chown=node:node . /app/\n\n"
                    "COPY vs ADD:\n"
                    "  COPY  → simple file copy; use this in almost all cases\n"
                    "  ADD   → COPY + auto-extracts tar files + can fetch URLs\n"
                    "          rarely needed; surprising behavior is a security risk\n\n"
                    ".dockerignore:\n"
                    "  Like .gitignore — excludes files from the build context.\n"
                    "  Always use it to prevent COPY . from including .env files,\n"
                    "  credentials, or large directories."
                ),
                "answer": "COPY",
                "hints": [
                    "The instruction COPYs files.",
                    "Four uppercase letters.",
                    "The answer is: COPY",
                ],
            },
            {
                "id": "build_4",
                "type": "quiz",
                "title": "Set Working Directory",
                "flavor": "You need to set the working directory for subsequent RUN, CMD, COPY, and ENTRYPOINT instructions. What Dockerfile instruction does this?",
                "lesson": (
                    "WORKDIR — sets the working directory for subsequent instructions.\n\n"
                    "Syntax: WORKDIR /path\n\n"
                    "  WORKDIR /app\n"
                    "  COPY . .\n"
                    "  RUN npm install\n"
                    "  → all three operate within /app\n\n"
                    "WORKDIR creates the directory if it doesn't exist.\n"
                    "You can use it multiple times — each WORKDIR is relative to the last.\n\n"
                    "Avoid using RUN cd /path instead of WORKDIR:\n"
                    "  cd only applies within a single RUN command.\n"
                    "  The next RUN starts from the previous WORKDIR, not where cd left you.\n\n"
                    "Best practice: set WORKDIR early and keep it consistent throughout."
                ),
                "answer": "WORKDIR",
                "hints": [
                    "Think: WORK + DIR",
                    "Seven uppercase letters.",
                    "The answer is: WORKDIR",
                ],
            },
            {
                "id": "build_5",
                "type": "quiz",
                "title": "The Security Risk: USER root",
                "flavor": "The compromised Dockerfile ran everything as root. What Dockerfile instruction sets the user that RUN, CMD, and ENTRYPOINT commands execute as?",
                "lesson": (
                    "USER — sets the user for subsequent RUN, CMD, and ENTRYPOINT instructions.\n\n"
                    "Syntax: USER username[:group]\n\n"
                    "Default: if USER is not specified, the container runs as root.\n\n"
                    "Running as root inside a container is a significant security risk:\n"
                    "  - If the container is compromised, the attacker has root in the container\n"
                    "  - Combined with a root filesystem bind mount, they have root on the host\n"
                    "  - This is exactly the attack chain in the breach\n\n"
                    "Best practice:\n"
                    "  RUN groupadd -r appuser && useradd -r -g appuser appuser\n"
                    "  USER appuser\n"
                    "  → subsequent commands run as a non-privileged user\n\n"
                    "Many base images provide a non-root user:\n"
                    "  node image has USER node\n"
                    "  nginx image has USER nginx"
                ),
                "answer": "USER",
                "hints": [
                    "The instruction that sets the USER.",
                    "Four uppercase letters.",
                    "The answer is: USER",
                ],
            },
            {
                "id": "build_6",
                "type": "fill_blank",
                "title": "Boss: Build With a Tag",
                "is_boss": True,
                "title": "Boss: Build the Image",
                "flavor": "Build a Docker image from the Dockerfile in the current directory, tagging it as 'myapp:v2'. Complete: docker build ___ .",
                "lesson": (
                    "docker build -t name:tag . — builds an image from a Dockerfile.\n\n"
                    "Syntax: docker build [flags] PATH\n\n"
                    "  PATH: the build context — directory containing Dockerfile and files\n"
                    "  .    → use the current directory as the build context\n\n"
                    "Key flags:\n"
                    "  -t name:tag    → tag the resulting image\n"
                    "  -f Dockerfile  → specify a different Dockerfile path\n"
                    "  --no-cache     → rebuild all layers, ignoring cached versions\n"
                    "  --build-arg KEY=VALUE  → pass build-time variables\n\n"
                    "Examples:\n"
                    "  docker build -t myapp:v2 .\n"
                    "  docker build -t myapp:latest -f Dockerfile.prod .\n"
                    "  docker build --no-cache -t myapp:clean .\n\n"
                    "The attacker's push: they built a backdoored image, tagged it with\n"
                    "the same tag as the production service, and pushed it to the registry."
                ),
                "answer": "-t myapp:v2",
                "hints": [
                    "The flag for tagging is -t, followed by name:tag.",
                    "Format: docker build -t name:tag .",
                    "The answer is: -t myapp:v2",
                ],
            },
        ],
    },
    "compose_matrix": {
        "id": "compose_matrix",
        "name": "The Compose Matrix",
        "subtitle": "Docker Compose & Multi-Container Stacks",
        "color": "cyan",
        "icon": "🎼",
        "commands": ["docker compose up", "docker compose down", "docker compose logs", "docker compose exec"],
        "challenges": [
            {
                "id": "comp_1",
                "type": "fill_blank",
                "title": "Start the Stack",
                "flavor": "You need to start all services defined in docker-compose.yml. Complete: docker compose ___",
                "lesson": (
                    "docker compose up — starts all services defined in docker-compose.yml.\n\n"
                    "Behavior:\n"
                    "  - Builds images if they don't exist\n"
                    "  - Creates networks defined in the compose file\n"
                    "  - Creates volumes defined in the compose file\n"
                    "  - Starts containers in dependency order (based on depends_on)\n"
                    "  - By default, streams logs from all services to the terminal\n\n"
                    "Key flags:\n"
                    "  -d         → detached mode (background)\n"
                    "  --build    → rebuild images even if they already exist\n"
                    "  --force-recreate  → recreate containers even if config hasn't changed\n\n"
                    "The override file:\n"
                    "  docker compose up reads docker-compose.yml AND\n"
                    "  docker-compose.override.yml automatically, merging both.\n"
                    "  There is no flag to disable this — it's always applied if present."
                ),
                "answer": "up",
                "hints": [
                    "The opposite of 'down'.",
                    "docker compose ___",
                    "The answer is: up",
                ],
            },
            {
                "id": "comp_2",
                "type": "fill_blank",
                "title": "Start Detached",
                "flavor": "You need to start the compose stack in the background. Complete: docker compose up ___",
                "lesson": (
                    "docker compose up -d — starts services in detached (background) mode.\n\n"
                    "Without -d: compose streams all service logs to your terminal.\n"
                    "  Ctrl+C stops all services.\n\n"
                    "With -d: compose starts services as background processes.\n"
                    "  Returns to the prompt immediately.\n"
                    "  Use docker compose logs to view output later.\n\n"
                    "Check what's running:\n"
                    "  docker compose ps\n\n"
                    "Stop without removing:\n"
                    "  docker compose stop\n\n"
                    "Stop and remove containers, networks (but not volumes):\n"
                    "  docker compose down\n\n"
                    "Stop and remove everything including volumes:\n"
                    "  docker compose down -v"
                ),
                "answer": "-d",
                "hints": [
                    "Same flag as docker run for detached mode.",
                    "A single letter flag.",
                    "The answer is: -d",
                ],
            },
            {
                "id": "comp_3",
                "type": "fill_blank",
                "title": "Tear Down the Stack",
                "flavor": "You need to stop and remove all containers and networks for this compose stack. Complete: docker compose ___",
                "lesson": (
                    "docker compose down — stops and removes containers and networks.\n\n"
                    "Specifically removes:\n"
                    "  - Containers created by 'docker compose up'\n"
                    "  - Networks defined in the compose file\n\n"
                    "Does NOT remove by default:\n"
                    "  - Named volumes\n"
                    "  - Images\n\n"
                    "Flags:\n"
                    "  -v         → also remove named volumes\n"
                    "  --rmi all  → also remove images used by services\n"
                    "  -t N       → timeout before killing containers\n\n"
                    "vs docker compose stop:\n"
                    "  docker compose stop → stops containers but leaves them\n"
                    "  docker compose down → stops AND removes containers and networks"
                ),
                "answer": "down",
                "hints": [
                    "The opposite of 'up'.",
                    "docker compose ___",
                    "The answer is: down",
                ],
            },
            {
                "id": "comp_4",
                "type": "quiz",
                "title": "View Compose Logs",
                "flavor": "You need to see the aggregated output from all services in the compose stack — every service's logs, combined and labeled. What subcommand shows compose logs?",
                "lesson": (
                    "docker compose logs — shows output from all compose services.\n\n"
                    "Features:\n"
                    "  - Each log line is prefixed with the service name\n"
                    "  - Aggregates stdout/stderr from all running services\n"
                    "  - Works whether the stack is running in detached mode or not\n\n"
                    "Key flags:\n"
                    "  -f          → follow (stream) log output\n"
                    "  --tail N    → show only last N lines per service\n"
                    "  --since TIME → show logs since a timestamp\n\n"
                    "Target a specific service:\n"
                    "  docker compose logs web       → logs from 'web' service only\n"
                    "  docker compose logs -f db     → follow database logs\n\n"
                    "The override file: its effect shows up here — extra ports,\n"
                    "extra environment variables, extra services all appear in the output."
                ),
                "answer": "logs",
                "hints": [
                    "The same word you use with docker logs.",
                    "docker compose ___",
                    "The answer is: logs",
                ],
            },
            {
                "id": "comp_5",
                "type": "fill_blank",
                "title": "Boss: Exec Into a Service",
                "is_boss": True,
                "title": "Boss: Shell Into a Compose Service",
                "flavor": "You need an interactive shell inside the 'web' service defined in your compose file. Complete: docker compose ___ -it web sh",
                "lesson": (
                    "docker compose exec — runs a command inside a running compose service.\n\n"
                    "Syntax: docker compose exec [flags] service command\n\n"
                    "  docker compose exec -it web sh\n"
                    "  → interactive shell inside the 'web' service container\n\n"
                    "vs docker exec:\n"
                    "  docker exec requires the container name or ID\n"
                    "  docker compose exec uses the service name from compose.yml\n"
                    "  (Docker resolves the actual container automatically)\n\n"
                    "Key flags:\n"
                    "  -it   → interactive with TTY\n"
                    "  -e KEY=VALUE  → set environment variable\n"
                    "  -u user       → run as a specific user\n"
                    "  --index N     → if service is scaled, target the Nth instance\n\n"
                    "This is how you investigate a running compose service without\n"
                    "knowing its generated container name."
                ),
                "answer": "exec",
                "hints": [
                    "Same concept as docker exec, but using the service name.",
                    "docker compose ___  -it web sh",
                    "The answer is: exec",
                ],
            },
        ],
    },
    "registry_core": {
        "id": "registry_core",
        "name": "The Registry Core",
        "subtitle": "Registries, System Audit & The Full Picture",
        "color": "yellow",
        "icon": "🏛️",
        "commands": ["docker push", "docker login", "docker system df", "docker system prune"],
        "challenges": [
            {
                "id": "reg_1",
                "type": "quiz",
                "title": "Push to a Registry",
                "flavor": "The attacker uploaded the backdoored image to the registry. What command pushes a local image to a remote registry?",
                "lesson": (
                    "docker push — uploads a local image to a remote registry.\n\n"
                    "Syntax: docker push name[:tag]\n\n"
                    "The image name must match the registry path:\n"
                    "  docker push docker.io/myuser/myapp:latest     → Docker Hub\n"
                    "  docker push ghcr.io/myorg/myapp:v1.0          → GitHub Container Registry\n"
                    "  docker push registry.example.com/myapp:prod   → private registry\n\n"
                    "What push does:\n"
                    "  1. Authenticates with the registry (using stored credentials)\n"
                    "  2. Uploads each layer that isn't already in the registry\n"
                    "  3. Updates the tag in the registry manifest\n\n"
                    "The attack: the attacker pushed a backdoored image with the same\n"
                    "name:tag as the legitimate production image. The registry replaced\n"
                    "the old manifest. The CI/CD pipeline pulled and deployed automatically."
                ),
                "answer": "push",
                "hints": [
                    "The opposite of pull.",
                    "docker ___",
                    "The answer is: push",
                ],
            },
            {
                "id": "reg_2",
                "type": "quiz",
                "title": "Authenticate to a Registry",
                "flavor": "Before pushing to a private registry, you need to authenticate. What command logs in to a Docker registry?",
                "lesson": (
                    "docker login — authenticates to a Docker registry.\n\n"
                    "Syntax: docker login [registry]\n\n"
                    "  docker login              → log in to Docker Hub (default)\n"
                    "  docker login ghcr.io      → log in to GitHub Container Registry\n"
                    "  docker login registry.example.com  → private registry\n\n"
                    "Credentials are stored in:\n"
                    "  ~/.docker/config.json\n"
                    "  (or in a credential helper, if configured)\n\n"
                    "The attacker had valid registry credentials — either stolen or\n"
                    "obtained through the exec session in the compromised container,\n"
                    "where the CI credentials were stored in an environment variable.\n\n"
                    "docker logout — removes stored credentials for a registry."
                ),
                "answer": "login",
                "hints": [
                    "Think: log + in",
                    "docker ___",
                    "The answer is: login",
                ],
            },
            {
                "id": "reg_3",
                "type": "quiz",
                "title": "Audit Disk Usage",
                "flavor": "After the investigation, you need to report on how much disk space the Docker environment is using — images, containers, volumes, build cache. What command shows Docker disk usage?",
                "lesson": (
                    "docker system df — shows Docker disk usage, broken down by type.\n\n"
                    "Output sections:\n"
                    "  Images       total size of all images vs reclaimable (unused)\n"
                    "  Containers   disk used by container writable layers\n"
                    "  Local Volumes  disk used by named volumes\n"
                    "  Build Cache  disk used by the build layer cache\n\n"
                    "Flags:\n"
                    "  docker system df -v    → verbose, shows individual items in each category\n\n"
                    "Forensic use:\n"
                    "  Unexpected image sizes, volumes from unknown services, a build cache\n"
                    "  larger than expected — all visible here. The reclaimable column shows\n"
                    "  how much can be freed with docker system prune."
                ),
                "answer": "df",
                "hints": [
                    "Same abbreviation as the Unix disk filesystem command.",
                    "docker system ___",
                    "The answer is: df",
                ],
            },
            {
                "id": "reg_4",
                "type": "quiz",
                "title": "Real-Time Container Stats",
                "flavor": "You need to monitor CPU, memory, and network usage for all running containers in real time. What command shows live container resource statistics?",
                "lesson": (
                    "docker stats — shows live resource usage for running containers.\n\n"
                    "Output columns:\n"
                    "  CONTAINER ID  container identifier\n"
                    "  NAME          container name\n"
                    "  CPU %         current CPU usage percentage\n"
                    "  MEM USAGE / LIMIT  memory used vs memory limit\n"
                    "  MEM %         memory usage percentage\n"
                    "  NET I/O       network traffic in/out\n"
                    "  BLOCK I/O     disk reads/writes\n"
                    "  PIDS          number of processes\n\n"
                    "Updates every second by default (like top for containers).\n\n"
                    "Flags:\n"
                    "  --no-stream   → print one snapshot and exit\n"
                    "  --format      → customize output\n\n"
                    "  docker stats --no-stream   → useful in scripts and reports"
                ),
                "answer": "stats",
                "hints": [
                    "Short for statistics.",
                    "docker ___",
                    "The answer is: stats",
                ],
            },
            {
                "id": "reg_5",
                "type": "fill_blank",
                "title": "Boss: Full System Cleanup",
                "is_boss": True,
                "title": "Boss: Purge the Environment",
                "flavor": "After the investigation is complete, you need to remove ALL unused Docker resources — stopped containers, dangling images, unused networks, and build cache. Complete: docker system ___",
                "lesson": (
                    "docker system prune — removes all unused Docker resources.\n\n"
                    "By default removes:\n"
                    "  - All stopped containers\n"
                    "  - All unused networks\n"
                    "  - All dangling images (<none>:<none>)\n"
                    "  - All build cache\n\n"
                    "Flags:\n"
                    "  -a, --all     → also remove all unused images\n"
                    "                  (any image not referenced by a running container)\n"
                    "  --volumes     → also remove unused named volumes\n"
                    "  -f, --force   → skip confirmation prompt\n\n"
                    "Nuclear option:\n"
                    "  docker system prune -a --volumes\n"
                    "  → removes everything not currently in use\n"
                    "  → use with extreme caution in production\n\n"
                    "This is the final command in the investigation — after the evidence\n"
                    "has been extracted and documented, the compromised environment\n"
                    "gets wiped clean."
                ),
                "answer": "prune",
                "hints": [
                    "To prune means to cut away what's unneeded.",
                    "docker system ___",
                    "The answer is: prune",
                ],
            },
        ],
    },
}

ZONE_ORDER = [
    "surface_layer",
    "image_vault",
    "container_grid",
    "port_matrix",
    "volume_sanctum",
    "network_forge",
    "build_engine",
    "compose_matrix",
    "registry_core",
]
