"""
zones.py - All zone and challenge data for Git Quest
Challenge types: quiz, flag_quiz, fill_blank, live
"""

ZONES = {
    "origin_vault": {
        "id": "origin_vault",
        "name": "The Origin Vault",
        "subtitle": "Init, Clone & Config",
        "color": "cyan",
        "icon": "🔐",
        "commands": ["git init", "git clone", "git config", "git status"],
        "challenges": [
            {
                "id": "orig_1",
                "type": "quiz",
                "title": "Open the Ledger",
                "flavor": "The repository doesn't exist yet. You need to create the ledger from scratch. What command initializes a new git repository in the current directory?",
                "lesson": (
                    "git init — initializes a new git repository in the current directory.\n\n"
                    "Creates a hidden .git/ subdirectory containing:\n"
                    "  objects/   all commit, tree, and blob objects\n"
                    "  refs/      branch and tag pointers\n"
                    "  HEAD       pointer to the current branch\n"
                    "  config     repository-level configuration\n\n"
                    "Syntax: git init [directory]\n"
                    "  Omit directory to init the current directory.\n\n"
                    "Example: git init    → creates .git/ in the current directory"
                ),
                "question": "What command creates a new git repository in the current directory?",
                "answers": ["git init", "init"],
                "xp": 50,
                "difficulty": "easy",
                "hints": [
                    "Think: initialize.",
                    "It's two words: git and a verb.",
                    "The answer is: git init",
                ],
            },
            {
                "id": "orig_2",
                "type": "quiz",
                "title": "Copy the Repository",
                "flavor": "The repository exists on a remote server. You need a local copy — the complete history, all branches, all commits. What command does that?",
                "lesson": (
                    "git clone — creates a complete local copy of a remote repository.\n\n"
                    "Cloning downloads:\n"
                    "  - All commits and their objects\n"
                    "  - All branches (as remote-tracking branches)\n"
                    "  - All tags\n"
                    "  - The full .git/ directory\n\n"
                    "Syntax: git clone <url> [directory]\n\n"
                    "Example: git clone https://github.com/org/repo.git\n"
                    "  → creates a 'repo' directory with the full history"
                ),
                "question": "What git command creates a complete local copy of a remote repository?",
                "answers": ["git clone", "clone"],
                "xp": 50,
                "difficulty": "easy",
                "hints": [
                    "Think: making a copy — like cloning.",
                    "The answer is: git clone",
                ],
            },
            {
                "id": "orig_3",
                "type": "quiz",
                "title": "Identify the Author",
                "flavor": "Every commit records who made it. The author field is critical forensic data — and it's set by configuration, not by authentication. What command manages git configuration?",
                "lesson": (
                    "git config — reads and writes git configuration values.\n\n"
                    "The three config levels (each overrides the one above):\n"
                    "  --system   /etc/gitconfig (all users on this machine)\n"
                    "  --global   ~/.gitconfig (your user account)\n"
                    "  --local    .git/config (this repository only)\n\n"
                    "Critical settings:\n"
                    "  git config --global user.name 'Your Name'\n"
                    "  git config --global user.email 'you@example.com'\n\n"
                    "These values appear in EVERY commit you make.\n"
                    "They are NOT verified against any authentication system.\n\n"
                    "Example: git config --list    → shows all active config values"
                ),
                "question": "What git command sets configuration values like user name and email?",
                "answers": ["git config", "config"],
                "xp": 75,
                "difficulty": "easy",
                "hints": [
                    "Think: configuration.",
                    "The answer is: git config",
                ],
            },
            {
                "id": "orig_4",
                "type": "live",
                "title": "Initialize the Investigation",
                "flavor": "The working directory is clean. You need to start tracking it. Initialize a git repository here.",
                "lesson": (
                    "git init — creates a .git/ directory and begins tracking the current directory.\n\n"
                    "After git init:\n"
                    "  - The directory becomes a git repository\n"
                    "  - git status will show all untracked files\n"
                    "  - No commits exist yet (nothing in the history)\n\n"
                    "Example: git init    → creates .git/ and outputs 'Initialized empty Git repository'"
                ),
                "question": "Initialize a git repository in the current sandbox directory.",
                "setup": {"files": {}, "dirs": []},
                "validation": {
                    "type": "dir_exists",
                    "target": ".git",
                },
                "xp": 100,
                "difficulty": "medium",
                "hints": [
                    "The command is: git init",
                    "It creates a .git directory.",
                    "The answer is: git init",
                ],
            },
            {
                "id": "orig_5",
                "type": "flag_quiz",
                "title": "Read the Configuration",
                "flavor": "You need to see all active configuration values for this repository — name, email, everything. Which flag lists all config entries?",
                "lesson": (
                    "git config --list — displays all configuration values currently in effect.\n\n"
                    "Shows values from all three config levels, merged and deduplicated.\n"
                    "Lower-level config overrides higher-level (local > global > system).\n\n"
                    "Other useful git config flags:\n"
                    "  --global    operate on the global (~/.gitconfig) config\n"
                    "  --local     operate on the repository's config\n"
                    "  --show-origin   show which file each setting comes from\n\n"
                    "Example: git config --list    → prints all key=value config pairs"
                ),
                "question": "What flag shows ALL configuration values currently in effect?",
                "answers": ["--list", "-l", "--list --show-origin"],
                "xp": 75,
                "difficulty": "easy",
                "hints": [
                    "It lists everything.",
                    "Think: --list",
                    "The answer is: --list",
                ],
            },
            {
                "id": "orig_boss",
                "type": "live",
                "title": "BOSS: First Commit in Evidence",
                "flavor": "Initialize the repository, configure the author identity, create a file called 'evidence.txt', stage it, and make the first commit. The ledger opens with this entry.",
                "lesson": (
                    "The complete workflow to make the first commit:\n\n"
                    "  git init                              initialize the repo\n"
                    "  git config user.email 'a@b.com'      set author email (local)\n"
                    "  echo 'content' > evidence.txt         create a file\n"
                    "  git add evidence.txt                  stage the file\n"
                    "  git commit -m 'Initial commit'        create the commit\n\n"
                    "The -m flag provides the commit message inline.\n"
                    "Without -m, git opens a text editor for the message."
                ),
                "question": (
                    "Multi-step: initialize a repo, create 'evidence.txt' with any content,\n"
                    "stage it, and commit it with the message 'Initial commit'.\n\n"
                    "Use && to chain the commands."
                ),
                "setup": {"files": {}, "dirs": []},
                "validation": {
                    "type": "dir_exists",
                    "target": ".git",
                },
                "xp": 200,
                "difficulty": "boss",
                "is_boss": True,
                "hints": [
                    "You need: git init, then create a file, then git add, then git commit -m",
                    "Chain with &&: git init && echo 'data' > evidence.txt && git add evidence.txt && git commit -m 'Initial commit'",
                    "Full command: git init && git config user.email 'audit@case.com' && echo 'evidence' > evidence.txt && git add evidence.txt && git commit -m 'Initial commit'",
                ],
            },
        ],
    },

    "staging_area": {
        "id": "staging_area",
        "name": "The Staging Area",
        "subtitle": "Add, Status & Diff",
        "color": "yellow",
        "icon": "📋",
        "commands": ["git add", "git status", "git diff", "git restore", ".gitignore"],
        "challenges": [
            {
                "id": "stage_1",
                "type": "quiz",
                "title": "Stage the Evidence",
                "flavor": "You've modified a file. The change exists in the working directory but hasn't been staged for commit yet. What command moves it to the staging area?",
                "lesson": (
                    "git add — stages changes for the next commit.\n\n"
                    "Git's three-layer model:\n"
                    "  Working directory   your actual files (untracked/modified)\n"
                    "  Staging area        changes selected for the next commit\n"
                    "  Repository          committed history\n\n"
                    "Syntax:\n"
                    "  git add filename         stage a specific file\n"
                    "  git add .                stage all changes in current directory\n"
                    "  git add -p               interactive: stage changes chunk by chunk\n\n"
                    "Example: git add report.txt    → stages report.txt for the next commit"
                ),
                "question": "What command stages changes to be included in the next commit?",
                "answers": ["git add", "add"],
                "xp": 50,
                "difficulty": "easy",
                "hints": [
                    "Think: adding to the staging area.",
                    "The answer is: git add",
                ],
            },
            {
                "id": "stage_2",
                "type": "quiz",
                "title": "Read the State",
                "flavor": "You need to know what's tracked, what's staged, what's modified, what's untracked. One command gives you the full picture of the working tree state.",
                "lesson": (
                    "git status — shows the state of the working directory and staging area.\n\n"
                    "Output sections:\n"
                    "  'Changes to be committed'      staged files (will be in next commit)\n"
                    "  'Changes not staged for commit' modified tracked files, not yet staged\n"
                    "  'Untracked files'               files git doesn't know about\n\n"
                    "Useful flags:\n"
                    "  git status -s    short format (compact, machine-readable)\n"
                    "  git status -b    include branch information\n\n"
                    "Example: git status    → complete working tree status"
                ),
                "question": "What command shows the current state of the working directory and staging area?",
                "answers": ["git status", "status"],
                "xp": 50,
                "difficulty": "easy",
                "hints": [
                    "Think: what's the current status?",
                    "The answer is: git status",
                ],
            },
            {
                "id": "stage_3",
                "type": "quiz",
                "title": "See the Changes",
                "flavor": "A file was modified. Before staging it, you need to see exactly what changed — line by line. What command shows the diff between the working directory and the staging area?",
                "lesson": (
                    "git diff — shows line-by-line differences between versions.\n\n"
                    "Common uses:\n"
                    "  git diff              working directory vs staging area (unstaged changes)\n"
                    "  git diff --staged     staging area vs last commit (what will be committed)\n"
                    "  git diff HEAD         working directory vs last commit (all changes)\n"
                    "  git diff commit1 commit2   between two specific commits\n\n"
                    "Output format:\n"
                    "  Lines starting with -   removed\n"
                    "  Lines starting with +   added\n\n"
                    "Example: git diff report.txt    → shows unstaged changes in report.txt"
                ),
                "question": "What command shows line-by-line differences between the working directory and the staging area?",
                "answers": ["git diff", "diff"],
                "xp": 75,
                "difficulty": "easy",
                "hints": [
                    "Think: differences.",
                    "The answer is: git diff",
                ],
            },
            {
                "id": "stage_4",
                "type": "fill_blank",
                "title": "See What's Staged",
                "flavor": "You've staged some changes. You want to see exactly what's in the staging area — what will actually go into the next commit. Which flag shows staged changes?",
                "lesson": (
                    "git diff --staged — shows the difference between the staging area and the last commit.\n\n"
                    "This is what will be committed if you run git commit right now.\n"
                    "Also called: git diff --cached (both flags are equivalent)\n\n"
                    "Why this matters forensically:\n"
                    "  git diff          shows what's NOT staged (might be misleading)\n"
                    "  git diff --staged shows what IS staged (what enters the record)\n\n"
                    "Example: git diff --staged    → exactly what the next commit will contain"
                ),
                "question": "Complete this command to see changes that are staged for commit:\n\ngit diff ___",
                "answers": ["--staged", "--cached"],
                "xp": 100,
                "difficulty": "medium",
                "hints": [
                    "It's a flag that means 'show staged changes'.",
                    "Think: staged. Or cached.",
                    "The answer is: --staged",
                ],
            },
            {
                "id": "stage_5",
                "type": "live",
                "title": "Stage a File",
                "flavor": "The file 'findings.txt' exists and has been modified. Stage it for the next commit.",
                "lesson": (
                    "git add <filename> — stages a specific file.\n\n"
                    "Only the file you name gets staged. Other modified files stay unstaged.\n"
                    "This is the precise approach — surgical, auditable, intentional.\n\n"
                    "After git add, verify with: git status\n"
                    "You should see 'findings.txt' under 'Changes to be committed'.\n\n"
                    "Example: git add findings.txt    → stages findings.txt"
                ),
                "question": "Stage the file 'findings.txt' for the next commit.",
                "setup": {
                    "files": {"findings.txt": "Case findings: anomalous commit timestamps detected.\n"},
                    "dirs": [],
                },
                "validation": {
                    "type": "command_output_contains",
                    "command": "git status",
                    "expected": "findings.txt",
                },
                "xp": 100,
                "difficulty": "medium",
                "hints": [
                    "Use git add with the filename.",
                    "Try: git add findings.txt",
                    "The answer is: git add findings.txt",
                ],
            },
            {
                "id": "stage_boss",
                "type": "live",
                "title": "BOSS: Precision Staging",
                "flavor": "Three files exist: 'evidence.txt', 'scratch.txt', and 'notes.txt'. Stage ONLY 'evidence.txt' — scratch.txt and notes.txt must remain unstaged. The integrity of the staging area matters.",
                "lesson": (
                    "Selective staging — stage specific files, not all changes:\n\n"
                    "  git add evidence.txt    stages only evidence.txt\n"
                    "  git add .               stages EVERYTHING (dangerous if you're not careful)\n\n"
                    "After selective staging:\n"
                    "  git status    should show evidence.txt under 'Changes to be committed'\n"
                    "                and scratch.txt, notes.txt under 'Untracked files'\n\n"
                    "In forensic work: staging everything indiscriminately means\n"
                    "you're committing things you haven't reviewed. That's how\n"
                    "sensitive data ends up in the history."
                ),
                "question": (
                    "Three files exist. Stage ONLY 'evidence.txt'.\n"
                    "Do NOT stage scratch.txt or notes.txt."
                ),
                "setup": {
                    "files": {
                        "evidence.txt": "PRIMARY EVIDENCE\n",
                        "scratch.txt": "working notes\n",
                        "notes.txt": "temp notes\n",
                    },
                    "dirs": [],
                },
                "validation": {
                    "type": "command_output_contains",
                    "command": "git status",
                    "expected": "evidence.txt",
                },
                "xp": 200,
                "difficulty": "boss",
                "is_boss": True,
                "hints": [
                    "Stage only the specific file you want.",
                    "git add evidence.txt  — not git add .",
                    "The answer is: git add evidence.txt",
                ],
            },
        ],
    },

    "commit_ledger": {
        "id": "commit_ledger",
        "name": "The Commit Ledger",
        "subtitle": "Commit, Log & Show",
        "color": "magenta",
        "icon": "📜",
        "commands": ["git commit", "git log", "git show", "git diff HEAD"],
        "challenges": [
            {
                "id": "commit_1",
                "type": "quiz",
                "title": "Seal the Record",
                "flavor": "The staging area is ready. The changes are reviewed. One command seals them into a permanent commit — a cryptographic record of this exact state. What is it?",
                "lesson": (
                    "git commit — records staged changes as a new commit in the history.\n\n"
                    "Each commit contains:\n"
                    "  - A snapshot of all staged changes\n"
                    "  - Author name and email\n"
                    "  - Committer name and email\n"
                    "  - Timestamp (authored and committed)\n"
                    "  - Commit message\n"
                    "  - Pointer to parent commit(s)\n"
                    "  - A SHA-1 hash of all the above\n\n"
                    "Syntax:\n"
                    "  git commit -m 'message'    commit with inline message\n"
                    "  git commit                 opens editor for message\n"
                    "  git commit --amend         modify the last commit\n\n"
                    "Example: git commit -m 'Add forensic analysis report'"
                ),
                "question": "What command creates a new commit from staged changes?",
                "answers": ["git commit", "commit"],
                "xp": 50,
                "difficulty": "easy",
                "hints": [
                    "Think: committing to the record.",
                    "The answer is: git commit",
                ],
            },
            {
                "id": "commit_2",
                "type": "quiz",
                "title": "Read the History",
                "flavor": "The ledger has fifty commits. You need to read them — author, timestamp, message, hash. Which command shows the commit history?",
                "lesson": (
                    "git log — displays the commit history.\n\n"
                    "Default output: hash, author, date, message — newest first.\n\n"
                    "Useful flags:\n"
                    "  --oneline          compact: hash + message only\n"
                    "  --graph            ASCII art branch graph\n"
                    "  --all              include all branches and tags\n"
                    "  --author='name'    filter by author\n"
                    "  --since='date'     commits after a date\n"
                    "  --until='date'     commits before a date\n"
                    "  -p                 show the diff for each commit\n"
                    "  --stat             show file change statistics\n\n"
                    "Example: git log --oneline --graph --all"
                ),
                "question": "What command shows the git commit history?",
                "answers": ["git log", "log"],
                "xp": 50,
                "difficulty": "easy",
                "hints": [
                    "Think: the log of what happened.",
                    "The answer is: git log",
                ],
            },
            {
                "id": "commit_3",
                "type": "flag_quiz",
                "title": "Compact the Log",
                "flavor": "50 commits, full output. You need just the hash and message for each — one line per commit. Which flag produces that?",
                "lesson": (
                    "git log --oneline — shows each commit as a single line: short hash + message.\n\n"
                    "The short hash is the first 7 characters of the full SHA-1.\n"
                    "It's unique within the repository (almost always).\n\n"
                    "Combine for maximum forensic readability:\n"
                    "  git log --oneline --graph --all --decorate\n\n"
                    "  --graph     shows branch/merge structure as ASCII art\n"
                    "  --all       shows commits from ALL branches, not just current\n"
                    "  --decorate  shows branch and tag labels on commits\n\n"
                    "Example: git log --oneline    → compact, one-per-line history"
                ),
                "question": "Which git log flag shows each commit on a single line (short hash + message)?",
                "answers": ["--oneline", "--one-line", "-1"],
                "xp": 75,
                "difficulty": "easy",
                "hints": [
                    "Think: one line.",
                    "The answer is: --oneline",
                ],
            },
            {
                "id": "commit_4",
                "type": "quiz",
                "title": "Inspect the Commit",
                "flavor": "You have a commit hash. You need to see exactly what that commit changed — full diff, author, timestamp, message. One command opens any commit by its hash.",
                "lesson": (
                    "git show — displays a commit's metadata and full diff.\n\n"
                    "Syntax:\n"
                    "  git show                shows the most recent commit\n"
                    "  git show <hash>         shows a specific commit\n"
                    "  git show <hash>:file    shows a file as it was in that commit\n\n"
                    "Output includes:\n"
                    "  - Full commit hash, author, date, message\n"
                    "  - Complete diff (all changed files, all changed lines)\n\n"
                    "Forensic use: git show <hash> gives you exactly what someone\n"
                    "committed, when, and under what claimed identity.\n\n"
                    "Example: git show a3f9c21    → full details of commit a3f9c21"
                ),
                "question": "What command shows the full details and diff of a specific commit?",
                "answers": ["git show", "show"],
                "xp": 75,
                "difficulty": "easy",
                "hints": [
                    "Think: show me this commit.",
                    "The answer is: git show",
                ],
            },
            {
                "id": "commit_5",
                "type": "fill_blank",
                "title": "Commit with a Message",
                "flavor": "The files are staged. The commit needs a message. Which flag lets you provide it inline without opening an editor?",
                "lesson": (
                    "git commit -m 'message' — creates a commit with an inline message.\n\n"
                    "Without -m, git opens your $EDITOR (vim, nano, etc.) for the message.\n"
                    "With -m, you provide it directly in the command.\n\n"
                    "Good commit messages:\n"
                    "  - Short summary (50 chars or less) on the first line\n"
                    "  - Imperative mood: 'Add feature' not 'Added feature'\n"
                    "  - Describe WHY, not just WHAT\n\n"
                    "Example: git commit -m 'Add forensic analysis of commit a3f9c21'"
                ),
                "question": "Complete this command to commit with an inline message:\n\ngit commit ___ 'Add analysis results'",
                "answers": ["-m", "--message"],
                "xp": 75,
                "difficulty": "easy",
                "hints": [
                    "It's a single flag that provides the message.",
                    "Think: -m for message.",
                    "The answer is: -m",
                ],
            },
            {
                "id": "commit_boss",
                "type": "live",
                "title": "BOSS: Commit the Findings",
                "flavor": "Stage 'report.txt' and commit it with the message 'Add forensic report'. The commit message is evidence — it needs to be exact.",
                "lesson": (
                    "The complete stage-and-commit workflow:\n\n"
                    "  git add report.txt\n"
                    "  git commit -m 'Add forensic report'\n\n"
                    "Or in one line with &&:\n"
                    "  git add report.txt && git commit -m 'Add forensic report'\n\n"
                    "After committing, verify with:\n"
                    "  git log --oneline    → should show your new commit at the top"
                ),
                "question": (
                    "Stage 'report.txt' and commit it with the message 'Add forensic report'.\n"
                    "The .git directory already exists (repo is initialized)."
                ),
                "setup": {
                    "files": {"report.txt": "FORENSIC ANALYSIS REPORT\nCase: #4471-B\nStatus: Evidence of tampering found.\n"},
                    "dirs": [],
                },
                "validation": {
                    "type": "dir_exists",
                    "target": ".git",
                },
                "xp": 200,
                "difficulty": "boss",
                "is_boss": True,
                "hints": [
                    "Two commands: git add report.txt, then git commit -m '...'",
                    "Try: git add report.txt && git commit -m 'Add forensic report'",
                    "Full: git add report.txt && git commit -m 'Add forensic report'",
                ],
            },
        ],
    },

    "branch_matrix": {
        "id": "branch_matrix",
        "name": "The Branch Matrix",
        "subtitle": "Branching & Navigation",
        "color": "blue",
        "icon": "🌿",
        "commands": ["git branch", "git switch", "git checkout", "git log --all"],
        "challenges": [
            {
                "id": "branch_1",
                "type": "quiz",
                "title": "List the Branches",
                "flavor": "Seventeen branches. Three deleted. You need to see what currently exists. Which command lists all local branches?",
                "lesson": (
                    "git branch — lists, creates, renames, or deletes branches.\n\n"
                    "Common usages:\n"
                    "  git branch              list local branches\n"
                    "  git branch -a           list local AND remote-tracking branches\n"
                    "  git branch -r           list remote-tracking branches only\n"
                    "  git branch feature      create a branch called 'feature'\n"
                    "  git branch -d feature   delete branch 'feature' (safe)\n"
                    "  git branch -D feature   force delete (even if unmerged)\n\n"
                    "The current branch is marked with *\n\n"
                    "Example: git branch -a    → lists all branches including remote ones"
                ),
                "question": "What command lists all local git branches?",
                "answers": ["git branch", "branch"],
                "xp": 50,
                "difficulty": "easy",
                "hints": [
                    "Think: branch.",
                    "The answer is: git branch",
                ],
            },
            {
                "id": "branch_2",
                "type": "quiz",
                "title": "Switch the Timeline",
                "flavor": "You're on main. The evidence is on a branch called 'feature/auth'. You need to move there — switch your working directory to that branch.",
                "lesson": (
                    "git switch — moves to a different branch.\n\n"
                    "Syntax:\n"
                    "  git switch <branch>         switch to an existing branch\n"
                    "  git switch -c <branch>      create and switch to a new branch\n"
                    "  git switch -               switch back to the previous branch\n\n"
                    "git switch was introduced in Git 2.23 as a clearer alternative to:\n"
                    "  git checkout <branch>    (the older equivalent)\n\n"
                    "Both work. git switch is preferred for branch operations.\n"
                    "git checkout retains more power (e.g., restoring files).\n\n"
                    "Example: git switch feature/auth    → switches to the feature/auth branch"
                ),
                "question": "What modern git command switches to a different branch?",
                "answers": ["git switch", "switch", "git checkout", "checkout"],
                "xp": 50,
                "difficulty": "easy",
                "hints": [
                    "Think: switching branches.",
                    "The answer is: git switch (or git checkout)",
                ],
            },
            {
                "id": "branch_3",
                "type": "flag_quiz",
                "title": "Create and Move",
                "flavor": "You need a new branch called 'audit/timeline' and you want to switch to it immediately. What flag creates and switches in one command?",
                "lesson": (
                    "git switch -c <name> — creates a new branch and immediately switches to it.\n\n"
                    "Equivalent to:\n"
                    "  git branch audit/timeline\n"
                    "  git switch audit/timeline\n\n"
                    "With git checkout (older syntax):\n"
                    "  git checkout -b audit/timeline\n\n"
                    "Branch names:\n"
                    "  Can contain letters, numbers, /, -, _\n"
                    "  Cannot contain spaces, .., @{, \\, ^, ~, :, ?\n"
                    "  Convention: feature/name, fix/issue, audit/subject\n\n"
                    "Example: git switch -c audit/timeline    → creates and switches"
                ),
                "question": "What flag creates a new branch and switches to it in one git switch command?",
                "answers": ["-c", "-C", "-b"],
                "xp": 75,
                "difficulty": "easy",
                "hints": [
                    "Think: create.",
                    "The answer is: -c",
                ],
            },
            {
                "id": "branch_4",
                "type": "flag_quiz",
                "title": "See All Branches",
                "flavor": "The remote has branches the local copy doesn't show by default. Which git branch flag shows ALL branches — local AND remote-tracking?",
                "lesson": (
                    "git branch -a — lists all branches: local and remote-tracking.\n\n"
                    "Remote-tracking branches are local copies of remote branches:\n"
                    "  origin/main\n"
                    "  origin/feature/auth\n"
                    "  origin/release/v2\n\n"
                    "They update when you run git fetch.\n"
                    "They show what the remote looked like at the last fetch.\n\n"
                    "Other flags:\n"
                    "  git branch -r    remote-tracking branches only\n"
                    "  git branch -v    show last commit on each branch\n"
                    "  git branch -vv   show tracking relationship to remote\n\n"
                    "Example: git branch -a    → complete branch inventory"
                ),
                "question": "Which git branch flag shows ALL branches (local and remote-tracking)?",
                "answers": ["-a", "--all", "-r -l", "-v"],
                "xp": 75,
                "difficulty": "easy",
                "hints": [
                    "Think: all.",
                    "The answer is: -a",
                ],
            },
            {
                "id": "branch_boss",
                "type": "live",
                "title": "BOSS: Navigate the Matrix",
                "flavor": "Create a branch called 'audit/findings' and switch to it. The investigation needs its own timeline.",
                "lesson": (
                    "Create and switch to a new branch:\n\n"
                    "  git switch -c audit/findings\n\n"
                    "Or using the older syntax:\n"
                    "  git checkout -b audit/findings\n\n"
                    "Verify you're on the new branch:\n"
                    "  git branch    → should show * audit/findings\n\n"
                    "The new branch starts at the same commit as the branch you were on."
                ),
                "question": "Create a branch called 'audit/findings' and switch to it.",
                "setup": {"files": {}, "dirs": []},
                "validation": {
                    "type": "dir_exists",
                    "target": ".git",
                },
                "xp": 200,
                "difficulty": "boss",
                "is_boss": True,
                "hints": [
                    "Use git switch -c to create and switch.",
                    "Try: git switch -c audit/findings",
                    "Or: git checkout -b audit/findings",
                ],
            },
        ],
    },

    "merge_protocol": {
        "id": "merge_protocol",
        "name": "The Merge Protocol",
        "subtitle": "Merging & Conflicts",
        "color": "green",
        "icon": "🔀",
        "commands": ["git merge", "git merge --no-ff", "git log --graph", "conflict resolution"],
        "challenges": [
            {
                "id": "merge_1",
                "type": "quiz",
                "title": "Converge the Timelines",
                "flavor": "A feature branch is ready to be integrated into main. Which command combines branch histories?",
                "lesson": (
                    "git merge <branch> — integrates commits from another branch into the current branch.\n\n"
                    "Two merge scenarios:\n\n"
                    "Fast-forward merge:\n"
                    "  - Occurs when the current branch hasn't diverged from the target\n"
                    "  - The branch pointer simply moves forward\n"
                    "  - NO merge commit is created\n"
                    "  - The history looks linear (no evidence a branch existed)\n\n"
                    "3-way merge:\n"
                    "  - Occurs when both branches have new commits\n"
                    "  - Creates a merge commit with TWO parents\n"
                    "  - The history shows the branch and when it was merged\n\n"
                    "Example: git merge feature/auth    → merges feature/auth into current branch"
                ),
                "question": "What command integrates commits from another branch into the current branch?",
                "answers": ["git merge", "merge"],
                "xp": 50,
                "difficulty": "easy",
                "hints": [
                    "Think: merging two branches.",
                    "The answer is: git merge",
                ],
            },
            {
                "id": "merge_2",
                "type": "quiz",
                "title": "The Merge Commit",
                "flavor": "A fast-forward merge leaves no record of when the branch was merged. Which flag forces a merge commit even when fast-forward is possible — preserving the evidence?",
                "lesson": (
                    "git merge --no-ff — forces a merge commit even when fast-forward is possible.\n\n"
                    "Why this matters:\n"
                    "  Default fast-forward:  history looks linear, no record of branch\n"
                    "  --no-ff merge:         creates a merge commit with 2 parents,\n"
                    "                         records exactly when and what was merged\n\n"
                    "Forensically:\n"
                    "  Fast-forward + branch delete = 'this code was always on main'\n"
                    "  --no-ff merge          = clear record of branch and merge point\n\n"
                    "Use --no-ff for important features, releases, and anything where\n"
                    "the merge event itself is part of the record.\n\n"
                    "Example: git merge --no-ff feature/auth    → always creates a merge commit"
                ),
                "question": "Which git merge flag forces a merge commit, preventing fast-forward?",
                "answers": ["--no-ff", "--no-fast-forward"],
                "xp": 100,
                "difficulty": "medium",
                "hints": [
                    "It prevents fast-forward.",
                    "The flag starts with --no",
                    "The answer is: --no-ff",
                ],
            },
            {
                "id": "merge_3",
                "type": "quiz",
                "title": "Conflict Resolution",
                "flavor": "The merge stopped. Git found the same lines modified in both branches. It can't decide which version is correct. What's the state of the repository right now?",
                "lesson": (
                    "Merge conflicts — occur when the same lines are changed in both branches.\n\n"
                    "During a conflict, git halts the merge and marks conflicted files:\n\n"
                    "  <<<<<<< HEAD\n"
                    "  current branch version\n"
                    "  =======\n"
                    "  incoming branch version\n"
                    "  >>>>>>> feature/auth\n\n"
                    "Resolution steps:\n"
                    "  1. Edit the conflicted files (remove markers, keep the correct content)\n"
                    "  2. git add <resolved_file>    mark as resolved\n"
                    "  3. git commit                 complete the merge\n\n"
                    "Or abort: git merge --abort    returns to pre-merge state"
                ),
                "question": "When git can't automatically resolve differing changes to the same lines, what is this called?",
                "answers": ["merge conflict", "conflict", "a conflict", "merge conflicts"],
                "xp": 75,
                "difficulty": "medium",
                "hints": [
                    "It happens when both branches changed the same lines.",
                    "Git marks the conflicting sections in the file.",
                    "The answer is: merge conflict",
                ],
            },
            {
                "id": "merge_4",
                "type": "flag_quiz",
                "title": "Visualize the Graph",
                "flavor": "You need to see the branch structure — where branches diverged, where they merged, which commits have two parents. Which git log flag draws the commit graph?",
                "lesson": (
                    "git log --graph — draws an ASCII art representation of the branch and merge history.\n\n"
                    "Best used with additional flags:\n"
                    "  git log --graph --oneline --all --decorate\n\n"
                    "The graph shows:\n"
                    "  * single-parent commits\n"
                    "  |\\  branch point (diverging)\n"
                    "  |/  merge point (converging)\n\n"
                    "Forensically critical: the graph reveals fast-forwards\n"
                    "(no branch/merge symbols) vs proper merges (branch + merge symbols).\n\n"
                    "Example: git log --graph --oneline --all    → full branch visualization"
                ),
                "question": "Which git log flag shows the commit history as an ASCII branch graph?",
                "answers": ["--graph", "--graph --oneline", "--graph --oneline --all"],
                "xp": 75,
                "difficulty": "easy",
                "hints": [
                    "Think: draw the graph.",
                    "The answer is: --graph",
                ],
            },
            {
                "id": "merge_boss",
                "type": "fill_blank",
                "title": "BOSS: Force the Evidence Trail",
                "flavor": "You're merging 'feature/contested' into main. A fast-forward would erase the record of when this code was integrated. Force a merge commit — preserve the evidence.",
                "lesson": (
                    "Force a merge commit even when fast-forward is possible:\n\n"
                    "  git merge --no-ff feature/contested\n\n"
                    "This creates a commit with TWO parent pointers:\n"
                    "  Parent 1: last commit on main before the merge\n"
                    "  Parent 2: last commit on feature/contested\n\n"
                    "The result is visible in git log --graph as a merge node.\n"
                    "It records exactly when the code entered the main branch.\n"
                    "It cannot be quietly removed without changing the commit hash."
                ),
                "question": "Complete this merge command to force a merge commit:\n\ngit merge ___ feature/contested",
                "answers": ["--no-ff", "--no-fast-forward"],
                "xp": 200,
                "difficulty": "boss",
                "is_boss": True,
                "hints": [
                    "You want to prevent fast-forward.",
                    "The flag starts with --no.",
                    "The answer is: --no-ff",
                ],
            },
        ],
    },

    "rebase_engine": {
        "id": "rebase_engine",
        "name": "The Rebase Engine",
        "subtitle": "Rebase & History Rewriting",
        "color": "red",
        "icon": "⚙️",
        "commands": ["git rebase", "git rebase -i", "squash", "fixup", "reword"],
        "challenges": [
            {
                "id": "rebase_1",
                "type": "quiz",
                "title": "What Rebase Does",
                "flavor": "Someone ran git rebase on a production branch and called it 'cleanup'. What does rebase actually do to commits?",
                "lesson": (
                    "git rebase — replays commits on top of a different base commit.\n\n"
                    "Rebase does NOT move commits. It:\n"
                    "  1. Takes commits from the current branch\n"
                    "  2. Detaches them from their current parent\n"
                    "  3. Replays them on top of the target branch/commit\n"
                    "  4. Creates NEW commits with new SHA-1 hashes\n"
                    "  5. The original commits become orphaned\n\n"
                    "The result looks like a cleaner, linear history.\n"
                    "The original history is destroyed (the commits are new objects).\n\n"
                    "Syntax: git rebase <target>    e.g., git rebase main\n\n"
                    "Golden rule: NEVER rebase commits that have been pushed to a shared remote."
                ),
                "question": "What does git rebase do to commits? What happens to the original commits?",
                "answers": [
                    "creates new commits",
                    "new commits with new hashes",
                    "replays commits as new commits",
                    "destroys and recreates commits",
                    "creates copies with new hashes",
                ],
                "xp": 100,
                "difficulty": "medium",
                "hints": [
                    "Rebase doesn't move commits — it makes new ones.",
                    "Each rebased commit gets a new SHA-1 hash.",
                    "The answer is: creates new commits (with new hashes); originals become orphaned",
                ],
            },
            {
                "id": "rebase_2",
                "type": "quiz",
                "title": "Interactive Rebase",
                "flavor": "The history shows five commits that should have been one. Someone is trying to squash the evidence. What command lets you interactively edit the history?",
                "lesson": (
                    "git rebase -i — interactive rebase; lets you edit, reorder, squash, and drop commits.\n\n"
                    "Syntax: git rebase -i HEAD~n    (last n commits)\n"
                    "        git rebase -i <hash>     (commits since that hash)\n\n"
                    "Interactive actions (edit in the text file git opens):\n"
                    "  pick    keep commit as-is\n"
                    "  reword  keep commit but edit the message\n"
                    "  edit    pause to amend the commit\n"
                    "  squash  combine with previous commit (keep both messages)\n"
                    "  fixup   combine with previous commit (discard this message)\n"
                    "  drop    remove this commit entirely\n\n"
                    "Example: git rebase -i HEAD~5    → interactive editor for last 5 commits"
                ),
                "question": "What flag makes git rebase interactive, allowing you to edit the history?",
                "answers": ["-i", "--interactive", "-i HEAD~"],
                "xp": 100,
                "difficulty": "medium",
                "hints": [
                    "Think: interactive.",
                    "The answer is: -i",
                ],
            },
            {
                "id": "rebase_3",
                "type": "quiz",
                "title": "Squash the Evidence",
                "flavor": "In an interactive rebase, which action combines multiple commits into one — keeping all the messages?",
                "lesson": (
                    "squash vs fixup — two ways to combine commits in interactive rebase:\n\n"
                    "  squash (s)  combine commit with the one above it; keep both messages\n"
                    "  fixup  (f)  combine commit with the one above it; discard this message\n\n"
                    "In the interactive rebase editor:\n"
                    "  pick a1b2c3 First commit\n"
                    "  squash d4e5f6 Second commit    ← combined into 'First commit'\n"
                    "  fixup  g7h8i9 Third commit     ← combined, message discarded\n\n"
                    "Forensically: squash compresses 5 commits into 1,\n"
                    "potentially hiding intermediate work and intermediate authors."
                ),
                "question": "In interactive rebase, which action combines commits while keeping all commit messages?",
                "answers": ["squash", "s"],
                "xp": 75,
                "difficulty": "medium",
                "hints": [
                    "It combines commits and keeps the messages.",
                    "The answer is: squash",
                ],
            },
            {
                "id": "rebase_4",
                "type": "fill_blank",
                "title": "Rebase onto Target",
                "flavor": "You're on a feature branch. You need to replay your commits on top of the latest main. Which command does this?",
                "lesson": (
                    "git rebase main — replays the current branch's commits on top of main.\n\n"
                    "Before rebase:\n"
                    "  main:    A -- B -- C\n"
                    "  feature:      D -- E\n\n"
                    "After git rebase main (while on feature):\n"
                    "  main:    A -- B -- C\n"
                    "  feature:              D' -- E'\n\n"
                    "D' and E' are new commits (new hashes) with C as their base.\n"
                    "The original D and E are orphaned.\n\n"
                    "Then git switch main && git merge feature → fast-forward (linear history)."
                ),
                "question": "Complete this command to rebase the current branch onto main:\n\ngit ___ main",
                "answers": ["rebase", "rebase -i"],
                "xp": 75,
                "difficulty": "easy",
                "hints": [
                    "The command is git rebase.",
                    "The answer is: rebase",
                ],
            },
            {
                "id": "rebase_boss",
                "type": "fill_blank",
                "title": "BOSS: Read the Rewrite",
                "flavor": "The log shows suspiciously round commit timestamps and messages that reference future events. They used interactive rebase. What command would you run to inspect the last 10 commits interactively — without actually changing anything yet?",
                "lesson": (
                    "git rebase -i HEAD~10 — opens the interactive rebase editor for the last 10 commits.\n\n"
                    "You can examine what's there, then quit the editor without saving\n"
                    "to abort without making any changes.\n\n"
                    "HEAD~n notation:\n"
                    "  HEAD      current commit\n"
                    "  HEAD~1    one commit before HEAD (parent)\n"
                    "  HEAD~5    five commits before HEAD\n"
                    "  HEAD~10   ten commits before HEAD\n\n"
                    "This lets you inspect the rebase plan without executing it:\n"
                    "  - Read the commit list and hashes\n"
                    "  - Quit the editor (`:q!` in vim, Ctrl+X in nano without saving)\n"
                    "  - No changes are made"
                ),
                "question": "Complete this command to open interactive rebase for the last 10 commits:\n\ngit rebase -i ___",
                "answers": ["HEAD~10", "HEAD~10 --", "HEAD~10 --no-edit"],
                "xp": 200,
                "difficulty": "boss",
                "is_boss": True,
                "hints": [
                    "You need to reference 10 commits back from HEAD.",
                    "HEAD~N means N commits before HEAD.",
                    "The answer is: HEAD~10",
                ],
            },
        ],
    },

    "remote_network": {
        "id": "remote_network",
        "name": "The Remote Network",
        "subtitle": "Remotes, Fetch & Push",
        "color": "cyan",
        "icon": "🌐",
        "commands": ["git remote", "git fetch", "git pull", "git push", "git push --force"],
        "challenges": [
            {
                "id": "remote_1",
                "type": "quiz",
                "title": "List the Remotes",
                "flavor": "This repository has connections to external servers. Where are they? Which command shows the configured remote repositories?",
                "lesson": (
                    "git remote — manages connections to remote repositories.\n\n"
                    "Common usages:\n"
                    "  git remote -v           list remotes with their URLs (fetch and push)\n"
                    "  git remote add <n> <u>  add a new remote named n at URL u\n"
                    "  git remote remove <n>   remove a remote\n"
                    "  git remote rename <o> <n>  rename a remote\n\n"
                    "The default remote name is 'origin' (set automatically by git clone).\n\n"
                    "Example: git remote -v    → shows origin's fetch and push URLs"
                ),
                "question": "What command lists the configured remote repositories and their URLs?",
                "answers": ["git remote -v", "git remote", "remote -v", "remote"],
                "xp": 50,
                "difficulty": "easy",
                "hints": [
                    "Think: remote repositories.",
                    "The answer is: git remote -v",
                ],
            },
            {
                "id": "remote_2",
                "type": "quiz",
                "title": "Download Without Merging",
                "flavor": "You want to see what changed on the remote without affecting your local working directory. Download the remote state but don't merge anything yet.",
                "lesson": (
                    "git fetch — downloads remote changes without modifying your working directory.\n\n"
                    "What fetch does:\n"
                    "  - Downloads new commits from the remote\n"
                    "  - Updates remote-tracking branches (origin/main, origin/feature)\n"
                    "  - Does NOT change your local branches\n"
                    "  - Does NOT change your working directory\n\n"
                    "After fetch, compare with:\n"
                    "  git log origin/main..main    commits on main not yet on remote\n"
                    "  git log main..origin/main    commits on remote not yet local\n\n"
                    "Example: git fetch origin    → downloads all changes from origin"
                ),
                "question": "Which git command downloads remote changes WITHOUT modifying the local working directory?",
                "answers": ["git fetch", "fetch"],
                "xp": 75,
                "difficulty": "medium",
                "hints": [
                    "It downloads but doesn't merge.",
                    "The answer is: git fetch",
                ],
            },
            {
                "id": "remote_3",
                "type": "quiz",
                "title": "Fetch and Merge",
                "flavor": "You want to download remote changes AND integrate them into your current branch in one step. What command does both?",
                "lesson": (
                    "git pull — fetches from the remote and merges into the current branch.\n\n"
                    "git pull = git fetch + git merge (by default)\n\n"
                    "Variations:\n"
                    "  git pull --rebase    fetch + rebase instead of merge\n"
                    "  git pull origin main fetch from origin's main and merge\n\n"
                    "When to use which:\n"
                    "  git fetch    when you want to inspect before integrating\n"
                    "  git pull     when you trust the remote and want to update fast\n\n"
                    "Forensically: git pull --rebase can rewrite history.\n"
                    "git pull (merge) preserves the full history.\n\n"
                    "Example: git pull    → fetch + merge from the tracked remote"
                ),
                "question": "What command fetches AND merges remote changes into the current branch?",
                "answers": ["git pull", "pull"],
                "xp": 50,
                "difficulty": "easy",
                "hints": [
                    "It's fetch + merge in one command.",
                    "The answer is: git pull",
                ],
            },
            {
                "id": "remote_4",
                "type": "quiz",
                "title": "Upload to the Remote",
                "flavor": "Your local commits need to go to the remote repository. Which command uploads them?",
                "lesson": (
                    "git push — uploads local commits to a remote repository.\n\n"
                    "Syntax:\n"
                    "  git push                  push to tracked remote (origin) and branch\n"
                    "  git push origin main      push local main to origin's main\n"
                    "  git push -u origin main   push AND set upstream tracking\n\n"
                    "git push fails (safely) if:\n"
                    "  - The remote has commits your local doesn't have\n"
                    "  - Solution: git pull first, then push\n\n"
                    "git push --force:\n"
                    "  - Overwrites the remote regardless of divergence\n"
                    "  - Destroys any commits on the remote that aren't in your local copy\n"
                    "  - Used by whoever tampered with this repository's history\n\n"
                    "Example: git push origin main    → uploads main to origin"
                ),
                "question": "What command uploads local commits to a remote repository?",
                "answers": ["git push", "push"],
                "xp": 50,
                "difficulty": "easy",
                "hints": [
                    "Think: pushing to the remote.",
                    "The answer is: git push",
                ],
            },
            {
                "id": "remote_boss",
                "type": "fill_blank",
                "title": "BOSS: The Force Push",
                "flavor": "The remote has been overwritten. The access logs show git push --force at 2:47 AM. What flag was used — and what does it do to the remote's existing history?",
                "lesson": (
                    "git push --force — overwrites the remote branch with the local branch,\n"
                    "regardless of what's currently on the remote.\n\n"
                    "What --force does:\n"
                    "  - Takes your local branch pointer\n"
                    "  - Sets the remote branch to point to the same commit\n"
                    "  - Any commits on the remote that aren't in your local history are GONE\n"
                    "  - Collaborators who fetched those commits will have diverged histories\n\n"
                    "Safer alternatives:\n"
                    "  --force-with-lease    only force-push if remote matches your last fetch\n"
                    "                        (prevents overwriting others' work accidentally)\n\n"
                    "Force push is the primary mechanism of git history tampering.\n"
                    "Most git hosts log force pushes. Most teams don't review those logs."
                ),
                "question": "Complete the command that overwrites the remote branch regardless of divergence:\n\ngit push ___ origin main",
                "answers": ["--force", "-f", "--force-with-lease"],
                "xp": 200,
                "difficulty": "boss",
                "is_boss": True,
                "hints": [
                    "It forces the push even if it would destroy remote commits.",
                    "The answer is: --force",
                ],
            },
        ],
    },

    "recovery_vault": {
        "id": "recovery_vault",
        "name": "The Recovery Vault",
        "subtitle": "Stash, Reset & Reflog",
        "color": "yellow",
        "icon": "🔄",
        "commands": ["git stash", "git reset", "git revert", "git reflog"],
        "challenges": [
            {
                "id": "recover_1",
                "type": "quiz",
                "title": "Shelve the Work",
                "flavor": "You have uncommitted changes. You need to switch branches without committing. What command temporarily saves your working directory state?",
                "lesson": (
                    "git stash — temporarily shelves uncommitted changes so you can switch context.\n\n"
                    "Common usages:\n"
                    "  git stash          save current changes to the stash stack\n"
                    "  git stash list     show all stashed changesets\n"
                    "  git stash pop      restore the most recent stash (and remove it)\n"
                    "  git stash apply    restore without removing from the stack\n"
                    "  git stash drop     delete a stash entry\n\n"
                    "Stash saves:\n"
                    "  - Tracked, modified files\n"
                    "  - Staged changes\n"
                    "  - Optionally: untracked files (git stash -u)\n\n"
                    "Example: git stash    → saves current changes, restores clean working directory"
                ),
                "question": "What command temporarily shelves uncommitted changes so you can switch context?",
                "answers": ["git stash", "stash"],
                "xp": 75,
                "difficulty": "easy",
                "hints": [
                    "Think: stashing the work for later.",
                    "The answer is: git stash",
                ],
            },
            {
                "id": "recover_2",
                "type": "quiz",
                "title": "The Ghost History",
                "flavor": "The reflog is the history of the history. It records every time a branch pointer moved — including the hard reset and force push that happened at 2:47 AM. What command shows it?",
                "lesson": (
                    "git reflog — shows a log of every change to HEAD and branch pointers.\n\n"
                    "The reflog records:\n"
                    "  - Every commit, merge, rebase\n"
                    "  - Every checkout, reset, rebase step\n"
                    "  - Even after force push, hard reset, or branch deletion\n\n"
                    "Retention policy:\n"
                    "  By default: 90 days for reachable objects, 30 days for unreachable\n"
                    "  Configurable: gc.reflogExpire, gc.reflogExpireUnreachable\n\n"
                    "Forensic value:\n"
                    "  git reflog shows the REAL sequence of operations, including the\n"
                    "  ones that were designed to be invisible in git log.\n\n"
                    "Example: git reflog    → full history of HEAD movement"
                ),
                "question": "What command shows a log of every change to HEAD and branch pointers — the 'ghost history'?",
                "answers": ["git reflog", "reflog"],
                "xp": 100,
                "difficulty": "medium",
                "hints": [
                    "Think: reference log.",
                    "The answer is: git reflog",
                ],
            },
            {
                "id": "recover_3",
                "type": "quiz",
                "title": "Undo Without Rewriting",
                "flavor": "You need to undo the effects of a commit that's already been pushed and shared. You can't rewrite history — other people have it. What command creates a new commit that reverses the changes?",
                "lesson": (
                    "git revert <hash> — creates a NEW commit that undoes a previous commit.\n\n"
                    "git revert vs git reset:\n"
                    "  git revert    safe for shared history — adds a new commit, doesn't rewrite\n"
                    "  git reset     rewrites history — NEVER use on shared/pushed commits\n\n"
                    "git revert:\n"
                    "  - Takes the diff of a commit and applies it in reverse\n"
                    "  - Creates a new commit with the reversal\n"
                    "  - The original commit remains in the history\n"
                    "  - Other developers can pull the revert without issues\n\n"
                    "Example: git revert a3f9c21    → creates a commit that undoes a3f9c21"
                ),
                "question": "What command creates a new commit that reverses the changes of a previous commit (safe for shared history)?",
                "answers": ["git revert", "revert"],
                "xp": 100,
                "difficulty": "medium",
                "hints": [
                    "It's the safe undo — it adds a commit rather than removing one.",
                    "The answer is: git revert",
                ],
            },
            {
                "id": "recover_4",
                "type": "quiz",
                "title": "Hard Reset Consequences",
                "flavor": "They ran git reset --hard to a previous commit. The working directory was wiped, the branch pointer moved back. But what happened to the commits that were ahead of the reset point?",
                "lesson": (
                    "git reset — moves the branch pointer and optionally changes staging/working directory.\n\n"
                    "Three modes:\n"
                    "  --soft    move branch pointer only; staging area and working dir unchanged\n"
                    "  --mixed   move pointer + reset staging area; working dir unchanged (default)\n"
                    "  --hard    move pointer + reset staging + reset working directory\n"
                    "            WARNING: working directory changes are PERMANENTLY LOST\n\n"
                    "After git reset --hard to commit X:\n"
                    "  - Commits after X are orphaned (no branch points to them)\n"
                    "  - They're NOT immediately deleted — they stay in the object store\n"
                    "  - They're still in the reflog\n"
                    "  - git gc eventually removes them (after 30-90 days)\n\n"
                    "Recovery: git reflog to find the old hash, then git reset --hard <hash>"
                ),
                "question": "After git reset --hard to a previous commit, what happens to commits that were ahead of the reset point?",
                "answers": [
                    "they become orphaned",
                    "orphaned",
                    "they are orphaned commits",
                    "they lose their branch reference",
                    "unreachable but not deleted",
                ],
                "xp": 125,
                "difficulty": "hard",
                "hints": [
                    "They still exist in the object store, but nothing points to them.",
                    "They're not immediately deleted — they're just unreachable from any branch.",
                    "The answer is: they become orphaned (unreachable) commits",
                ],
            },
            {
                "id": "recover_boss",
                "type": "fill_blank",
                "title": "BOSS: Read the Reflog",
                "flavor": "The branch was hard-reset to hide the evidence. But the original commits are still in the reflog. Which command do you run to find them?",
                "lesson": (
                    "git reflog — the primary forensic tool for recovering 'lost' commits.\n\n"
                    "Output format:\n"
                    "  a3f9c21 HEAD@{0}: commit: Add analysis\n"
                    "  b2e8d14 HEAD@{1}: reset: moving to HEAD~3\n"
                    "  c1d7f03 HEAD@{2}: commit: Contested algorithm added\n"
                    "  d0c6e92 HEAD@{3}: commit: Initial structure\n\n"
                    "The 'reset: moving to HEAD~3' entry shows the hard reset.\n"
                    "The commits that were reset away (c1d7f03, d0c6e92) are still here.\n\n"
                    "To recover: git reset --hard c1d7f03\n"
                    "Or create a branch at the old hash: git branch recovered c1d7f03"
                ),
                "question": "Complete this command to view the full history of HEAD movements including the hidden reset:\n\ngit ___",
                "answers": ["reflog", "reflog show", "reflog HEAD"],
                "xp": 200,
                "difficulty": "boss",
                "is_boss": True,
                "hints": [
                    "Think: reference log.",
                    "The answer is: reflog",
                ],
            },
        ],
    },

    "forensics_chamber": {
        "id": "forensics_chamber",
        "name": "The Forensics Chamber",
        "subtitle": "Blame, Bisect & Advanced Log",
        "color": "red",
        "icon": "🔬",
        "commands": ["git blame", "git bisect", "git log --follow", "git cherry-pick", "git shortlog"],
        "challenges": [
            {
                "id": "forensics_1",
                "type": "quiz",
                "title": "Attribute the Code",
                "flavor": "Every line of the contested algorithm. You need to know which commit last touched each line, and who authored that commit. One command annotates the entire file.",
                "lesson": (
                    "git blame <file> — annotates every line with commit hash, author, and date.\n\n"
                    "Output format (per line):\n"
                    "  a3f9c21 (Jane Smith  2022-03-14 09:23:11 +0000  42) def algorithm():\n"
                    "  b2e8d14 (Corp DevOps 2023-08-01 02:47:00 +0000  43)     pass\n\n"
                    "  Column 1: short commit hash\n"
                    "  Column 2: author name\n"
                    "  Column 3: commit timestamp\n"
                    "  Column 4: line number\n"
                    "  Column 5: line content\n\n"
                    "Forensic use: if every critical line shows an author who left before\n"
                    "the corp claims the code was written, that's significant.\n\n"
                    "Example: git blame algorithm.py    → full annotation of algorithm.py"
                ),
                "question": "What command annotates every line of a file with the commit and author that last changed it?",
                "answers": ["git blame", "blame"],
                "xp": 100,
                "difficulty": "medium",
                "hints": [
                    "Think: blaming each line on a specific commit.",
                    "The answer is: git blame",
                ],
            },
            {
                "id": "forensics_2",
                "type": "quiz",
                "title": "Binary Search the History",
                "flavor": "The algorithm was working in January. It's broken now. There are 300 commits between then and now. You need to find the exact commit that introduced the change — efficiently.",
                "lesson": (
                    "git bisect — uses binary search to find which commit introduced a change.\n\n"
                    "Workflow:\n"
                    "  git bisect start          begin bisect session\n"
                    "  git bisect bad            mark current commit as 'bad' (has the issue)\n"
                    "  git bisect good <hash>    mark a known-good commit\n\n"
                    "Git checks out the midpoint commit. You test it.\n"
                    "  git bisect good           if this commit is fine\n"
                    "  git bisect bad            if this commit has the issue\n\n"
                    "Git keeps halving the range. After log2(300) ≈ 8 steps, it identifies\n"
                    "the exact commit that introduced the change.\n\n"
                    "  git bisect reset          when done, return to original state\n\n"
                    "Example: With 300 commits, bisect finds the answer in 8 tests."
                ),
                "question": "What git command uses binary search to find which commit introduced a specific change?",
                "answers": ["git bisect", "bisect"],
                "xp": 100,
                "difficulty": "medium",
                "hints": [
                    "Think: bisecting the history in half.",
                    "The answer is: git bisect",
                ],
            },
            {
                "id": "forensics_3",
                "type": "flag_quiz",
                "title": "Track Through Renames",
                "flavor": "The file was renamed three times to obscure its origin. git log shows nothing for the current filename before the third rename. Which flag follows the file across renames?",
                "lesson": (
                    "git log --follow <file> — tracks file history across renames.\n\n"
                    "Without --follow:\n"
                    "  git log algorithm.py    shows only commits after the last rename\n\n"
                    "With --follow:\n"
                    "  git log --follow algorithm.py    shows the FULL history, including\n"
                    "                                   commits when it was named something else\n\n"
                    "Git detects renames by content similarity (>50% by default).\n\n"
                    "Forensic significance: renaming a file is a common obfuscation technique.\n"
                    "--follow exposes the original authorship regardless of renames.\n\n"
                    "Example: git log --follow --oneline algorithm.py"
                ),
                "question": "Which git log flag tracks a file's history across renames?",
                "answers": ["--follow", "--follow -p"],
                "xp": 125,
                "difficulty": "hard",
                "hints": [
                    "Think: follow the file through renames.",
                    "The answer is: --follow",
                ],
            },
            {
                "id": "forensics_4",
                "type": "quiz",
                "title": "Port a Specific Commit",
                "flavor": "There's one commit on the evidence branch that you need on the main forensics branch — just that one commit, without merging the entire branch. How?",
                "lesson": (
                    "git cherry-pick <hash> — applies a specific commit to the current branch.\n\n"
                    "Cherry-pick:\n"
                    "  - Takes the diff from a specific commit\n"
                    "  - Applies that diff to the current branch\n"
                    "  - Creates a NEW commit (new hash, same changes)\n"
                    "  - The original commit is not moved or affected\n\n"
                    "Syntax:\n"
                    "  git cherry-pick a3f9c21         pick one commit\n"
                    "  git cherry-pick a3f..b4e         pick a range\n"
                    "  git cherry-pick --no-commit      apply changes without committing\n\n"
                    "Forensic use: extract specific changes from a branch without\n"
                    "pulling in unrelated work.\n\n"
                    "Example: git cherry-pick a3f9c21    → applies that commit's changes here"
                ),
                "question": "What command applies a specific commit from anywhere in the history to the current branch?",
                "answers": ["git cherry-pick", "cherry-pick"],
                "xp": 125,
                "difficulty": "hard",
                "hints": [
                    "Think: picking a specific commit like a cherry.",
                    "The answer is: git cherry-pick",
                ],
            },
            {
                "id": "forensics_boss",
                "type": "fill_blank",
                "title": "FINAL BOSS: The Attribution Report",
                "flavor": "The closing argument. git blame on 'algorithm.py'. Every line. Every commit. Every author timestamp. Which command produces the annotated file output for the record?",
                "lesson": (
                    "git blame — the forensic closer.\n\n"
                    "Full command for maximum forensic detail:\n"
                    "  git blame -w --date=iso algorithm.py\n\n"
                    "  -w            ignore whitespace changes (common obfuscation)\n"
                    "  --date=iso    show full ISO timestamps (exact seconds)\n"
                    "  -L n,m        blame only lines n through m\n"
                    "  -e            show author email instead of name\n\n"
                    "The output is your exhibit.\n"
                    "Commit hash. Author. Timestamp. Line content.\n"
                    "Forty-eight hours of work concluding in one command."
                ),
                "question": "Complete this command to annotate 'algorithm.py' with full author and commit information:\n\ngit ___ algorithm.py",
                "answers": ["blame", "blame -w", "blame --date=iso"],
                "xp": 300,
                "difficulty": "boss",
                "is_boss": True,
                "hints": [
                    "You want to attribute each line to its author.",
                    "The command is two words: git blame.",
                    "The answer is: blame",
                ],
            },
        ],
    },
}

ZONE_ORDER = [
    "origin_vault",
    "staging_area",
    "commit_ledger",
    "branch_matrix",
    "merge_protocol",
    "rebase_engine",
    "remote_network",
    "recovery_vault",
    "forensics_chamber",
]
