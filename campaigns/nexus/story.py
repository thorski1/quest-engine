"""
story.py - Narrative for The NEXUS Files campaign.
One continuous story. Seven skill domains. One corporation. One truth.
"""

CAMPAIGN_INTRO = """
[bold yellow]NEXUS INFRASTRUCTURE SYSTEMS GROUP.[/bold yellow]

You won't find that name in the news. You won't find it trending anywhere.
NEXUS doesn't need a brand — it needs contracts, and it has them: the data
infrastructure for [bold white]four regional healthcare networks[/bold white], two commodity exchanges,
the personnel database for a defense contractor holding three active DHS certifications,
and the payment processing backbone for eleven state benefits systems.

If something important is happening in a computer somewhere in the United States,
there is a [bold cyan]forty-three percent chance[/bold cyan] that a NEXUS server is involved.

The fraud has been running for [bold white]eleven years[/bold white].

Not embezzlement — nothing so crude. [italic]Systematic structural overbilling[/italic] on federal
cost-plus contracts. Phantom subcontractors that exist only in the procurement
documents. A cascade of subsidiaries, each one legitimate on paper, each one
routing a small percentage of every contract upward through the structure.
Small percentages of very large contracts.

The total is somewhere north of [bold red]four billion dollars[/bold red].

A whistleblower surfaced six weeks ago. Sent documentation to a congressional
investigator, to a journalist, to a federal attorney. Then disappeared — not
dramatically. Just: went silent, deleted their accounts, stopped responding.
The documentation makes the case. It doesn't prove it. To prosecute, they need
the [bold white]primary financial records[/bold white]. The ones inside NEXUS.

Someone hired you to get them out.

[bold magenta]You are Ghost. No fixed address. No corporate affiliation. Five years,
nineteen networks, zero artifacts left behind. You get in, you get what's needed,
and you get out. Your handler calls you the best in the business. You don't
disagree — you've seen the business.[/bold magenta]

The dossier came through a cutout three days ago. NEXUS runs on four layers:
the [cyan]terminal infrastructure[/cyan], a [cyan]code repository[/cyan] at the center of everything,
[cyan]containerized services[/cyan] that process the financial transactions, and a
[cyan]database[/cyan] holding eleven years of primary records.

All four layers will need to be navigated. All four will require fluency.
There are no shortcuts, no exploit kits, no zero-days. This is a skills operation.

[bold white]You have seventy-two hours before the investigators need your report.[/bold white]

The clock is running.

[bold cyan]Begin.[/bold cyan]
"""

CHAPTER_INTROS = {
    "ssh": """
The workstation is a foothold, not a destination.

The financial processing system runs on servers you can't reach from here —
not directly. NEXUS's internal network is segmented. The servers that matter
are behind jump hosts, firewall rules, and a bastion that logs every connection.

None of that matters once you know SSH properly.

Not just [yellow]ssh user@host[/yellow]. The full stack: key pairs, the config file that maps
the entire infrastructure in plain text, tunnels that make firewalled ports
appear on localhost, jump chains that traverse four servers with one command.

The sysadmin whose workstation you're on has [yellow]~/.ssh/config[/yellow] with seven entries.
The keys are in [yellow]~/.ssh/[/yellow]. Some of them are still valid.

[bold white]Navigate the network. The servers that matter are on the other side of it.[/bold white]
""",
    "vim": """
You're deep in the network now. Twelve hops in. Remote servers with no GUI,
no VS Code, no nano — the sysadmin who set these up removed it.

Three files need to be read, cross-referenced, and partially edited:
[yellow]/etc/nexus/processor.conf[/yellow], [yellow]/var/lib/nexus/routes.db[/yellow], and the audit log.

The only editor available on all three servers is [bold white]vim[/bold white].

Most people know enough vim to escape it: [yellow]:q![/yellow]. That's not going to be
enough here. You need to navigate 4,000-line files, search and replace
across the routing table, edit config values with text objects, and annotate
417 transaction entries with a single macro.

[bold white]The files are waiting. The cursor is in normal mode. Begin.[/bold white]
""",
    "bash": """
Every infiltration starts at the terminal.

NEXUS's outer layer is standard — filesystem controls, process management,
network services. The corps assume nobody fluent in raw shell still exists.
They've automated everything, abstracted everything, hidden the terminal
behind twelve layers of GUI. Their developers haven't touched a command line
in years.

That is their vulnerability. That is your entry point.

You have local access to a NEXUS workstation — a junior administrator's
machine, acquired through a social engineering approach that took four days
and a convincing LinkedIn profile. From here, you can navigate the filesystem,
examine running processes, read configuration files, trace the network topology.

The goal of this phase: [bold white]understand the shape of what you're inside.[/bold white]

Navigate. Read. Pipe. Script. Find the thread.

[italic]"The terminal is not legacy. It's the only honest interface
the machine has. Everything else is theater."[/italic]
""",
    "git": """
You found it.

In [yellow]/var/repos/nexus-core[/yellow], buried three directories deep in a service account's
home directory, a git repository. Eleven years of commit history.
The repository tracks the core financial processing code — the algorithm
that calculates contract amounts, processes disbursements, generates the
reports that go to the federal auditors.

The history has been [bold red]tampered with[/bold red].

You can see it in the commit graph — gaps in the parent chain, timestamps
that don't align with the badge access logs you pulled from the admin console,
author fields that reference accounts that didn't exist until [italic]after[/italic] the commits
they claim to have made. Someone ran [yellow]git rebase -i[/yellow] on this repository
and called it "cleanup."

The reflog is still there. The original commit hashes are still there.
They cleaned the history and forgot that git keeps two histories —
the one you see in [yellow]git log[/yellow], and the one that records every change to
every branch pointer, every hard reset, every force push.

[bold white]Read the history. Find what they removed. Prove it was there.[/bold white]

[italic]"Git doesn't lie. It just waits for someone who knows how to read it."[/italic]
""",
    "docker": """
The code doesn't run on bare metal. Nothing at NEXUS does.

The financial processing algorithm — the one whose history was rewritten —
runs as a containerized microservice. Fifty-three microservices in total,
spread across three private Kubernetes clusters and a Docker Swarm deployment
that's been running since 2019 and nobody has touched since.

The containers are where the fraud [italic]operated[/italic]. Not just where the code ran —
where the specific misconfigurations that allowed the fraud to run undetected
for eleven years were deliberately introduced and maintained.

Bind mounts that shouldn't exist. Ports published to interfaces that should
have been firewalled. Services sharing networks they had no business being on.
A private registry that logs every push — including the force pushes that
rewrote production images after the code was "cleaned."

[bold white]Map the container infrastructure. Document every misconfiguration.
Understand how the fraud ran without triggering an audit.[/bold white]

[italic]"A container is not a vault. It's an isolation boundary.
The difference matters when someone is determined to find where the boundary is weak."[/italic]
""",
    "postgres": """
Everything leads here.

The terminal gave you access. The git history gave you the timeline.
The container audit gave you the mechanism. Now you need the [bold white]primary records[/bold white].

NEXUS runs Postgres. A single cluster, horizontally partitioned,
[bold cyan]two hundred billion rows[/bold cyan] of financial transaction data going back to the beginning.
Every contract disbursement. Every vendor payment. Every invoice processed
through the system in eleven years. The ones that went to legitimate vendors.
The ones that went to the phantom subsidiaries. The ones that were billed
at two hundred percent of cost with no supporting documentation.

It's all in there. The congressional investigators know it exists.
They can't subpoena it because NEXUS's lawyers have stalled the discovery
process for eight months and will stall it for eight more.

You don't need a subpoena.

[bold white]Extract the evidence. Run the queries. Find the chain.[/bold white]

[italic]"The database doesn't know it's evidence. It just answers queries.
Ask it the right questions."[/italic]
""",
}

CHAPTER_OUTROS = {
    "ssh": """
The network is mapped. Seven servers reached through a chain of jump hosts
and tunnels that the firewall never saw as anything but SSH on port 22.

The config file was a treasure map. The keys were already here.
The tunnel to the database is running in the background.

The processing servers don't run on bash commands. They have config files,
routing tables, audit logs. You need to read them — and the only tool available
on every server in the NEXUS estate is an editor that most people are afraid of.

[bold cyan]Vim is next. The files are waiting.[/bold cyan]
""",
    "vim": """
The files are edited. The evidence is annotated. 417 transactions flagged
with a single macro. The audit log rotation extended to 90 days.

The vim session is closed. One session, three files, zero extra processes in the logs.
The editor wasn't the obstacle — it was the tool.

The config files pointed to a repository. Eleven years of commit history,
recently accessed by a service account that has no business touching source code.

[bold cyan]The git repository is next. Someone tried to clean the history.[/bold cyan]
""",
    "bash": """
The filesystem is mapped. Every service catalogued. The network topology traced
from the workstation outward through seven internal subnets.

In [yellow]/var/repos/nexus-core[/yellow], a git repository.
Eleven years of commits. Recently accessed — not by any developer.
By a service account that has no business touching source code.

Someone tried to clean the history.

[bold cyan]The repository is next.[/bold cyan]
""",
    "git": """
The history is reconstructed.

Three commits that shouldn't exist — authored before the accounts that claim
to have written them were even created. Pushed from IP addresses that resolve
to a NEXUS office location that was officially vacated in 2021.

The original commit hashes are in your report. The reflog entries are
timestamped, signed, chain-of-custody intact.

The code is deployed. It runs in containers. The containers are where the
fraud [italic]operated[/italic] — not just where the code ran, but where it was configured
to run without detection. That's the next layer.

[bold cyan]The container infrastructure is next.[/bold cyan]
""",
    "docker": """
Nine misconfigurations documented.

The bind mount that gave the financial processing container read-write access
to the host filesystem. The debug port published to every network interface,
including the one facing the public internet. The default bridge network
that let the financial service communicate directly with the disbursement
service — no authentication layer, no logging, no firewall.

The registry access logs show a [yellow]git push --force[/yellow] at 2:47 AM, six hours
before the breach that covered the tracks. The account used was a DevOps
contractor who'd been offboarded that afternoon. His token stayed active
for six more hours.

None of this is accident. This is [bold white]architecture[/bold white].

The data that flowed through this infrastructure — every phantom invoice,
every inflated disbursement — ended up in one place.

[bold cyan]The database is next. The primary records. The proof.[/bold cyan]
""",
    "postgres": """
The queries returned.

[bold white]Four hundred and seventeen transactions[/bold white] paid to vendors that don't exist —
shell companies, each one incorporated in a different state, each one
dissolving within eighteen months of its last NEXUS payment.

[bold white]Eleven years[/bold white] of systematic overbilling on seventeen federal contracts,
the excess routed through the subsidiary structure at a rate that kept
each individual transaction below the threshold that triggers automatic audit.

The financial trail is complete. Every disbursement, every vendor,
every timestamp. The data was always there. It just needed someone
who knew how to ask for it.

[bold cyan]Evidence package assembled. Report complete.[/bold cyan]
""",
}

CAMPAIGN_FINAL = """
[bold yellow]★ ★ ★  OPERATION COMPLETE  ★ ★ ★[/bold yellow]

[bold white]The NEXUS Files.[/bold white]

The evidence package reached the congressional investigator at 04:23 AM —
forty-three minutes before your seventy-two hour window closed.
Four hundred and seventeen fraudulent transactions. Eleven years of records.
The subsidiary structure mapped in full. The technical chain-of-custody intact
through terminal access logs, git forensics, container audit trails, and
database query results.

NEXUS's lawyers filed a motion to suppress within hours. The motion was denied.

Six weeks later, the first indictments.

[bold magenta]You were already gone.[/bold magenta]

No fixed address. New identity. New cutout. Somewhere with better internet
and a terminal window open to a command prompt that nobody else knows about.

The work was clean. The skills were everything.

[italic]Shell. Git. Docker. Postgres.[/italic]
[italic]The four domains of knowing what a computer is actually doing.[/italic]
[italic]Not what the GUI says. Not what the dashboard shows. What's actually there.[/italic]

[bold white]You know now. That knowledge doesn't expire.[/bold white]

[bold cyan]Ghost, signing off.[/bold cyan]
"""
