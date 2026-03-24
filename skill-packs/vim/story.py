"""
story.py - Narrative text for Vim Quest
Theme: Deep inside a compromised network, Ghost needs to read and edit files
       with no GUI available. Only the terminal. Only vim.
"""

INTRO_STORY = """
You're twelve hops deep in the NEXUS network.

Not through the front door — through a forgotten maintenance subnet,
a decommissioned jump host that still has valid certificates, a chain of
[bold cyan]SSH tunnels[/bold cyan] that took four hours to build and five minutes to traverse.

You're in. The problem: every GUI tool is locked behind an authenticated proxy.
No VS Code. No Sublime. No nano, because the sysadmin who set up this server
considered nano a security risk and removed it. Paranoid, but thorough.

What's available: [bold white]vim[/bold white].

[bold magenta]Vim is on every Unix system. Has been since 1991. The sysadmins learned it
because they had to. The developers avoided it because they could.
Ghost learned it because there would always be a moment like this one —
twelve hops deep, no GUI, config files that need editing, log files that
need reading, and only one editor available.[/bold magenta]

The financial processing config is at [yellow]/etc/nexus/processor.conf[/yellow].
The disbursement routing table is at [yellow]/var/lib/nexus/routes.db[/yellow].
The audit log — the one that was supposed to catch the fraud — is at
[yellow]/var/log/nexus/audit.log[/yellow], and it's [bold red]empty[/bold red]. Someone cleared it.
That clearing is itself evidence, but first you need to read the rotation
logs to find out when it happened.

All of this requires opening files, reading them, navigating them,
sometimes editing them. Without leaving fingerprints. Without exiting
to a command that might be logged differently.

[bold white]You need to know vim. Not just survive vim. Know it.[/bold white]

The files are waiting. The cursor is in normal mode.
[bold cyan]Begin.[/bold cyan]
"""

ZONE_INTROS = {
    "normal_vault": """
[bold cyan]== THE NORMAL VAULT ==[/bold cyan]

Normal mode is the default. It is the mode vim is in when you open a file.
It is the mode you should be in most of the time.

Most people who fear vim fear this: they opened a file, they started typing,
nothing appeared, they pressed Escape six times and nothing changed, they typed
[yellow]:q![/yellow] and weren't sure if it worked.

They were thinking about it wrong.

Normal mode is not "the mode before you can do anything." It is the [italic]primary[/italic]
mode. Every other mode is a temporary excursion from normal mode. You go into
insert mode to type text. You return to normal mode to do everything else.

[yellow]h j k l[/yellow] — left, down, up, right. No arrow keys needed.
[yellow]w / b / e[/yellow] — word forward, word backward, end of word.
[yellow]gg / G[/yellow] — top of file, bottom of file.
[yellow]0 / $[/yellow] — beginning of line, end of line.

[italic]"Normal mode is not a cage. It's a cockpit."[/italic]
""",
    "insert_protocol": """
[bold cyan]== THE INSERT PROTOCOL ==[/bold cyan]

Insert mode is where text is written. The trick is knowing the fastest way in
and the fastest way out — and knowing that there are multiple entry points,
each optimized for a different situation.

The audit log rotation config needs one line changed. One line. Getting there
efficiently, changing it precisely, and returning to normal mode without
disturbing anything else — that's what this zone covers.

[yellow]i[/yellow] — insert before cursor.
[yellow]a[/yellow] — insert after cursor (append).
[yellow]o[/yellow] — open a new line below and enter insert mode.
[yellow]O[/yellow] — open a new line above.
[yellow]I[/yellow] — insert at the beginning of the line.
[yellow]A[/yellow] — insert at the end of the line.
[yellow]ESC / Ctrl+C[/yellow] — return to normal mode.

[italic]"Insert mode is the exception, not the rule.
You enter it, make the change, and leave."[/italic]
""",
    "command_line": """
[bold cyan]== THE COMMAND LINE ==[/bold cyan]

The [yellow]:[/yellow] key drops you into command-line mode — vim's interface to the filesystem,
the editor settings, and the system itself.

[yellow]:w[/yellow] saves the file. [yellow]:q[/yellow] quits. [yellow]:wq[/yellow] saves and quits.
[yellow]:q![/yellow] quits without saving — critical when you open the wrong file,
or open a file read-only, or realize the change you made needs to be undone
and you want a clean exit.

[yellow]:e filename[/yellow] opens a different file without leaving vim.
[yellow]:vs[/yellow] and [yellow]:sp[/yellow] split the screen vertically or horizontally.
[yellow]:set[/yellow] changes editor behavior.

The processor.conf and the audit log need to be read in the same session.
Command-line mode is how you navigate between them.

[italic]"The command line is vim's API.
You're not clicking through menus — you're programming the editor."[/italic]
""",
    "visual_mode": """
[bold cyan]== VISUAL MODE ==[/bold cyan]

Visual mode is selection. Mark a region of text, then operate on it.

The routing table has fifty-three entries. Seventeen of them need to be
deleted. In a GUI editor: click, shift-click, delete. In vim: visual mode,
motion, [yellow]d[/yellow].

Three flavors:
[yellow]v[/yellow] — character-wise visual (select individual characters).
[yellow]V[/yellow] — line-wise visual (select whole lines).
[yellow]Ctrl+V[/yellow] — block visual (select a rectangular column of text).

Block visual is the power feature. Select a column across twenty lines,
insert at the beginning of all of them simultaneously — one operation,
twenty lines changed.

[italic]"Visual mode is how you tell vim what you're talking about
before you tell it what to do."[/italic]
""",
    "search_engine": """
[bold cyan]== THE SEARCH ENGINE ==[/bold cyan]

The audit log rotation config is 4,000 lines. The relevant setting is
somewhere in the middle. You could scroll — or you could search.

[yellow]/pattern[/yellow] — search forward.
[yellow]?pattern[/yellow] — search backward.
[yellow]n[/yellow] — next match. [yellow]N[/yellow] — previous match.
[yellow]*[/yellow] — search for the word under the cursor.

And then search-and-replace:
[yellow]:s/old/new/g[/yellow] — replace all occurrences on the current line.
[yellow]:%s/old/new/g[/yellow] — replace all occurrences in the entire file.
[yellow]:%s/old/new/gc[/yellow] — replace all, confirming each one.

The disbursement routing table has a vendor name that appears in 23 places.
The vendor is one of the phantom subsidiaries. All 23 entries need to be flagged.

[italic]"Search is navigation. Replace is surgery."[/italic]
""",
    "motion_objects": """
[bold cyan]== MOTION & TEXT OBJECTS ==[/bold cyan]

The most efficient vim usage comes from combining verbs with objects.
[yellow]d[/yellow] (delete), [yellow]c[/yellow] (change), [yellow]y[/yellow] (yank/copy) — all take a motion or text object.

[yellow]dw[/yellow] — delete to next word boundary.
[yellow]ciw[/yellow] — change inner word (delete the whole word, enter insert mode).
[yellow]ci"[/yellow] — change inside quotes (everything between the quote marks).
[yellow]da([/yellow] — delete around parentheses (including the parens themselves).
[yellow]yap[/yellow] — yank a paragraph.

The config file uses [yellow]key = "value"[/yellow] pairs throughout.
Changing a value means: go to the value, [yellow]ci"[/yellow], type the new value, [yellow]ESC[/yellow].
Three keystrokes to position, three to change, one to exit.

[italic]"Text objects are vim's vocabulary.
Once you have the vocabulary, you stop thinking about keystrokes
and start thinking about what you want to do."[/italic]
""",
    "split_network": """
[bold cyan]== THE SPLIT NETWORK ==[/bold cyan]

Three files. One session. No switching back and forth between terminal windows —
that would generate additional process logs. Everything in vim, in one session.

[yellow]:vs filename[/yellow] — vertical split, open file on the right.
[yellow]:sp filename[/yellow] — horizontal split, open file below.
[yellow]Ctrl+W h/j/k/l[/yellow] — move between splits (same direction keys as cursor movement).
[yellow]Ctrl+W =[/yellow] — equalize split sizes.

[yellow]:ls[/yellow] — list all open buffers.
[yellow]:b N[/yellow] — switch to buffer N.
[yellow]:bnext / :bprev[/yellow] — cycle through buffers.

The processor config, the routing table, and the audit log — all open simultaneously,
cross-referenced, evidence extracted.

[italic]"Splits turn vim into a workbench. Multiple files, one window,
zero additional processes in the logs."[/italic]
""",
    "macro_forge": """
[bold cyan]== THE MACRO FORGE ==[/bold cyan]

The routing table has 417 flagged transactions. Each one needs a specific
annotation added. Doing it manually: 417 repetitive operations. Using a macro:
record once, replay 416 times. Done in seconds.

[yellow]q{register}[/yellow] — start recording a macro into a register (e.g. [yellow]qa[/yellow]).
[yellow]q[/yellow] — stop recording.
[yellow]@{register}[/yellow] — replay the macro (e.g. [yellow]@a[/yellow]).
[yellow]@@[/yellow] — replay the last macro.
[yellow]N@{register}[/yellow] — replay N times (e.g. [yellow]416@a[/yellow]).

[yellow]:[range]normal @{register}[/yellow] — apply a macro to a range of lines.
[yellow]:%normal @a[/yellow] — apply macro to every line in the file.

[italic]"A macro is a program inside the editor.
When the task is repetitive, the answer is always a macro."[/italic]
""",
}

ZONE_COMPLETIONS = {
    "normal_vault": """
[bold green]THE NORMAL VAULT — MAPPED.[/bold green]

Movement without the mouse. Navigation without arrow keys. The file is a space
you move through deliberately — [cyan]gg[/cyan] to the top, [cyan]G[/cyan] to the bottom,
[cyan]w[/cyan] and [cyan]b[/cyan] through words, [cyan]/[/cyan] to search. You're not hunting for the cursor.
You're sending it where you need it.

[bold cyan]The Insert Protocol: entering the text without triggering noise.[/bold cyan]
""",
    "insert_protocol": """
[bold green]THE INSERT PROTOCOL — CLEARED.[/bold green]

In, change, out. The rotation config has been updated. One line — the retention
period — changed from 7 days to 90. When the investigators get here,
the logs will exist. [cyan]i[/cyan], [cyan]a[/cyan], [cyan]o[/cyan] — the entry points.
[cyan]ESC[/cyan] — the exit. Clean.

[bold cyan]The Command Line: saving files, opening files, staying in one session.[/bold cyan]
""",
    "command_line": """
[bold green]THE COMMAND LINE — MASTERED.[/bold green]

[cyan]:w[/cyan], [cyan]:e[/cyan], [cyan]:vs[/cyan]. All three files open. Nothing left unsaved.
The command line is how vim interfaces with the world outside the buffer.
You know how to use it now — not just [cyan]:wq[/cyan] to escape, but as an actual tool.

[bold cyan]Visual Mode: selecting precisely, operating efficiently.[/bold cyan]
""",
    "visual_mode": """
[bold green]VISUAL MODE — DEPLOYED.[/bold green]

Seventeen routing entries deleted. [cyan]Ctrl+V[/cyan] selected the column of flags,
[cyan]I[/cyan] inserted the annotation prefix on all of them simultaneously.
Block visual is not a power-user feature — it's a fundamental operation.

[bold cyan]The Search Engine: finding the needle in 4,000 lines.[/bold cyan]
""",
    "search_engine": """
[bold green]THE SEARCH ENGINE — ONLINE.[/bold green]

[cyan]:%s/phantom_vendor/[FLAGGED: phantom_vendor]/g[/cyan] — 23 replacements, one command.
The disbursement table is annotated. The audit trail is building.
Search and replace is not about convenience. It's about precision at scale.

[bold cyan]Motion & Text Objects: the grammar that makes vim fast.[/bold cyan]
""",
    "motion_objects": """
[bold green]MOTION & TEXT OBJECTS — INTERNALIZED.[/bold green]

[cyan]ci"[/cyan] to change a quoted value. [cyan]dap[/cyan] to delete a paragraph. [cyan]yi([/cyan] to copy
inside parentheses. The config values are changed with three keystrokes each.
The grammar is starting to feel like thinking rather than typing.

[bold cyan]The Split Network: three files, one session, no extra processes.[/bold cyan]
""",
    "split_network": """
[bold green]THE SPLIT NETWORK — ACTIVE.[/bold green]

Three panes. [cyan]Ctrl+W l[/cyan] to move right. [cyan]Ctrl+W h[/cyan] to move left. The processor
config, the routing table, and the audit log rotation — all in view simultaneously.
Cross-referenced. Evidence extracted without spawning a single new process.

[bold cyan]The Macro Forge: 417 annotations, one macro, seconds.[/bold cyan]
""",
    "macro_forge": """
[bold yellow]★ ★ ★  THE MACRO FORGE — COMPLETE.  ★ ★ ★[/bold yellow]

[bold white]The vim session is closed.[/bold white]

417 transactions annotated. The routing table flagged. The audit log rotation
extended so the logs will survive long enough for the investigators to subpoena
them. All of it done in one vim session, leaving the minimum possible trace.

[cyan]qa[/cyan] to record. [cyan]q[/cyan] to stop. [cyan]416@a[/cyan] to repeat. Done.

The editor is not the obstacle. The editor is the tool.
[bold white]You know the tool now.[/bold white]

[bold magenta]"The moment vim stops feeling like fighting and starts feeling like thinking —
that's when you know you have it."[/bold magenta]

[bold yellow]VIM STATUS: GRANDMASTER. FILES: EDITED. EVIDENCE: PRESERVED.[/bold yellow]
""",
}

BOSS_INTROS = {
    "normal_vault": "[bold red]⚠  MOVEMENT TRIAL: The Cursor Challenge[/bold red]\nNavigate a 4,000-line file without arrow keys, without a mouse, and find what you need in under a minute. Prove you know normal mode.",
    "insert_protocol": "[bold red]⚠  EDIT TRIAL: The One-Line Change[/bold red]\nOne specific line in the config needs to change. Get there, change exactly the right thing, get out. Efficiency is the test.",
    "command_line": "[bold red]⚠  SESSION MANAGEMENT: The Three-File Session[/bold red]\nThree files. One vim session. Navigate between them, save changes to two, discard changes in one. All without leaving vim.",
    "visual_mode": "[bold red]⚠  SELECTION TRIAL: The Block Operation[/bold red]\nA column of values in a structured file needs to be modified simultaneously. Block visual mode. One operation. All rows.",
    "search_engine": "[bold red]⚠  REPLACEMENT TRIAL: The 23 Vendors[/bold red]\nA vendor name appears 23 times. Replace all occurrences with a flagged version. Leave no instance unchanged.",
    "motion_objects": "[bold red]⚠  GRAMMAR TRIAL: The Config Rewrite[/bold red]\nFour key-value pairs. Change only the values. Do it with text objects — no manual counting, no hunting.",
    "split_network": "[bold red]⚠  MULTI-FILE AUDIT: The Split Session[/bold red]\nThree files open, two need changes cross-referenced from the third. Navigate. Edit. Save. All in one session.",
    "macro_forge": "[bold red]★  MACRO TRIAL: The 417 Annotations[/bold red]\nRecord one macro that annotates a transaction line. Replay it 416 times. The file has 417 flagged entries. You have one shot to get the macro right.",
}

ACHIEVEMENT_DESCRIPTIONS = {
    "first_blood": ("First Edit Made", "Changed a file in vim for the first time. The cursor moved where you told it."),
    "navigator": ("Normal Mode Fluent", "Cleared the Normal Vault. hjkl is no longer a puzzle — it's a reflex."),
    "archivist": ("Insert Mode Clean", "Cleared the Insert Protocol. You enter insert mode deliberately and leave immediately."),
    "seeker": ("Command Line Operator", "Cleared the Command Line. :w, :e, :vs — you use vim's API without thinking about it."),
    "pipe_dream": ("Visual Block User", "Cleared Visual Mode. Ctrl+V is in your muscle memory now."),
    "necromancer": ("Search & Replace Expert", "Cleared the Search Engine. :%s/old/new/g — one command, entire file."),
    "warden": ("Text Object Fluent", "Cleared Motion & Objects. ci\" and dap are words in your vocabulary now."),
    "scriptor": ("Split Session Master", "Cleared the Split Network. Multiple files, one session, zero extra processes."),
    "networked": ("Macro Architect", "Cleared the Macro Forge. You recorded, you replayed, you automated."),
    "grandmaster": ("VIM GRANDMASTER", "All zones complete. Vim is no longer an obstacle. It's an extension of thought."),
    "streak_3": ("Muscle Memory", "3 correct in a row. The keystrokes are starting to feel automatic."),
    "streak_5": ("Modal Fluency", "5 in a row. You're thinking in modes now, not in keystrokes."),
    "streak_10": ("VIM ENLIGHTENED", "10 in a row. The editor doesn't exist anymore. Only the intent and the result."),
    "no_hints": ("No :help Needed", "Cleared a zone without hints. The documentation is already in your hands."),
    "speed_demon": ("Sub-5 Keystroke", "Answered in under 5 seconds. The command was already there."),
    "level_10": ("Vim Initiate", "Level 10. You can open, edit, and close a file without panicking."),
    "level_20": ("Vim Practitioner", "Level 20. Text objects feel natural. Macros are no longer exotic."),
    "level_30": ("Vim Master", "Maximum level. You think in motions and operators. The mouse is irrelevant."),
    "completionist": ("Complete Modal Mastery", "Every zone. Every challenge. Total vim fluency achieved."),
    "boss_slayer": ("Boss Challenge Cleared", "Beat your first vim boss. The file yielded."),
}
