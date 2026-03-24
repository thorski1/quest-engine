"""
story.py - Narrative text for SSH Quest
Theme: Ghost needs to pivot through NEXUS's remote systems. SSH is the
       covert movement layer — tunnels, keys, and hops through the network.
"""

INTRO_STORY = """
The workstation is compromised. That's the easy part.

The financial processing system doesn't run on the workstation.
It runs on [bold cyan]remote servers[/bold cyan] — three of them, in two data centers,
accessible only through a jump host that sits in a DMZ subnet
behind two firewall rules and a bastion that logs every connection.

In theory, you shouldn't be able to reach any of them from here.

In practice, [bold white]SSH[/bold white] is the most powerful lateral movement tool
ever deployed at scale — and NEXUS has been running it on every
server they own since 1998. The key is not breaking the protocol.
The key is knowing the protocol better than whoever configured it.

[bold magenta]Every sysadmin at NEXUS uses SSH to manage these servers.
That means there are SSH keys in home directories. There are
configured hosts in ~/.ssh/config files. There are port forwards
running in tmux sessions that the sysadmin started three weeks
ago and hasn't thought about since. There are authorized_keys files
that still list accounts for contractors who left two years ago.[/bold magenta]

You don't need to break SSH. You need to [italic]use[/italic] it —
fluently, quietly, leaving as few traces as possible.

A basic connection looks like [yellow]ssh user@host[/yellow].
A multi-hop tunnel that forwards the database port through two
jump hosts and decrypts traffic at the destination looks like:
[yellow]ssh -J user@bastion1,user@bastion2 -L 5432:db:5432 user@internal[/yellow].

There's a spectrum between those two. You need to know all of it.

[bold cyan]The jump host is waiting. The keys are somewhere in this filesystem.
Begin.[/bold cyan]
"""

ZONE_INTROS = {
    "connection_basics": """
[bold cyan]== CONNECTION BASICS ==[/bold cyan]

The foundation: connecting to a remote host.

[yellow]ssh user@hostname[/yellow] — the simplest form. Everything else is built on top of this.

The connection establishes an encrypted channel. Every byte that travels
between your terminal and the remote host is encrypted — no eavesdropping
on the network. The remote host's commands execute on the remote machine,
but their output appears in your terminal.

This is how NEXUS's sysadmins manage every server in their infrastructure.
This is also how Ghost moves.

[italic]"SSH is the universal remote access protocol.
Knowing it completely is knowing the shape of the entire infrastructure."[/italic]
""",
    "key_vault": """
[bold cyan]== THE KEY VAULT ==[/bold cyan]

Password authentication is loud. Every failed password attempt is logged.
Password authentication requires the password to exist somewhere — and
passwords get written down, get reused, get captured.

Key authentication is different. The private key never leaves your machine.
The server has your public key. The authentication is cryptographic proof —
you possess the private key that corresponds to the public key in
[yellow]~/.ssh/authorized_keys[/yellow].

The sysadmin whose workstation you're on has keys in [yellow]~/.ssh/[/yellow].
Some of them still work on servers they've been rotated out of.

[italic]"The key vault is always full. The question is whether anyone
is keeping track of what's in it."[/italic]
""",
    "config_matrix": """
[bold cyan]== THE CONFIG MATRIX ==[/bold cyan]

The [yellow]~/.ssh/config[/yellow] file is a treasure map.

Every entry is a named shortcut to a remote system. Host aliases, usernames,
key file paths, port numbers, jump proxies — all configured once and invoked
by a single name. The sysadmin who set this up knows their infrastructure
intimately. You're about to learn it from their config file.

[yellow]Host nexus-db[/yellow]
[yellow]  HostName 10.20.30.40[/yellow]
[yellow]  User admin[/yellow]
[yellow]  IdentityFile ~/.ssh/nexus_key[/yellow]
[yellow]  ProxyJump bastion[/yellow]

This is better than a network diagram.

[italic]"~/.ssh/config is the most honest documentation in any organization.
It reflects what the operators actually do, not what the runbooks say."[/italic]
""",
    "transfer_ops": """
[bold cyan]== TRANSFER OPERATIONS ==[/bold cyan]

Data doesn't move itself. Evidence needs to come out.
Configuration files need to go in.

[yellow]scp[/yellow] — secure copy. Same syntax as [yellow]cp[/yellow] but with remote paths.
[yellow]rsync[/yellow] — synchronize files over SSH. Incremental, bandwidth-efficient,
resumable.
[yellow]sftp[/yellow] — interactive file transfer session.

The routing table is on a remote server. It needs to come here.
Securely. Without leaving obvious traces in the file transfer logs.

[italic]"Getting data out is often harder than getting in.
The protocols are the same in both directions."[/italic]
""",
    "tunnel_network": """
[bold cyan]== THE TUNNEL NETWORK ==[/bold cyan]

The database isn't accessible from the public internet.
It's on a private subnet, behind a firewall, accessible only from
within the NEXUS internal network.

[yellow]SSH port forwarding[/yellow] tunnels a port from a remote network through
the encrypted SSH connection to a local port. The firewall sees
a legitimate SSH connection. From your machine's perspective,
the database is on localhost.

[yellow]ssh -L 5432:db.internal:5432 user@jumphost[/yellow]
→ localhost:5432 is now the NEXUS database.

[italic]"The firewall sees one connection going in on port 22.
It doesn't see what's flowing through it."[/italic]
""",
    "jump_chain": """
[bold cyan]== THE JUMP CHAIN ==[/bold cyan]

The database server is not directly reachable from the bastion.
It's reachable from an internal jump host, which is reachable from
the bastion, which is reachable from the DMZ, which is reachable
from the workstation you're on.

Four hops. One command.

[yellow]ssh -J user@hop1,user@hop2,user@hop3 user@final[/yellow]

Each comma-separated host in the [yellow]-J[/yellow] list is a hop. SSH negotiates
the chain, establishing a new connection through each host, until
it reaches the destination. From your terminal's perspective:
one session, one command, four servers deep.

[italic]"The network was designed to route around damage.
SSH was designed to route around restrictions."[/italic]
""",
    "agent_protocol": """
[bold cyan]== THE AGENT PROTOCOL ==[/bold cyan]

Typing a passphrase at every hop is slow and leaves keystrokes in logs.
[yellow]ssh-agent[/yellow] is a background process that holds decrypted private keys in
memory and handles authentication challenges on your behalf.

More critically: [yellow]agent forwarding[/yellow] passes the agent through the SSH
connection itself. The remote server can use your local agent to
authenticate further connections — without your private key ever
leaving your machine.

[yellow]ssh -A user@host[/yellow]
→ The host can use your agent for onward connections.

[italic]"The agent never sends the key. It signs the challenge.
The private key never moves — only the proof of possession does."[/italic]
""",
    "hardening_core": """
[bold cyan]== THE HARDENING CORE ==[/bold cyan]

The final zone. The one the defenders need to understand.

NEXUS's SSH configuration is not hardened. You know this because you've
been moving through it for hours. [bold red]PasswordAuthentication yes[/bold red] on the
bastion. [bold red]PermitRootLogin yes[/bold red] on three servers. Authorized keys that
haven't been audited in four years.

Understanding how to harden SSH is understanding every mistake
that made this infiltration possible — and every setting that
would have stopped it.

[yellow]sshd_config[/yellow] — the server-side configuration. It determines
who can connect, how, and from where.

[italic]"The attacker learns the misconfiguration to exploit it.
The defender learns it to prevent it. The knowledge is the same."[/italic]
""",
}

ZONE_COMPLETIONS = {
    "connection_basics": """
[bold green]CONNECTION BASICS — ESTABLISHED.[/bold green]

The first hop is made. User, host, port — the three coordinates of any
remote system. [cyan]ssh user@host[/cyan] is the address. Everything else is options.
You're on the jump host. The internal network is visible from here.

[bold cyan]The Key Vault: finding and using the keys that are already here.[/bold cyan]
""",
    "key_vault": """
[bold green]THE KEY VAULT — ACCESSED.[/bold green]

Three keys in [cyan]~/.ssh/[/cyan]. Two of them still work.
[cyan]ssh-keygen[/cyan], [cyan]ssh-copy-id[/cyan], [cyan]authorized_keys[/cyan] — you know the
lifecycle of a key now, and you know how to find the ones that should have been rotated.

[bold cyan]The Config Matrix: the map left in plain text.[/bold cyan]
""",
    "config_matrix": """
[bold green]THE CONFIG MATRIX — READ.[/bold green]

[cyan]~/.ssh/config[/cyan] had seven entries. The [cyan]nexus-db[/cyan] entry pointed to the
internal database server through the production bastion. The IdentityFile pointed
to a key that still works. Three lines of config replaced an entire pivot procedure.

[bold cyan]Transfer Operations: getting the evidence out.[/bold cyan]
""",
    "transfer_ops": """
[bold green]TRANSFER OPERATIONS — COMPLETE.[/bold green]

[cyan]scp[/cyan], [cyan]rsync[/cyan], [cyan]sftp[/cyan] — the data transfer layer over SSH.
The routing table is local now. The config files are backed up.
The evidence package is accumulating.

[bold cyan]The Tunnel Network: reaching what the firewall thinks is unreachable.[/bold cyan]
""",
    "tunnel_network": """
[bold green]THE TUNNEL NETWORK — ACTIVE.[/bold green]

[cyan]ssh -L 5432:db.internal:5432 user@jumphost[/cyan] — one command.
localhost:5432 is the NEXUS database. The firewall saw one legitimate SSH
connection. It didn't see the database port running through it.

[bold cyan]The Jump Chain: four hops in one command.[/bold cyan]
""",
    "jump_chain": """
[bold green]THE JUMP CHAIN — COMPLETE.[/bold green]

[cyan]ssh -J bastion,internal-jump user@db-server[/cyan]. Two hops. One command.
The [cyan]ProxyJump[/cyan] directive in [cyan]~/.ssh/config[/cyan] makes it automatic.
The final server is reachable. The connection is established. The session is running.

[bold cyan]The Agent Protocol: eliminating passphrases, forwarding auth.[/bold cyan]
""",
    "agent_protocol": """
[bold green]THE AGENT PROTOCOL — RUNNING.[/bold green]

[cyan]ssh-agent[/cyan] is loaded. The key is added. [cyan]-A[/cyan] forwards the agent through the connection.
From the remote server, the onward hops authenticate using the local agent —
no key material ever transmitted, no passphrase ever typed after the first.

[bold cyan]The Hardening Core: the final zone. The mistakes that made this possible.[/bold cyan]
""",
    "hardening_core": """
[bold yellow]★ ★ ★  THE HARDENING CORE — AUDITED.  ★ ★ ★[/bold yellow]

[bold white]The SSH infiltration is complete.[/bold white]

Seven misconfigured servers. Four unnecessary enabled options.
Three unauthorized keys in [cyan]authorized_keys[/cyan] files. Two servers with
[cyan]PermitRootLogin yes[/cyan]. One organization that thought SSH was secure
because they were using it.

SSH [italic]is[/italic] secure. The protocol is sound. The implementations are sound.
The configurations were not.

You moved through NEXUS's entire server infrastructure using their
own keys, their own jump hosts, their own agent forwarding setup.
They handed you the network.

[bold magenta]"SSH is the most powerful protocol ever deployed at scale.
The misconfiguration rate suggests most organizations don't realize this."[/bold magenta]

[bold yellow]SSH SPECIALIST: GRANDMASTER. NETWORK: FULLY TRAVERSED.[/bold yellow]
""",
}

BOSS_INTROS = {
    "connection_basics": "[bold red]⚠  CONNECTION TRIAL: The First Hop[/bold red]\nThe jump host is waiting. Prove you know every flag and option needed to connect correctly.",
    "key_vault": "[bold red]⚠  KEY FORENSICS: The Orphaned Keys[/bold red]\nThree keys in ~/.ssh/. One of them is for a server you're not supposed to be able to reach. Find the right command.",
    "config_matrix": "[bold red]⚠  CONFIG AUDIT: The Seven Entries[/bold red]\nRead ~/.ssh/config correctly. Every field matters. The ProxyJump entry is the one you need.",
    "transfer_ops": "[bold red]⚠  EXFILTRATION TRIAL: The Routing Table[/bold red]\nThe routing table needs to come out. 847MB. Incrementally. Without filling the connection buffer.",
    "tunnel_network": "[bold red]⚠  TUNNEL CONSTRUCTION: The DB Port[/bold red]\nForward port 5432 from the internal database server to localhost. The firewall is not aware.",
    "jump_chain": "[bold red]⚠  MULTI-HOP: The Four-Server Chain[/bold red]\nBastion → internal jump → application server → database. One command. Prove you know ProxyJump.",
    "agent_protocol": "[bold red]⚠  AGENT FORWARDING: The Keyless Hop[/bold red]\nForward the agent. The remote server needs to authenticate onward without a key file present.",
    "hardening_core": "[bold red]★  FINAL AUDIT: The Configuration[/bold red]\nEvery misconfiguration that made this infiltration possible. Name them. Know how to prevent them.",
}

ACHIEVEMENT_DESCRIPTIONS = {
    "first_blood": ("First Connection Made", "Established your first SSH connection. The remote shell is yours."),
    "navigator": ("Connection Specialist", "Cleared Connection Basics. user@host:port is second nature."),
    "archivist": ("Key Operator", "Cleared the Key Vault. You know the full lifecycle of an SSH key."),
    "seeker": ("Config Reader", "Cleared the Config Matrix. ~/.ssh/config is a treasure map and you can read it."),
    "pipe_dream": ("Transfer Expert", "Cleared Transfer Operations. scp, rsync, sftp — data moves when you tell it to."),
    "necromancer": ("Tunnel Builder", "Cleared the Tunnel Network. The firewall thought it was blocking you."),
    "warden": ("Jump Chain Operator", "Cleared the Jump Chain. Four hops, one command. No hops skipped."),
    "scriptor": ("Agent Specialist", "Cleared the Agent Protocol. The private key never moved."),
    "networked": ("SSH Hardening Expert", "Cleared the Hardening Core. You know every mistake that made this possible."),
    "grandmaster": ("SSH GRANDMASTER", "All zones complete. You moved through a secured network using only SSH."),
    "streak_3": ("Connection Streak", "3 correct in a row. SSH is becoming second nature."),
    "streak_5": ("Tunnel Vision", "5 in a row. You see the network as a graph of SSH connections."),
    "streak_10": ("NETWORK GHOST", "10 in a row. You moved through the infrastructure and left no trace."),
    "no_hints": ("No Config Needed", "Cleared a zone without hints. The man page is already in your head."),
    "speed_demon": ("Sub-5 Connection", "Answered in under 5 seconds. The flags were already there."),
    "level_10": ("Junior Operator", "Level 10. You can connect, transfer, and disconnect without hesitation."),
    "level_20": ("Senior Operator", "Level 20. Tunnels and jump chains are reflexes."),
    "level_30": ("Master SSH Operator", "Maximum level. You understand SSH from the key exchange to the hardening config."),
    "completionist": ("Full Network Traversal", "Every zone. Every challenge. Complete SSH mastery achieved."),
    "boss_slayer": ("First Barrier Bypassed", "Beat your first SSH boss challenge. The network yielded."),
}
