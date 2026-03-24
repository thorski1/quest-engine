"""
story.py - Narrative text for Git Quest
Theme: Corporate forensic timeline audit. Every commit is evidence.
"""

INTRO_STORY = """
The litigation started eighteen months ago. A [bold cyan]wrongful termination suit[/bold cyan]
that became an IP dispute that became a securities fraud investigation that became
— somehow — a criminal referral to three different federal agencies simultaneously.

At the center of all of it: a git repository.

The corp claims the contested code was written entirely by their in-house team, on
company time, using company resources, and therefore belongs to them entirely.
The plaintiff claims she wrote the critical algorithm before she was ever hired,
and the company stole it, committed it under a different name, and then fired her
when she tried to bring it up through legal channels.

Both sides have produced git logs. The logs [bold white]disagree[/bold white] with each other.

Someone tampered with the history. The timestamps don't line up. Commit messages have been
reworded. Author fields don't match the access logs from the badge system. Somebody ran
a [yellow]git rebase[/yellow] on a production branch and called it "cleanup."

[bold white]You are a Timeline Auditor.[/bold white]

[bold magenta]Independent contractor. Forensic git specialist. Cleared for chain-of-custody work
in digital evidence cases. Three courts have accepted your testimony.[/bold magenta]

You've been handed a copy of the repository and forty-eight hours to produce a report
that answers one question: [bold yellow]what does the actual history say?[/bold yellow]

The corps' lawyers will try to tell you the history says whatever they need it to say.
You know that git doesn't lie — not if you know how to read it.
And you know how to read it.

[bold cyan]The repository is open. The commits are waiting. Start from the beginning.[/bold cyan]
"""

ZONE_INTROS = {
    "origin_vault": """
[bold cyan]== THE ORIGIN VAULT ==[/bold cyan]

Every repository has a beginning. An [yellow]init[/yellow]. A [yellow]clone[/yellow].
A moment when the ledger was opened and the first entry was made.

The corp's lawyers want you to start from the present and work backwards.
That's not how this works. You start at the origin — the first commit, the initial
configuration, the [yellow].git[/yellow] directory that contains the entire history of every
decision that was ever made in this codebase.

Before you can read the ledger, you need to understand what it is.
Before you can audit the commits, you need to understand how commits are created.

[yellow]git init[/yellow] — creates the ledger.
[yellow]git clone[/yellow] — copies it.
[yellow]git config[/yellow] — identifies who made the entries.

[italic]"The author field is not a signature. It's what someone told git their name was.
The difference is significant in a legal context."[/italic]
""",
    "staging_area": """
[bold cyan]== THE STAGING AREA ==[/bold cyan]

Between the working files and the permanent record, there is a [bold white]buffer[/bold white].

The corps' junior developers don't know this. They think git add means "save."
They think git commit means "submit." They've never looked at what actually happens
between the two — what the staging area is, what it means, why it exists.

You know exactly what it means. And right now, it matters — because whoever
manipulated this history was careless about what they staged. The diff tells a story.

[yellow]git add[/yellow] — moves changes into the staging area.
[yellow]git status[/yellow] — shows what's staged, what's not, what's tracked.
[yellow]git diff[/yellow] — shows exactly what changed, line by line.
[yellow].gitignore[/yellow] — the list of files the repository deliberately doesn't see.

[italic]"The staging area is where intent becomes record. Read it carefully."[/italic]
""",
    "commit_ledger": """
[bold cyan]== THE COMMIT LEDGER ==[/bold cyan]

A commit is not a save. It's not a backup. It's a [bold white]cryptographic assertion[/bold white].

Every commit contains: a snapshot of the code, the author's name and email,
the committer's name and email (often the same, not always), a timestamp,
a message, and a pointer to its parent commit. All of this is hashed together
into a 40-character SHA-1 that uniquely identifies it.

Change any byte of that content and the hash changes. You can't quietly edit a
commit without producing a different commit. What you [italic]can[/italic] do is rewrite
history in a way that looks clean to anyone who doesn't look carefully.

They looked clean. You're looking carefully.

[yellow]git commit[/yellow] — seals the staging area into the ledger.
[yellow]git log[/yellow] — reads the ledger, commit by commit.
[yellow]git show[/yellow] — opens any commit and shows exactly what it contained.

[italic]"Every commit is a signed statement: 'at this moment, I claim the code looked like this.'
The signature is cryptographic. The identity is not."[/italic]
""",
    "branch_matrix": """
[bold cyan]== THE BRANCH MATRIX ==[/bold cyan]

A branch is a [bold white]pointer[/bold white]. That's all it is.

Forty characters of SHA-1 hash, stored in a file under [yellow].git/refs/[/yellow],
pointing to a specific commit. When you make a new commit, the pointer moves forward.
When you create a new branch, you create a new pointer at the current position.

The corp has seventeen branches. Three of them were deleted. You can still read
what was in them — branches are pointers, and pointers can be recovered, but
the corps' lawyers don't know that. Their IT team probably doesn't either.

[yellow]git branch[/yellow] — create, list, or delete branch pointers.
[yellow]git switch[/yellow] — move to a different branch (update which commits you see).
[yellow]git checkout[/yellow] — the older, more powerful, slightly confusing version of switch.

[italic]"Branches are not copies of the code. They are references to moments in history.
You can have a thousand branches and they all point to the same commits."[/italic]
""",
    "merge_protocol": """
[bold cyan]== THE MERGE PROTOCOL ==[/bold cyan]

When two timelines converge, something has to give.

The merge commit is the moment when two separate lines of development are
reconciled into one. It has [bold white]two parents[/bold white] — a fact that shows up in the
[yellow]git log[/yellow] output if you know where to look. Most people don't look.

The contested code was on a feature branch. The feature branch was merged into
main. The merge was fast-forwarded — which means the feature branch's commits
were replayed as if they'd always been on main, and the two-parent merge commit
was never created. The branch pointer was deleted. The trail should be cold.

Should be.

[yellow]git merge[/yellow] — combines branch histories.
[yellow]git merge --no-ff[/yellow] — forces a merge commit even when fast-forward is possible.
Fast-forward merge — moves the pointer forward without creating a merge commit.

[italic]"A fast-forward is a way of saying: 'we don't want any record of when this happened.'"[/italic]
""",
    "rebase_engine": """
[bold cyan]== THE REBASE ENGINE ==[/bold cyan]

Here's the thing about [yellow]git rebase[/yellow]: it doesn't move commits. It destroys them
and creates new ones that look identical except for their parent pointer and
therefore their hash. The original commits still exist — for a while — in the
reflog. Then they get garbage-collected.

Whoever rewrote this history used interactive rebase. [yellow]git rebase -i[/yellow].
They squashed commits together. They rewrote messages. They changed the order.
They were good — good enough to fool the corp's own developers, who looked at
the log and saw nothing unusual.

They left the reflog intact. That was their mistake.

[yellow]git rebase[/yellow] — replays commits on top of a different base commit.
[yellow]git rebase -i[/yellow] — interactive rebase: reorder, squash, edit, drop commits.

[italic]"Rebase doesn't lie. It just creates a more convenient version of the truth.
The old truth is still there, if you know where to look."[/italic]
""",
    "remote_network": """
[bold cyan]== THE REMOTE NETWORK ==[/bold cyan]

The local repository is a copy. The remote is the source.

[bold white]Or is it?[/bold white]

In a normal development workflow: developers clone from the remote, make changes
locally, push back. The remote is authoritative. The remote has the canonical history.

In this case, the remote's history was rewritten [bold red]after[/bold red] it was pushed.
Someone ran a [yellow]force push[/yellow]. [yellow]git push --force[/yellow]. This overwrites the remote's
history with whatever is in the local repository, regardless of what was there before.

Force push is the equivalent of tearing pages out of a ledger and replacing them.
Most git hosting services log force pushes. Most corps don't audit those logs.

[yellow]git remote[/yellow] — manage connections to remote repositories.
[yellow]git fetch[/yellow] — download remote changes without merging.
[yellow]git pull[/yellow] — fetch + merge.
[yellow]git push[/yellow] — upload local commits to the remote.

[italic]"The remote is not the truth. The remote is the version of the truth
that whoever has push access decided you should see."[/italic]
""",
    "recovery_vault": """
[bold cyan]== THE RECOVERY VAULT ==[/bold cyan]

Nothing in git is truly deleted. Not immediately.

[yellow]git reset --hard[/yellow] doesn't delete commits — it moves the branch pointer backwards
and marks the orphaned commits for eventual garbage collection.
[yellow]git stash[/yellow] doesn't delete work — it saves it in a special stack.
The [bold yellow]reflog[/bold yellow] records every change to every branch pointer, including the
force pushes and hard resets that the corps thought would cover their tracks.

The reflog has a retention policy: 90 days by default. The tampering happened
sixty-three days ago. The reflog entries are still there.

[yellow]git stash[/yellow] — temporarily shelve uncommitted changes.
[yellow]git reset[/yellow] — move a branch pointer (--soft, --mixed, --hard).
[yellow]git revert[/yellow] — create a new commit that undoes a previous commit.
[yellow]git reflog[/yellow] — show every change to HEAD, including the ones they tried to hide.

[italic]"The reflog is the ghost history. The history of the history.
It's not proof — but it's where you start looking for proof."[/italic]
""",
    "forensics_chamber": """
[bold cyan]== THE FORENSICS CHAMBER ==[/bold cyan]

Final phase. The evidence is assembled. Now you need to prove it.

[yellow]git blame[/yellow] shows, for every line of every file, which commit last modified it
and who authored that commit. The contested algorithm — every line of it —
was last touched by a commit authored by someone who left the company
four months before the corp claims the algorithm was written.

[yellow]git bisect[/yellow] finds the exact commit where a specific change was introduced,
using binary search across the commit history. It's how you prove
[italic]when[/italic] something was added, not just [italic]that[/italic] it's there.

[yellow]git log --follow[/yellow] tracks a file across renames — critical when the corps
renamed the contested file three times trying to obscure its origin.

[yellow]git blame[/yellow] — annotate every line with its last commit.
[yellow]git bisect[/yellow] — binary search the commit history.
[yellow]git cherry-pick[/yellow] — apply a specific commit to the current branch.
[yellow]git log --follow[/yellow] — track file history across renames.

[italic]"The code doesn't remember who wrote it. Git does.
If you know how to ask."[/italic]
""",
}

ZONE_COMPLETIONS = {
    "origin_vault": """
[bold green]THE ORIGIN VAULT — CATALOGUED.[/bold green]

You know what a repository is now. Not "a folder with git in it" — a cryptographic
ledger with a complete, linked history of every change ever made, going back to the
first [cyan]git init[/cyan]. You know who the authors claim to be. You've noted the discrepancy
in the config.

[bold cyan]The Staging Area is next. This is where intent meets record.[/bold cyan]
""",
    "staging_area": """
[bold green]THE STAGING AREA — MAPPED.[/bold green]

Status. Diff. What's tracked, what's not, what's ignored and why.
The staging area tells you what someone [italic]intended[/italic] to commit — and sometimes
what they [italic]didn't[/italic] intend to leave out.

Three files in the .gitignore that shouldn't be there. Noted.

[bold cyan]The Commit Ledger holds the permanent record. Time to read it.[/bold cyan]
""",
    "commit_ledger": """
[bold green]THE COMMIT LEDGER — READ.[/bold green]

Every commit. Every author. Every timestamp. Every message.
You've run [cyan]git log[/cyan] with enough flags to see the full shape of this history.
You've opened individual commits with [cyan]git show[/cyan] and read what they actually contain.

Three commits have mismatched author and committer timestamps. Flagged.

[bold cyan]The Branch Matrix is next — seventeen branches, three of them deleted.[/bold cyan]
""",
    "branch_matrix": """
[bold green]THE BRANCH MATRIX — NAVIGATED.[/bold green]

You've moved between branches. You've listed what exists, what existed, what the
remote thinks exists. You understand that branches are pointers — lightweight,
cheap, and recoverable even after deletion if the commits they pointed to
are still in the reflog.

Two of the three deleted branches are still recoverable. The third is marginal.

[bold cyan]The Merge Protocol shows how the timelines were combined — and how
fast-forwarding can erase the record of when.[/bold cyan]
""",
    "merge_protocol": """
[bold green]THE MERGE PROTOCOL — RECONSTRUCTED.[/bold green]

You found it. The feature branch was merged with [cyan]--ff-only[/cyan], forcing a
fast-forward and leaving no merge commit in the log. The branch was then deleted.
The timestamps on the resulting commits suggest they were authored two weeks before
the earliest date the corp claims the work began.

The timeline is starting to resolve.

[bold cyan]The Rebase Engine is where the cleanup happened.[/bold cyan]
""",
    "rebase_engine": """
[bold green]THE REBASE ENGINE — DECODED.[/bold green]

Interactive rebase. Squash. Fixup. Reword. The complete toolkit of history rewriting.
You can read it in the commit graph — gaps in the parent chain, timestamps that
skip forward, message styles that shift mid-way through the log.

You know what they did. You know roughly when. You need the reflog to prove it.

[bold cyan]The Remote Network reveals the force push.[/bold cyan]
""",
    "remote_network": """
[bold green]THE REMOTE NETWORK — EXPOSED.[/bold green]

The remote access logs show a [cyan]git push --force[/cyan] at 2:47 AM on a Tuesday.
The account that did it belongs to a DevOps contractor who was offboarded the
same afternoon. His access token was active for six more hours.

Either someone used his credentials after he left, or someone forgot to revoke them
and got very lucky. Corporate negligence or deliberate cover-up — either way, it's in the log.

[bold cyan]The Recovery Vault. The reflog. The ghost history.[/bold cyan]
""",
    "recovery_vault": """
[bold green]THE RECOVERY VAULT — EXCAVATED.[/bold green]

The reflog had the original branch state, sixty-three days old.
[cyan]git reflog[/cyan] showed the HEAD movements — the hard reset, the force push, the cleanup.
You reconstructed the commits they thought were gone.
They weren't gone. They were orphaned. There's a difference.

The original commit hashes are now in your report. Timestamped. Verified.
Signed. Chain-of-custody intact.

[bold cyan]The Forensics Chamber. Final phase. Time to prove it.[/bold cyan]
""",
    "forensics_chamber": """
[bold yellow]★ ★ ★  THE FORENSICS CHAMBER — CASE CLOSED.  ★ ★ ★[/bold yellow]

[bold white]The report is complete.[/bold white]

[cyan]git blame[/cyan] on the contested algorithm: every critical line last touched by
commit [yellow]a3f9c21[/yellow], authored by the plaintiff, dated fourteen months before
her hire date, when she was working on a personal project hosted on her own account.

[cyan]git log --follow[/cyan] traced the file through three renames. Same content.
Same authorship. Different filename, different directory, same code.

[cyan]git bisect[/cyan] found the exact commit where it entered the corporate repository:
pushed from an IP address that resolved to the corp's main office, by an account
that was not the plaintiff's.

Forty-eight hours. One repository. [bold white]Thirty-seven exhibits.[/bold white]

[bold magenta]The git history doesn't lie. It just waits for someone who knows how to read it.[/bold magenta]

[bold yellow]TIMELINE AUDITOR STATUS: GRANDMASTER.  CASE STATUS: RESOLVED.[/bold yellow]
""",
}

BOSS_INTROS = {
    "origin_vault": "[bold red]⚠  REPOSITORY AUDIT: The Origin Trace[/bold red]\nThe defense wants to challenge whether this is even the original repository. Prove you understand what a git repo is — from the inside.",
    "staging_area": "[bold red]⚠  EVIDENCE REVIEW: The Staging Gauntlet[/bold red]\nThe staging area contains the last uncommitted changes before the account was locked. You need to read exactly what was there.",
    "commit_ledger": "[bold red]⚠  COMMIT ANALYSIS: The Log Interrogation[/bold red]\nFifty commits. Three of them are the ones that matter. Find them — using git log flags that expose exactly what you need.",
    "branch_matrix": "[bold red]⚠  BRANCH RECOVERY: The Deleted Timeline[/bold red]\nA deleted branch. A commit that shouldn't exist. Prove you can navigate the branch structure well enough to find it.",
    "merge_protocol": "[bold red]⚠  MERGE FORENSICS: The Fast-Forward Cover[/bold red]\nThe merge left no merge commit. The branch is gone. But the commits are still there if you know where to look.",
    "rebase_engine": "[bold red]⚠  REBASE ANALYSIS: The Rewritten History[/bold red]\nSomeone ran git rebase -i and called it cleanup. Prove you understand exactly what that does to the commit graph.",
    "remote_network": "[bold red]⚠  FORCE PUSH DETECTION: The Remote Audit[/bold red]\nA 2:47 AM force push. Reconstructing what the remote looked like before requires understanding how remotes actually work.",
    "recovery_vault": "[bold red]⚠  REFLOG EXCAVATION: The Ghost History[/bold red]\nThe reflog is 63 days old. The entries are still there. Extract the original commit hashes before garbage collection runs.",
    "forensics_chamber": "[bold red]★  FINAL ANALYSIS: The Blame Audit[/bold red]\nEvery line of the contested algorithm. Every commit in its history. One command surfaces who actually wrote it, and when.",
}

ACHIEVEMENT_DESCRIPTIONS = {
    "first_blood": ("First Commit Read", "Read your first git object. The ledger acknowledged your presence."),
    "navigator": ("Repository Mapped", "Cleared the Origin Vault. You know what a .git directory actually is."),
    "archivist": ("Staging Expert", "Cleared the Staging Area. git add, git status, git diff — you read the intent before it becomes record."),
    "seeker": ("Commit Historian", "Cleared the Commit Ledger. Every log entry, every diff, every author claim — you can read them all."),
    "pipe_dream": ("Branch Architect", "Cleared the Branch Matrix. Branches are pointers. You know what they point to, and what they used to point to."),
    "necromancer": ("Merge Analyst", "Cleared the Merge Protocol. Fast-forward, three-way merge, merge commit — you know what each one hides."),
    "warden": ("Rebase Decoder", "Cleared the Rebase Engine. Squash, fixup, reword — history rewriting is no longer invisible to you."),
    "scriptor": ("Remote Auditor", "Cleared the Remote Network. fetch, pull, push, force push — you know what hits the remote and what it overwrites."),
    "networked": ("Reflog Archaeologist", "Cleared the Recovery Vault. The reflog is your primary source. Nothing stays deleted for 90 days."),
    "grandmaster": ("TIMELINE AUDITOR: GRANDMASTER", "Cleared the Forensics Chamber. git blame, git bisect, git log --follow. The case is closed. The history doesn't lie."),
    "streak_3": ("Commit Streak", "3 correct in a row. Your git knowledge is starting to flow."),
    "streak_5": ("Clean History", "5 in a row. Your understanding of git is as clean as a well-maintained commit graph."),
    "streak_10": ("REBASE MASTER", "10 in a row. You could rewrite this history yourself. You choose not to."),
    "no_hints": ("No Hints Needed", "Cleared a zone without hints. The documentation is in your head now."),
    "speed_demon": ("Sub-5 Commit", "Answered in under 5 seconds. The command was already there before you finished reading."),
    "level_10": ("Junior Auditor", "Level 10. git log is starting to look like a story, not a list."),
    "level_20": ("Senior Auditor", "Level 20. You read reflog entries like other people read email."),
    "level_30": ("Master Auditor", "Maximum level. You understand git from object model to reflog. Courts have accepted your testimony."),
    "completionist": ("Full Audit Complete", "Every zone. Every challenge. Total repository forensics achieved."),
    "boss_slayer": ("Defense Overruled", "Beat your first boss challenge. The defense attorney's argument didn't survive contact with git log."),
}
