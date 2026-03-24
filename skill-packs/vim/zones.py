"""
zones.py - All zone and challenge data for Vim Quest
Challenge types: quiz, fill_blank, flag_quiz
"""

ZONES = {
    "normal_vault": {
        "id": "normal_vault",
        "name": "The Normal Vault",
        "subtitle": "Movement, Navigation & Basic Editing",
        "color": "cyan",
        "icon": "🔲",
        "commands": ["hjkl", "w/b/e", "gg/G", "0/$", "dd/yy/p", "u/Ctrl+R"],
        "challenges": [
            {
                "id": "nv_1",
                "type": "quiz",
                "title": "Move Left",
                "flavor": "The cursor is on a line in the config file. You need to move it one character to the left. In normal mode, what key does this?",
                "lesson": (
                    "h — move the cursor one character left.\n\n"
                    "The four movement keys in vim (all in normal mode):\n"
                    "  h → left    j → down    k → up    l → right\n\n"
                    "They're on the home row of the keyboard — your right hand's resting position.\n"
                    "This is intentional: vim was designed so your hands never leave the home row.\n\n"
                    "Arrow keys also work, but using hjkl keeps your hands in position.\n"
                    "After a few hours of practice, hjkl becomes faster than arrow keys."
                ),
                "answer": "h",
                "hints": ["It's the leftmost of the four movement keys.", "Home row: h j k l — h is far left.", "The answer is: h"],
            },
            {
                "id": "nv_2",
                "type": "quiz",
                "title": "Jump to File Bottom",
                "flavor": "The audit log is 4,000 lines. You need to jump to the very last line instantly. What key does this in normal mode?",
                "lesson": (
                    "G — jump to the last line of the file.\n\n"
                    "Complementary motions:\n"
                    "  gg  → jump to the first line (line 1)\n"
                    "  G   → jump to the last line\n"
                    "  NNG → jump to line N (e.g. 42G goes to line 42)\n\n"
                    "Context:\n"
                    "  :N  → also goes to line N (e.g. :42 ↵)\n"
                    "  Ctrl+G → show current line number and file info in the status bar\n\n"
                    "G is uppercase — hold Shift while pressing g."
                ),
                "answer": "G",
                "hints": ["It's a single uppercase letter — the last letter of the alphabet.", "Uppercase G. Think: go to the end.", "The answer is: G"],
            },
            {
                "id": "nv_3",
                "type": "quiz",
                "title": "Move Forward One Word",
                "flavor": "You're at the beginning of a long key name. You need to jump forward one word at a time through the line. What key moves forward one word in normal mode?",
                "lesson": (
                    "w — move forward to the beginning of the next word.\n\n"
                    "Word movement keys:\n"
                    "  w  → forward to the start of the next word\n"
                    "  b  → backward to the start of the previous word\n"
                    "  e  → forward to the end of the current/next word\n\n"
                    "WORD vs word:\n"
                    "  w moves by 'word' — separated by whitespace AND punctuation\n"
                    "  W moves by 'WORD' — separated only by whitespace\n\n"
                    "Example: in 'key_name = \"value\"':\n"
                    "  w steps: key_ → name → = → \" → value → \"\n"
                    "  W steps: key_name → = → \"value\""
                ),
                "answer": "w",
                "hints": ["Think: word forward.", "Single lowercase letter.", "The answer is: w"],
            },
            {
                "id": "nv_4",
                "type": "quiz",
                "title": "Delete the Current Line",
                "flavor": "One line in the routing table is completely wrong and needs to be deleted. What normal-mode command deletes the entire current line?",
                "lesson": (
                    "dd — delete the current line.\n\n"
                    "The 'd' operator deletes. Doubled (dd) means 'delete the current line.'\n\n"
                    "Related:\n"
                    "  dd    → delete current line (cut to register)\n"
                    "  D     → delete from cursor to end of line\n"
                    "  d$    → same as D\n"
                    "  d0    → delete from cursor to beginning of line\n"
                    "  dw    → delete to the next word boundary\n"
                    "  5dd   → delete 5 lines\n\n"
                    "Note: deleted text in vim is 'yanked' into a register.\n"
                    "You can paste it with p (after cursor) or P (before cursor).\n"
                    "vim's 'delete' is more like 'cut.'"
                ),
                "answer": "dd",
                "hints": ["The 'd' operator, doubled.", "Two characters, same key pressed twice.", "The answer is: dd"],
            },
            {
                "id": "nv_5",
                "type": "quiz",
                "title": "Undo the Last Change",
                "flavor": "You deleted the wrong line. You need to undo immediately. What key undoes the last change in normal mode?",
                "lesson": (
                    "u — undo the last change.\n\n"
                    "  u        → undo the last change\n"
                    "  Ctrl+R   → redo (undo the undo)\n\n"
                    "vim has a full undo tree — not just a linear undo stack.\n"
                    "You can undo multiple times:\n"
                    "  uuu → undo three changes\n"
                    "  5u  → undo five changes\n\n"
                    "The undo history persists as long as the file is open.\n"
                    "It's reset when you close and reopen the file\n"
                    "(unless you configure undofile for persistent undo)."
                ),
                "answer": "u",
                "hints": ["It's the first letter of 'undo'.", "Single lowercase letter.", "The answer is: u"],
            },
            {
                "id": "nv_6",
                "type": "fill_blank",
                "is_boss": True,
                "title": "Boss: End of Line",
                "flavor": "You need to move to the very end of the current line in normal mode, without a count. What key does this?",
                "lesson": (
                    "$ — move to the end of the current line.\n\n"
                    "The line boundary keys:\n"
                    "  0   → move to column 0 (absolute beginning of line)\n"
                    "  ^   → move to the first non-whitespace character on the line\n"
                    "  $   → move to the last character on the line\n\n"
                    "Combined with operators:\n"
                    "  d$  → delete from cursor to end of line (same as D)\n"
                    "  y$  → yank from cursor to end of line\n"
                    "  c$  → change from cursor to end of line (same as C)\n\n"
                    "The $ and ^ mirror regex anchors — same meaning:\n"
                    "end of line and start of non-whitespace."
                ),
                "answer": "$",
                "hints": ["Think of regex: what character means 'end of line'?", "The shift+4 key on most keyboards.", "The answer is: $"],
            },
        ],
    },
    "insert_protocol": {
        "id": "insert_protocol",
        "name": "The Insert Protocol",
        "subtitle": "Entering, Editing & Exiting Insert Mode",
        "color": "green",
        "icon": "✏️",
        "commands": ["i/I", "a/A", "o/O", "c/cc/cw", "ESC", "Ctrl+C"],
        "challenges": [
            {
                "id": "ins_1",
                "type": "quiz",
                "title": "Enter Insert Mode",
                "flavor": "The cursor is positioned just before the value you need to change. What key enters insert mode at the cursor position?",
                "lesson": (
                    "i — enter insert mode at the cursor position (insert before cursor).\n\n"
                    "The primary insert entry points:\n"
                    "  i   → insert before the cursor\n"
                    "  a   → insert after the cursor (append)\n"
                    "  I   → insert at the beginning of the line\n"
                    "  A   → insert at the end of the line\n"
                    "  o   → open a new line below and enter insert mode\n"
                    "  O   → open a new line above and enter insert mode\n\n"
                    "Most common: i (insert here) and a (insert after — useful when\n"
                    "your cursor is on the last character of something you want to append to).\n\n"
                    "The status bar shows -- INSERT -- when you're in insert mode."
                ),
                "answer": "i",
                "hints": ["Think: insert. Single lowercase letter.", "The 'i' key.", "The answer is: i"],
            },
            {
                "id": "ins_2",
                "type": "quiz",
                "title": "Insert at End of Line",
                "flavor": "The cursor is at the beginning of a config line. You need to add a comment at the very end of the line without moving through it manually. What key enters insert mode at the end of the line?",
                "lesson": (
                    "A — enter insert mode at the end of the current line (Append).\n\n"
                    "A is shift+a. It's the combination of $ (end of line) and a (append).\n\n"
                    "Using A:\n"
                    "  Position cursor anywhere on the line\n"
                    "  Press A\n"
                    "  Cursor jumps to end of line, enter insert mode\n"
                    "  Type the text to append\n"
                    "  Press ESC\n\n"
                    "Much faster than:\n"
                    "  $ → move to end\n"
                    "  a → append after end\n\n"
                    "Similarly: I (uppercase) enters insert at the beginning of the line."
                ),
                "answer": "A",
                "hints": ["It's the uppercase version of 'a'.", "Shift+A — jumps to end of line and enters insert.", "The answer is: A"],
            },
            {
                "id": "ins_3",
                "type": "quiz",
                "title": "Open a New Line Below",
                "flavor": "You need to add a new line below the current one with some content. What key opens a new line below and enters insert mode?",
                "lesson": (
                    "o — open a new line below the current line and enter insert mode.\n\n"
                    "  o   → new line BELOW, enter insert mode\n"
                    "  O   → new line ABOVE, enter insert mode\n\n"
                    "What o actually does:\n"
                    "  1. Moves to the end of the current line\n"
                    "  2. Inserts a newline\n"
                    "  3. Enters insert mode on the new line\n"
                    "  4. Applies the current indentation automatically\n\n"
                    "This is the fastest way to add a new line when your cursor is\n"
                    "already on the line you want to insert after.\n\n"
                    "Remember: O (uppercase) adds above, o (lowercase) adds below."
                ),
                "answer": "o",
                "hints": ["Think: 'open' a new line below.", "Lowercase 'o'.", "The answer is: o"],
            },
            {
                "id": "ins_4",
                "type": "quiz",
                "title": "Exit Insert Mode",
                "flavor": "You've finished editing. You're in insert mode. What key returns you to normal mode?",
                "lesson": (
                    "ESC — exit insert mode, return to normal mode.\n\n"
                    "  ESC      → return to normal mode from any other mode\n"
                    "  Ctrl+C   → also returns to normal mode (slightly different behavior\n"
                    "              for some abbreviations and mappings)\n"
                    "  Ctrl+[   → equivalent to ESC; useful on keyboards without ESC\n\n"
                    "This is the most-used key in vim after hjkl.\n\n"
                    "Common habit: keep your hand position so ESC is easy to reach.\n"
                    "Many vim users remap Caps Lock to ESC for this reason.\n\n"
                    "After ESC, the cursor moves one character to the left (back to\n"
                    "the last character you were on before insert mode ended)."
                ),
                "answer": "ESC",
                "hints": ["The key at the top-left of most keyboards.", "It's written as a three-letter abbreviation.", "The answer is: ESC"],
            },
            {
                "id": "ins_5",
                "type": "quiz",
                "title": "Change a Word",
                "flavor": "Your cursor is at the start of a word you need to replace entirely. What normal-mode command deletes the word and enters insert mode so you can type the replacement?",
                "lesson": (
                    "cw — change word: delete to end of word, enter insert mode.\n\n"
                    "The 'c' (change) operator: like 'd' (delete), but enters insert mode\n"
                    "after deleting, so you can type the replacement immediately.\n\n"
                    "Common change operations:\n"
                    "  cw    → change to end of word\n"
                    "  ciw   → change entire word (inner word — see text objects)\n"
                    "  cc    → change the entire line\n"
                    "  C     → change from cursor to end of line\n"
                    "  c$    → same as C\n"
                    "  ci\"   → change inside double quotes\n\n"
                    "Workflow for replacing a word:\n"
                    "  Position cursor at start of word → cw → type new word → ESC"
                ),
                "answer": "cw",
                "hints": ["'c' for change, 'w' for word.", "Two letters: the change operator + word motion.", "The answer is: cw"],
            },
            {
                "id": "ins_6",
                "type": "fill_blank",
                "is_boss": True,
                "title": "Boss: Change Entire Line",
                "flavor": "A config line is completely wrong and needs to be rewritten from scratch. What command deletes the entire current line and enters insert mode?",
                "lesson": (
                    "cc — change the current line: delete the line content, enter insert mode.\n\n"
                    "  cc   → delete the line's text, stay on the line, enter insert mode\n"
                    "  dd   → delete the line entirely (removed from file, not just emptied)\n\n"
                    "The difference:\n"
                    "  dd   → the line is gone. p pastes it back.\n"
                    "  cc   → the line remains (at the same line number), its content is\n"
                    "          cleared, you type the replacement. The line number doesn't change.\n\n"
                    "Useful when you want to rewrite a line completely but keep it\n"
                    "in the same position in the file.\n\n"
                    "After cc, you're in insert mode on a blank line with correct indentation."
                ),
                "answer": "cc",
                "hints": ["The 'change' operator doubled, like 'dd' is the 'delete' operator doubled.", "Two of the same letter.", "The answer is: cc"],
            },
        ],
    },
    "command_line": {
        "id": "command_line",
        "name": "The Command Line",
        "subtitle": "Saving, Opening & Managing Files",
        "color": "yellow",
        "icon": ":",
        "commands": [":w", ":q", ":wq", ":q!", ":e", ":vs/:sp", ":set"],
        "challenges": [
            {
                "id": "cmd_1",
                "type": "fill_blank",
                "title": "Save the File",
                "flavor": "You've made the changes to the config file. You need to save it. Complete the command-line command: :___",
                "lesson": (
                    ":w — write (save) the current file.\n\n"
                    "  :w           → save the current file\n"
                    "  :w filename  → save to a different filename (like Save As)\n"
                    "  :w!          → force write (override read-only, if permissions allow)\n\n"
                    "Combined:\n"
                    "  :wq   → write and quit\n"
                    "  :x    → write (only if changed) and quit — slightly different from :wq\n"
                    "          :x doesn't update the file's timestamp if nothing changed\n"
                    "  ZZ    → normal mode shortcut for :x\n\n"
                    "Command-line mode is entered with ':' from normal mode.\n"
                    "The command appears at the bottom of the screen.\n"
                    "Press Enter to execute, or ESC to cancel."
                ),
                "answer": "w",
                "hints": ["Single letter — 'write'.", "The answer is: w"],
            },
            {
                "id": "cmd_2",
                "type": "fill_blank",
                "title": "Quit Without Saving",
                "flavor": "You opened the wrong file and made accidental changes. You need to exit without saving anything. Complete: :___",
                "lesson": (
                    ":q! — quit without saving, ignoring unsaved changes.\n\n"
                    "  :q    → quit (fails if there are unsaved changes)\n"
                    "  :q!   → quit and DISCARD unsaved changes (the ! means 'force')\n"
                    "  :wq   → save and quit\n"
                    "  :qa!  → quit ALL open files without saving (a = all)\n\n"
                    "The ! (bang) in vim commands generally means 'force' or 'override'.\n"
                    "  :w!   → force write\n"
                    "  :q!   → force quit (discard changes)\n"
                    "  :e!   → force reload from disk (discard unsaved changes in current buffer)\n\n"
                    "Most beginners learn :q! before anything else. It's the escape hatch."
                ),
                "answer": "q!",
                "hints": ["Quit, forced — using the '!' modifier.", "The answer is: q!"],
            },
            {
                "id": "cmd_3",
                "type": "fill_blank",
                "title": "Open Another File",
                "flavor": "You're in a vim session and need to open a different file: /var/log/nexus/audit.log. Complete: :___ /var/log/nexus/audit.log",
                "lesson": (
                    ":e — edit (open) a file in the current vim session.\n\n"
                    "  :e filename   → open a file in the current window (replaces current buffer)\n"
                    "  :e!           → reload the current file from disk (discard changes)\n"
                    "  :e .          → open the directory explorer (netrw) for the current directory\n\n"
                    "Tab completion works for filenames in command-line mode:\n"
                    "  :e /var/log/ne<Tab> → completes the path\n\n"
                    "Related:\n"
                    "  :vs filename   → open in a vertical split\n"
                    "  :sp filename   → open in a horizontal split\n"
                    "  :tabedit file  → open in a new tab"
                ),
                "answer": "e",
                "hints": ["Think: 'edit' a file.", "Single letter.", "The answer is: e"],
            },
            {
                "id": "cmd_4",
                "type": "fill_blank",
                "title": "Vertical Split",
                "flavor": "You need to open a second file side-by-side with the current one (vertical split). Complete: :___ /etc/nexus/processor.conf",
                "lesson": (
                    ":vs — vertical split: open a file in a new vertical pane.\n\n"
                    "  :vs filename   → vertical split; file opens on the RIGHT\n"
                    "  :sp filename   → horizontal split; file opens BELOW\n"
                    "  :vs            → vertical split the current buffer (useful for comparing)\n\n"
                    "Navigating splits:\n"
                    "  Ctrl+W h   → move to the split on the left\n"
                    "  Ctrl+W l   → move to the split on the right\n"
                    "  Ctrl+W j   → move to the split below\n"
                    "  Ctrl+W k   → move to the split above\n"
                    "  Ctrl+W w   → cycle through splits\n\n"
                    "Resizing splits:\n"
                    "  Ctrl+W =   → equalize all split sizes\n"
                    "  Ctrl+W >   → increase width\n"
                    "  Ctrl+W <   → decrease width"
                ),
                "answer": "vs",
                "hints": ["Two letters: vertical split.", "The answer is: vs"],
            },
            {
                "id": "cmd_5",
                "type": "fill_blank",
                "title": "Save and Quit",
                "flavor": "You're done editing. Save the file and close vim in one command. Complete: :___",
                "lesson": (
                    ":wq — write and quit.\n\n"
                    "  :wq   → save the current file and exit vim\n"
                    "  :wq!  → force save (override read-only) and quit\n"
                    "  :x    → same as :wq but only writes if changes were made\n"
                    "  ZZ    → normal mode shortcut for :x\n\n"
                    "Multiple buffers:\n"
                    "  :wqa  → write all modified buffers and quit\n"
                    "  :qa   → quit all (fails if any have unsaved changes)\n"
                    "  :qa!  → force quit all (discard all unsaved changes)\n\n"
                    "In a session with multiple split windows:\n"
                    "  :q    → closes the current window (not the whole session)\n"
                    "  :qall → closes all windows and exits vim"
                ),
                "answer": "wq",
                "hints": ["Write + quit, combined into one command.", "Two letters.", "The answer is: wq"],
            },
            {
                "id": "cmd_6",
                "type": "fill_blank",
                "is_boss": True,
                "title": "Boss: Go to Line Number",
                "flavor": "The error is on line 2847 of the 4,000-line audit log. Go there directly from command-line mode. Complete: :___",
                "lesson": (
                    ":N — go to line number N.\n\n"
                    "  :2847   → jump to line 2847\n"
                    "  :1      → jump to line 1 (same as gg in normal mode)\n"
                    "  :$      → jump to the last line (same as G)\n\n"
                    "Alternatives:\n"
                    "  2847G   → in normal mode, go to line 2847\n"
                    "  2847gg  → also goes to line 2847\n\n"
                    "Show current line information:\n"
                    "  Ctrl+G   → shows filename, current line, total lines, percentage\n"
                    "  :set nu  → show line numbers in the left margin\n"
                    "  :set rnu → show relative line numbers\n\n"
                    "The answer to this specific question: the number itself is the command.\n"
                    "':2847' goes to line 2847. The answer format is just the number."
                ),
                "answer": "2847",
                "hints": ["The command is just the line number itself.", "Type the number after the colon.", "The answer is: 2847"],
            },
        ],
    },
    "visual_mode": {
        "id": "visual_mode",
        "name": "Visual Mode",
        "subtitle": "Selection, Block Operations & Visual Editing",
        "color": "magenta",
        "icon": "🔲",
        "commands": ["v", "V", "Ctrl+V", "d/y/c in visual", "><", "I in block"],
        "challenges": [
            {
                "id": "vis_1",
                "type": "quiz",
                "title": "Enter Character Visual",
                "flavor": "You need to select a few characters in the middle of a line and delete them. What key enters character-wise visual mode?",
                "lesson": (
                    "v — enter character-wise visual mode.\n\n"
                    "In visual mode:\n"
                    "  - The cursor movement keys (hjkl, w, b, etc.) extend the selection\n"
                    "  - The selection is highlighted\n"
                    "  - Operators (d, y, c, >, <) act on the selection\n\n"
                    "Three visual modes:\n"
                    "  v        → character-wise (select individual characters)\n"
                    "  V        → line-wise (select whole lines)\n"
                    "  Ctrl+V   → block-wise (select a rectangular column)\n\n"
                    "After selecting:\n"
                    "  d → delete the selection\n"
                    "  y → yank (copy) the selection\n"
                    "  c → change (delete and enter insert mode)\n"
                    "  > → indent right\n"
                    "  < → indent left"
                ),
                "answer": "v",
                "hints": ["Single lowercase letter — 'visual'.", "The answer is: v"],
            },
            {
                "id": "vis_2",
                "type": "quiz",
                "title": "Select Whole Lines",
                "flavor": "You need to select three complete lines and delete them. What key enters line-wise visual mode?",
                "lesson": (
                    "V — enter line-wise visual mode (uppercase V).\n\n"
                    "Line-wise visual selects entire lines, not partial lines.\n"
                    "The minimum selection is one full line. Moving up or down\n"
                    "adds or removes complete lines from the selection.\n\n"
                    "Workflow for deleting 3 lines:\n"
                    "  V     → enter line visual mode (selects current line)\n"
                    "  2j    → extend selection down 2 more lines (3 total)\n"
                    "  d     → delete the 3 selected lines\n\n"
                    "Alternative without visual mode:\n"
                    "  3dd   → delete 3 lines from the current position\n\n"
                    "Line-wise visual is most useful when the number of lines\n"
                    "isn't easily counted, or when you want to visually confirm\n"
                    "the selection before acting on it."
                ),
                "answer": "V",
                "hints": ["Uppercase V — visual line mode.", "Shift+V", "The answer is: V"],
            },
            {
                "id": "vis_3",
                "type": "quiz",
                "title": "Block Visual Mode",
                "flavor": "The routing table has a column of values that all need to be prefixed with 'FLAG:'. What visual mode lets you select a rectangular column across multiple lines simultaneously?",
                "lesson": (
                    "Ctrl+V — enter block-wise visual mode (column selection).\n\n"
                    "Block visual selects a rectangular region across multiple lines.\n"
                    "It ignores line length — you select a column N characters wide\n"
                    "and M lines tall.\n\n"
                    "Key operations in block visual:\n"
                    "  I   → insert text at the beginning of every selected line\n"
                    "  A   → append text at the end of every selected line\n"
                    "  d   → delete the selected column from every line\n"
                    "  r   → replace all characters in the block with one character\n\n"
                    "To prefix a column:\n"
                    "  Ctrl+V → select the column\n"
                    "  I      → enter block insert mode\n"
                    "  type 'FLAG:'  → only shows on first line while typing\n"
                    "  ESC   → text appears on ALL selected lines simultaneously"
                ),
                "answer": "Ctrl+V",
                "hints": ["Think: block visual. It's a control key combination.", "Ctrl + V — column selection.", "The answer is: Ctrl+V"],
            },
            {
                "id": "vis_4",
                "type": "quiz",
                "title": "Yank the Selection",
                "flavor": "You've selected a block of evidence text in visual mode and need to copy it (yank it) to paste elsewhere. What key yanks (copies) the visual selection?",
                "lesson": (
                    "y — yank (copy) the visual selection.\n\n"
                    "  y → yank the selected text into the default register\n"
                    "  d → delete (cut) the selected text\n"
                    "  c → change (delete and enter insert mode)\n\n"
                    "After yanking, exit visual mode (ESC or y exits automatically),\n"
                    "move to the destination, and paste:\n"
                    "  p → paste after the cursor\n"
                    "  P → paste before the cursor\n\n"
                    "Registers: yanked text goes into the unnamed register (\").\n"
                    "  \"ay → yank into register 'a'\n"
                    "  \"ap → paste from register 'a'\n\n"
                    "System clipboard:\n"
                    "  \"+y → yank to the system clipboard\n"
                    "  \"+p → paste from the system clipboard"
                ),
                "answer": "y",
                "hints": ["Think: 'yank' — vim's term for copy.", "Single lowercase letter.", "The answer is: y"],
            },
            {
                "id": "vis_5",
                "type": "quiz",
                "title": "Indent Selected Lines",
                "flavor": "You've selected several lines of config in visual mode and need to indent them one level to the right. What key indents the selection?",
                "lesson": (
                    "> — indent the selected lines one level to the right.\n\n"
                    "  >  → indent the visual selection right (one shiftwidth)\n"
                    "  <  → unindent the visual selection left\n\n"
                    "In normal mode (no visual selection):\n"
                    "  >>  → indent the current line right\n"
                    "  <<  → unindent the current line left\n"
                    "  N>> → indent N lines\n\n"
                    "The indentation amount is controlled by :set shiftwidth=N\n"
                    "(default is usually 8, but most modern configs set it to 2 or 4).\n\n"
                    "After indenting in visual mode, vim exits visual mode.\n"
                    "To indent again, use gv to re-select the same region, then > again."
                ),
                "answer": ">",
                "hints": ["Think of an arrow pointing right — indenting to the right.", "The > symbol.", "The answer is: >"],
            },
            {
                "id": "vis_6",
                "type": "fill_blank",
                "is_boss": True,
                "title": "Boss: Insert at Column",
                "flavor": "In block visual mode, you've selected a column. What key inserts text at the beginning of every selected line simultaneously?",
                "lesson": (
                    "I — insert at the beginning of every line in a block visual selection.\n\n"
                    "This is one of vim's most powerful operations:\n"
                    "  1. Ctrl+V to enter block visual\n"
                    "  2. Select the column across the lines you want to modify\n"
                    "  3. Press I (uppercase i)\n"
                    "  4. Type the text — it only appears on the first line while typing\n"
                    "  5. Press ESC — the text instantly appears on ALL selected lines\n\n"
                    "Example: adding '# ' (comment prefix) to 20 lines:\n"
                    "  Ctrl+V\n"
                    "  19j (extend selection down 19 lines)\n"
                    "  I\n"
                    "  # \n"
                    "  ESC\n"
                    "  → all 20 lines now start with '# '\n\n"
                    "Note: I in block visual is uppercase i (Shift+i), not lowercase."
                ),
                "answer": "I",
                "hints": ["It's the uppercase version of the 'insert' key.", "Shift+I — insert at start of every selected line.", "The answer is: I"],
            },
        ],
    },
    "search_engine": {
        "id": "search_engine",
        "name": "The Search Engine",
        "subtitle": "Search, Replace & Pattern Navigation",
        "color": "red",
        "icon": "🔍",
        "commands": ["/pattern", "?pattern", "n/N", "*/#", ":%s/old/new/g"],
        "challenges": [
            {
                "id": "srch_1",
                "type": "fill_blank",
                "title": "Search Forward",
                "flavor": "The config file is 4,000 lines. You need to find the 'max_retry_count' setting. What do you type to start a forward search for 'max_retry'?",
                "lesson": (
                    "/ — enter forward search mode.\n\n"
                    "  /pattern   → search forward for 'pattern'\n"
                    "  ?pattern   → search backward for 'pattern'\n\n"
                    "After typing the pattern, press Enter to search.\n\n"
                    "Navigation after searching:\n"
                    "  n   → jump to the NEXT match (forward)\n"
                    "  N   → jump to the PREVIOUS match (backward)\n\n"
                    "Highlight all matches:\n"
                    "  :set hlsearch   → highlight all matches\n"
                    "  :nohlsearch     → clear highlights (or :noh)\n\n"
                    "Incremental search (highlights as you type):\n"
                    "  :set incsearch  → most modern vim configs enable this by default\n\n"
                    "So: to search for 'max_retry': type /max_retry then Enter."
                ),
                "answer": "/max_retry",
                "hints": ["The search key is '/', followed by the pattern.", "The answer is: /max_retry"],
            },
            {
                "id": "srch_2",
                "type": "quiz",
                "title": "Search for Word Under Cursor",
                "flavor": "Your cursor is on a vendor name in the routing table. You want to find all other occurrences instantly. What key searches for the exact word under the cursor?",
                "lesson": (
                    "* — search forward for the word under the cursor.\n\n"
                    "  *   → search forward for the exact word under the cursor\n"
                    "  #   → search backward for the exact word under the cursor\n\n"
                    "These are 'whole word' searches — they match the exact word,\n"
                    "not substrings. If the cursor is on 'vendor', * finds 'vendor'\n"
                    "but not 'vendor_id' or 'multivendor'.\n\n"
                    "After pressing *, use n/N to navigate between matches.\n\n"
                    "Combining with substitution:\n"
                    "  Position on a word, press *, note the search pattern in\n"
                    "  the status bar, then use :%s// (empty pattern reuses last search)\n"
                    "  to replace all occurrences."
                ),
                "answer": "*",
                "hints": ["It's a special symbol — the asterisk.", "The * key — searches for the word under cursor.", "The answer is: *"],
            },
            {
                "id": "srch_3",
                "type": "fill_blank",
                "title": "Replace on Current Line",
                "flavor": "The current line has 'phantom_vendor' twice. You need to replace both instances with 'FLAGGED'. Complete the substitution command: :s/phantom_vendor/FLAGGED/___",
                "lesson": (
                    ":s/old/new/g — substitute on the current line, all occurrences.\n\n"
                    "The 'g' flag means 'global' — replace ALL occurrences on the line.\n"
                    "Without 'g', only the FIRST occurrence on the line is replaced.\n\n"
                    "Flags:\n"
                    "  g → replace all occurrences (global)\n"
                    "  i → case-insensitive match\n"
                    "  c → confirm each replacement\n"
                    "  e → suppress error if pattern not found\n\n"
                    "Scope:\n"
                    "  :s/old/new/g        → current line only\n"
                    "  :%s/old/new/g       → entire file\n"
                    "  :5,10s/old/new/g    → lines 5 through 10\n"
                    "  :'<,'>s/old/new/g   → visual selection (set automatically after V)"
                ),
                "answer": "g",
                "hints": ["The flag that means 'all occurrences' (global).", "Single letter appended after the last /", "The answer is: g"],
            },
            {
                "id": "srch_4",
                "type": "fill_blank",
                "title": "Replace in Entire File",
                "flavor": "The vendor name 'NEXUS_PHANTOM' appears 23 times across the file. Replace all occurrences with 'FLAGGED_VENDOR'. Complete: :___s/NEXUS_PHANTOM/FLAGGED_VENDOR/g",
                "lesson": (
                    ":%s/old/new/g — substitute in the entire file.\n\n"
                    "The % address means 'all lines' — equivalent to 1,$ (line 1 to last line).\n\n"
                    "  :%s/old/new/g    → replace all occurrences in the entire file\n"
                    "  :%s/old/new/gc   → replace all, confirming each one\n"
                    "                     (y/n/a/q/l per match)\n\n"
                    "Address examples:\n"
                    "  :%         → all lines\n"
                    "  :1,10      → lines 1-10\n"
                    "  :.,+5      → current line plus 5 lines after\n"
                    "  :'<,'>     → current visual selection\n\n"
                    "Special characters in the pattern:\n"
                    "  \\n  → newline\n"
                    "  \\.  → literal dot (. alone matches any character)\n"
                    "  \\b  → word boundary"
                ),
                "answer": "%",
                "hints": ["The address that means 'entire file' goes before the 's'.", "The % symbol.", "The answer is: %"],
            },
            {
                "id": "srch_5",
                "type": "quiz",
                "title": "Next Search Match",
                "flavor": "You've searched for 'disbursement_code' and there are multiple matches. What key jumps to the next match?",
                "lesson": (
                    "n — jump to the next search match.\n\n"
                    "  n  → next match in the search direction (forward for /, backward for ?)\n"
                    "  N  → opposite direction\n\n"
                    "After a / search:\n"
                    "  n → next match forward\n"
                    "  N → previous match (backward)\n\n"
                    "After a ? search:\n"
                    "  n → next match backward (same direction as the search)\n"
                    "  N → next match forward\n\n"
                    "If the search wraps around (reaches end of file and continues\n"
                    "from the beginning), vim shows 'search wrapped around' in the\n"
                    "status bar. Disable wrapping with :set nowrapscan."
                ),
                "answer": "n",
                "hints": ["Think: 'next'. Single lowercase letter.", "The answer is: n"],
            },
            {
                "id": "srch_6",
                "type": "fill_blank",
                "is_boss": True,
                "title": "Boss: Confirm Each Replacement",
                "flavor": "You need to review each replacement before making it. What flag added to :%s/old/new/ makes vim confirm each substitution interactively?",
                "lesson": (
                    "c — the confirm flag: vim pauses at each match and asks y/n/a/q/l.\n\n"
                    "  :%s/PHANTOM/FLAGGED/gc  → replace all, confirming each one\n\n"
                    "At each match, vim shows:\n"
                    "  y → yes, replace this one\n"
                    "  n → no, skip this one\n"
                    "  a → all, replace all remaining without asking\n"
                    "  q → quit, stop the substitution\n"
                    "  l → last, replace this one and stop\n"
                    "  Ctrl+E / Ctrl+Y → scroll to see more context\n\n"
                    "The confirm flag is essential when you can't use a pattern\n"
                    "precise enough to match only what you want — it lets you\n"
                    "review each match and decide individually."
                ),
                "answer": "c",
                "hints": ["The flag that means 'confirm'.", "Single letter, appended after 'g'.", "The answer is: c"],
            },
        ],
    },
    "motion_objects": {
        "id": "motion_objects",
        "name": "Motion & Text Objects",
        "subtitle": "The Grammar That Makes Vim Fast",
        "color": "cyan",
        "icon": "🎯",
        "commands": ["ciw/diw", "ci\"/di\"", "da(", "yap", "f/t/F/T", "%"],
        "challenges": [
            {
                "id": "mot_1",
                "type": "fill_blank",
                "title": "Change Inner Word",
                "flavor": "The cursor is somewhere on the word 'phantom'. You want to delete the entire word and type a replacement, without moving to the start of the word first. What command does this?",
                "lesson": (
                    "ciw — change inner word: delete the whole word, enter insert mode.\n\n"
                    "Text object syntax: [operator][i/a][object]\n"
                    "  i = 'inner' (just the object, no surrounding space)\n"
                    "  a = 'around' (object + surrounding whitespace or delimiters)\n\n"
                    "  ciw   → change inner word (works regardless of cursor position within word)\n"
                    "  diw   → delete inner word\n"
                    "  yiw   → yank inner word\n"
                    "  caw   → change around word (includes trailing space)\n"
                    "  daw   → delete around word\n\n"
                    "The power: 'i' and 'a' modifiers make the operator cursor-position-independent.\n"
                    "ciw works whether your cursor is at the start, middle, or end of the word."
                ),
                "answer": "ciw",
                "hints": ["Change (c) + inner (i) + word (w).", "Three letters.", "The answer is: ciw"],
            },
            {
                "id": "mot_2",
                "type": "fill_blank",
                "title": "Change Inside Quotes",
                "flavor": "Config line: route = \"phantom_subsidiary\". Cursor is anywhere on the line. You need to replace the value inside the quotes. What command deletes everything between the quotes and enters insert mode?",
                "lesson": (
                    "ci\" — change inside double quotes.\n\n"
                    "  ci\"   → change inside double quotes (deletes content, keeps quotes)\n"
                    "  ca\"   → change around double quotes (deletes content AND quotes)\n"
                    "  di\"   → delete inside double quotes\n"
                    "  yi\"   → yank inside double quotes\n\n"
                    "Works for any delimiter:\n"
                    "  ci'   → inside single quotes\n"
                    "  ci(   → inside parentheses\n"
                    "  ci[   → inside square brackets\n"
                    "  ci{   → inside curly braces\n"
                    "  cit   → inside HTML/XML tags\n\n"
                    "The cursor doesn't need to be inside the quotes —\n"
                    "vim finds the nearest matching pair on the current line."
                ),
                "answer": "ci\"",
                "hints": ["Change (c) + inner (i) + double-quote (\").", "Three characters.", "The answer is: ci\""],
            },
            {
                "id": "mot_3",
                "type": "fill_blank",
                "title": "Delete Around Parentheses",
                "flavor": "The line contains a function call: process(phantom_data, 0x4A). You want to delete the parentheses AND everything inside them. What command does this?",
                "lesson": (
                    "da( — delete around parentheses: delete the parens AND their contents.\n\n"
                    "  di(   → delete INSIDE parentheses (keeps the parens)\n"
                    "  da(   → delete the parens AND everything inside them\n\n"
                    "Same pattern works for all paired delimiters:\n"
                    "  da[   → delete around square brackets\n"
                    "  da{   → delete around curly braces\n"
                    "  da\"   → delete around double quotes\n"
                    "  dat   → delete around XML/HTML tag\n\n"
                    "Note: da( and da) do the same thing — both refer to the paren pair.\n"
                    "Similarly: di(/di) are equivalent.\n\n"
                    "The 'a' (around) modifier includes the delimiters themselves.\n"
                    "The 'i' (inner) modifier excludes them."
                ),
                "answer": "da(",
                "hints": ["Delete (d) + around (a) + open-paren (()", "Three characters.", "The answer is: da("],
            },
            {
                "id": "mot_4",
                "type": "quiz",
                "title": "Jump to Character",
                "flavor": "The cursor is at the start of the line. You need to move the cursor TO the first comma on the line (landing ON the comma). What key does this?",
                "lesson": (
                    "f{char} — move forward to the next occurrence of a character on the line.\n\n"
                    "  f,   → jump forward to the next comma, landing ON it\n"
                    "  t,   → jump forward to just BEFORE the next comma (till)\n"
                    "  F,   → jump backward to the previous comma (landing on it)\n"
                    "  T,   → jump backward to just after the previous comma\n\n"
                    "Repeating:\n"
                    "  ;    → repeat the last f/t/F/T in the same direction\n"
                    "  ,    → repeat in the opposite direction\n\n"
                    "f vs t:\n"
                    "  f goes TO the character (lands on it)\n"
                    "  t goes TILL the character (stops one before)\n"
                    "  t is useful for delete: dt, deletes everything up to (not including) the comma"
                ),
                "answer": "f",
                "hints": ["Think: 'find' a character on the line.", "Single lowercase letter.", "The answer is: f"],
            },
            {
                "id": "mot_5",
                "type": "quiz",
                "title": "Jump to Matching Bracket",
                "flavor": "The cursor is on an opening parenthesis in a complex nested expression. What key jumps to the matching closing parenthesis?",
                "lesson": (
                    "% — jump to the matching bracket, parenthesis, or brace.\n\n"
                    "  %   → jump to the matching ), ], or }\n"
                    "        (also works in reverse: on ), jumps to matching ()\n\n"
                    "Supported pairs:\n"
                    "  () → parentheses\n"
                    "  [] → square brackets\n"
                    "  {} → curly braces\n\n"
                    "Useful for:\n"
                    "  - Verifying nested structures are balanced\n"
                    "  - Selecting a block: v% selects from here to the matching bracket\n"
                    "  - d% deletes from cursor to matching bracket (inclusive)\n\n"
                    "Can also jump between #if/#endif and other matched language constructs\n"
                    "if the matchit plugin is loaded (included with most vim distributions)."
                ),
                "answer": "%",
                "hints": ["The key that means 'percentage' — also used for jump to match.", "The % key.", "The answer is: %"],
            },
            {
                "id": "mot_6",
                "type": "fill_blank",
                "is_boss": True,
                "title": "Boss: Yank a Paragraph",
                "flavor": "The config file has a block of settings separated by blank lines (a paragraph). You need to copy the entire current paragraph. What command yanks the current paragraph as a text object?",
                "lesson": (
                    "yap — yank around paragraph.\n\n"
                    "Paragraph text object:\n"
                    "  ip  → inner paragraph (the text, not the surrounding blank lines)\n"
                    "  ap  → around paragraph (the text AND surrounding blank lines)\n\n"
                    "  yip  → yank inner paragraph\n"
                    "  yap  → yank around paragraph (includes surrounding blank lines)\n"
                    "  dip  → delete inner paragraph\n"
                    "  dap  → delete around paragraph\n"
                    "  cip  → change inner paragraph\n\n"
                    "What counts as a paragraph:\n"
                    "  - A block of non-empty lines, bounded by blank lines or file edges\n"
                    "  - Same definition as in prose writing\n\n"
                    "After yap, you can move to another location and paste with p or P."
                ),
                "answer": "yap",
                "hints": ["Yank (y) + around (a) + paragraph (p).", "Three letters.", "The answer is: yap"],
            },
        ],
    },
    "split_network": {
        "id": "split_network",
        "name": "The Split Network",
        "subtitle": "Splits, Buffers & Multi-File Sessions",
        "color": "blue",
        "icon": "🪟",
        "commands": [":vs/:sp", "Ctrl+W nav", ":ls/:b", ":tabnew", "buffers"],
        "challenges": [
            {
                "id": "splt_1",
                "type": "fill_blank",
                "title": "Navigate to Left Split",
                "flavor": "You have two vertical splits open. Your cursor is in the right pane. Move to the left pane. Complete: Ctrl+W ___",
                "lesson": (
                    "Ctrl+W h — move to the split on the left.\n\n"
                    "Split navigation uses the same hjkl keys as cursor movement:\n"
                    "  Ctrl+W h   → move to split on the LEFT\n"
                    "  Ctrl+W l   → move to split on the RIGHT\n"
                    "  Ctrl+W j   → move to split BELOW\n"
                    "  Ctrl+W k   → move to split ABOVE\n"
                    "  Ctrl+W w   → cycle to the next split (clockwise)\n"
                    "  Ctrl+W W   → cycle to the previous split (counterclockwise)\n\n"
                    "Creating splits:\n"
                    "  :vs   → vertical split (current or new file)\n"
                    "  :sp   → horizontal split\n"
                    "  Ctrl+W v  → vertical split current buffer\n"
                    "  Ctrl+W s  → horizontal split current buffer\n\n"
                    "Closing splits:\n"
                    "  :q     → close current split\n"
                    "  Ctrl+W c  → close current split\n"
                    "  Ctrl+W o  → close ALL other splits (only keep current)"
                ),
                "answer": "h",
                "hints": ["Same as cursor movement: h is left.", "The answer is: h"],
            },
            {
                "id": "splt_2",
                "type": "quiz",
                "title": "List Open Buffers",
                "flavor": "You have several files open in this vim session and need to see the full list. What command lists all open buffers?",
                "lesson": (
                    ":ls — list all open buffers.\n\n"
                    "Output format:\n"
                    "  1  %a  \"file1.txt\"     line 12\n"
                    "  2  #   \"file2.conf\"    line 1\n"
                    "  3      \"file3.log\"     line 1\n\n"
                    "Status flags:\n"
                    "  %  → current buffer\n"
                    "  #  → alternate buffer (last visited; Ctrl+^ switches to it)\n"
                    "  a  → active (loaded and visible)\n"
                    "  h  → hidden (loaded but not displayed)\n"
                    "  +  → modified (unsaved changes)\n\n"
                    "Navigating buffers:\n"
                    "  :b N     → switch to buffer N\n"
                    "  :b name  → switch to buffer matching 'name'\n"
                    "  :bnext   → next buffer\n"
                    "  :bprev   → previous buffer\n"
                    "  Ctrl+^   → toggle between current and alternate buffer (:b #)"
                ),
                "answer": "ls",
                "hints": ["Same as the Unix command for listing — but prefixed with ':'.", "The answer is: ls"],
            },
            {
                "id": "splt_3",
                "type": "fill_blank",
                "title": "Switch to Buffer",
                "flavor": "You see from :ls that the audit log is buffer 3. Switch to it. Complete: :b ___",
                "lesson": (
                    ":b N — switch to buffer number N.\n\n"
                    "  :b 3     → switch to buffer 3\n"
                    "  :b file  → switch to buffer matching 'file' (partial name OK)\n"
                    "  :b#      → switch to the alternate buffer (same as Ctrl+^)\n\n"
                    "Buffer deletion:\n"
                    "  :bd N    → delete (close) buffer N\n"
                    "  :bda     → delete all buffers\n\n"
                    "Viewing multiple buffers simultaneously:\n"
                    "  :ba      → open all buffers in splits\n"
                    "  :vert ba → open all buffers in vertical splits\n\n"
                    "The alternate buffer (marked with # in :ls) is the last buffer\n"
                    "you were in before the current one. Ctrl+^ is the fastest way\n"
                    "to toggle between two files."
                ),
                "answer": "3",
                "hints": ["Just the buffer number.", "The answer is: 3"],
            },
            {
                "id": "splt_4",
                "type": "fill_blank",
                "title": "Equalize Split Sizes",
                "flavor": "Your splits have become uneven after resizing. You need to equalize them all. Complete: Ctrl+W ___",
                "lesson": (
                    "Ctrl+W = — equalize the sizes of all open splits.\n\n"
                    "Resize operations:\n"
                    "  Ctrl+W =   → make all windows equal size\n"
                    "  Ctrl+W >   → increase width of current window by 1\n"
                    "  Ctrl+W <   → decrease width by 1\n"
                    "  Ctrl+W +   → increase height by 1\n"
                    "  Ctrl+W -   → decrease height by 1\n"
                    "  N Ctrl+W > → increase width by N\n\n"
                    "Set exact size:\n"
                    "  :vertical resize 80   → set current window to 80 columns\n"
                    "  :resize 40            → set current window to 40 lines\n\n"
                    "Maximize current window:\n"
                    "  Ctrl+W |   → maximize width\n"
                    "  Ctrl+W _   → maximize height\n"
                    "  Ctrl+W |   then Ctrl+W _ → maximize both"
                ),
                "answer": "=",
                "hints": ["The key that means 'equalize'.", "The = key.", "The answer is: ="],
            },
            {
                "id": "splt_5",
                "type": "fill_blank",
                "title": "Open New Tab",
                "flavor": "You want to open a completely separate workspace (new tab) for a different file. Complete the command: :___",
                "lesson": (
                    ":tabnew — open a new tab.\n\n"
                    "  :tabnew           → open a new empty tab\n"
                    "  :tabnew filename  → open a file in a new tab\n"
                    "  :tabedit file     → same as :tabnew file\n\n"
                    "Tab navigation:\n"
                    "  gt    → go to next tab (in normal mode)\n"
                    "  gT    → go to previous tab\n"
                    "  N gt  → go to tab N\n"
                    "  :tabclose → close current tab\n"
                    "  :tabonly  → close all other tabs\n\n"
                    "Tabs vs splits:\n"
                    "  Splits: multiple files visible simultaneously in one window\n"
                    "  Tabs: separate 'pages', each can contain their own set of splits\n\n"
                    "Use splits for files you're actively cross-referencing,\n"
                    "tabs for distinct tasks or contexts."
                ),
                "answer": "tabnew",
                "hints": ["The command that creates a new tab.", "The answer is: tabnew"],
            },
            {
                "id": "splt_6",
                "type": "fill_blank",
                "is_boss": True,
                "title": "Boss: Close Other Splits",
                "flavor": "You only need the current file now. Close all other splits but keep the current one. Complete: Ctrl+W ___",
                "lesson": (
                    "Ctrl+W o — close all OTHER splits, keep only the current one.\n\n"
                    "  Ctrl+W o   → 'only' — close all other windows\n"
                    "  :only      → same effect via command line\n\n"
                    "This is useful after doing cross-file reference work in splits —\n"
                    "you've found what you needed, now return to single-file focus.\n\n"
                    "Compare:\n"
                    "  Ctrl+W c   → close the CURRENT window (keep the others)\n"
                    "  Ctrl+W o   → keep the current, close ALL OTHERS\n"
                    "  :q         → close current window (same as Ctrl+W c in a split)"
                ),
                "answer": "o",
                "hints": ["Think: 'only' — keep only the current split.", "Single letter: the 'only' command.", "The answer is: o"],
            },
        ],
    },
    "macro_forge": {
        "id": "macro_forge",
        "name": "The Macro Forge",
        "subtitle": "Macros, Registers & Repeating Operations",
        "color": "red",
        "icon": "⚙️",
        "commands": ["q{reg}", "@{reg}", "@@", ":%normal", "registers"],
        "challenges": [
            {
                "id": "mac_1",
                "type": "fill_blank",
                "title": "Start Recording a Macro",
                "flavor": "You need to record a macro into register 'a'. What key sequence starts recording?",
                "lesson": (
                    "q{register} — start recording a macro.\n\n"
                    "  qa  → start recording into register 'a'\n"
                    "  qb  → start recording into register 'b'\n"
                    "  q   → stop recording (press q again when done)\n\n"
                    "While recording:\n"
                    "  - Every normal mode command, insert mode action, and\n"
                    "    command-line command is captured\n"
                    "  - The recording indicator appears in the status bar: 'recording @a'\n"
                    "  - Press q to stop\n\n"
                    "Registers: macros are stored in named registers (a-z, 0-9, etc.)\n"
                    "  - Lowercase (qa): overwrites the register\n"
                    "  - Uppercase (qA): appends to the register\n\n"
                    "Plan your macro before recording: make sure it ends in a position\n"
                    "where it can be replayed from (e.g., move to the next line at the end)."
                ),
                "answer": "qa",
                "hints": ["q starts recording, then the register name.", "The answer is: qa"],
            },
            {
                "id": "mac_2",
                "type": "fill_blank",
                "title": "Stop Recording",
                "flavor": "You've completed the actions for your macro. What key stops the recording?",
                "lesson": (
                    "q — press q (in normal mode) to stop recording a macro.\n\n"
                    "The recording flow:\n"
                    "  1. qa  → start recording into register 'a'\n"
                    "  2. ... perform the actions ...\n"
                    "  3. q   → stop recording\n\n"
                    "The same 'q' key both starts and stops recording:\n"
                    "  - Without an active recording: q{register} starts recording\n"
                    "  - During active recording: q stops recording\n\n"
                    "Common mistake: pressing q while in insert mode doesn't stop\n"
                    "the recording — it types the letter 'q' instead.\n"
                    "Make sure you're in normal mode before pressing q to stop."
                ),
                "answer": "q",
                "hints": ["The same key used to start recording — pressed again.", "Single letter.", "The answer is: q"],
            },
            {
                "id": "mac_3",
                "type": "fill_blank",
                "title": "Play a Macro",
                "flavor": "Your macro is in register 'a'. You need to run it once. What key sequence plays the macro?",
                "lesson": (
                    "@{register} — play (execute) a macro from a register.\n\n"
                    "  @a    → execute the macro stored in register 'a'\n"
                    "  @b    → execute the macro stored in register 'b'\n"
                    "  @@    → re-execute the last macro (whatever @a/@b was)\n\n"
                    "Repeating:\n"
                    "  10@a  → execute the macro 10 times\n"
                    "  416@a → execute 416 times (for that routing table...)\n\n"
                    "If the macro fails on a line (e.g., pattern not found),\n"
                    "execution stops. This is useful: it means a macro with a\n"
                    "search will automatically stop when it runs out of matches."
                ),
                "answer": "@a",
                "hints": ["@ followed by the register name.", "The answer is: @a"],
            },
            {
                "id": "mac_4",
                "type": "fill_blank",
                "title": "Replay Last Macro",
                "flavor": "You just ran @a and need to run it again immediately. What shortcut replays the most recently executed macro?",
                "lesson": (
                    "@@ — replay the last executed macro.\n\n"
                    "  @@    → repeat the last @{register} call\n"
                    "  10@@  → repeat the last macro 10 more times\n\n"
                    "Relationship to the . command:\n"
                    "  .     → repeat the last single normal-mode change\n"
                    "  @@    → repeat the last macro (which may contain many changes)\n\n"
                    "The @@ shortcut is useful for:\n"
                    "  - Running a macro on multiple non-contiguous lines\n"
                    "    (move to each line, @@ to apply)\n"
                    "  - Quick repeated application without remembering which register\n\n"
                    "@@@ doesn't exist — only @@ for repeating."
                ),
                "answer": "@@",
                "hints": ["Double @ — repeats the last macro.", "The answer is: @@"],
            },
            {
                "id": "mac_5",
                "type": "fill_blank",
                "title": "Apply Macro to All Lines",
                "flavor": "Macro 'a' annotates a transaction line. You want to apply it to every line in the file. Complete the command: :___normal @a",
                "lesson": (
                    ":% normal @a — apply a macro to every line in the file.\n\n"
                    "  :%normal @a   → run macro 'a' on every line in the file\n"
                    "  :5,20normal @a → run macro 'a' on lines 5 through 20\n"
                    "  :'<,'>normal @a → run macro 'a' on the visual selection\n\n"
                    "The :normal command executes normal-mode keystrokes for each\n"
                    "line in the range.\n\n"
                    "Other :normal uses:\n"
                    "  :%normal A;   → append semicolon to end of every line\n"
                    "  :%normal I//  → prepend // (comment) to every line\n"
                    "  :5,10normal dd → delete lines 5-10 one by one\n\n"
                    "This is one of the most powerful vim idioms: combining ranges\n"
                    "with :normal to apply any normal-mode operation to many lines."
                ),
                "answer": "%",
                "hints": ["The address meaning 'all lines'.", "The answer is: %"],
            },
            {
                "id": "mac_6",
                "type": "fill_blank",
                "is_boss": True,
                "title": "Boss: Run Macro N Times",
                "flavor": "The routing table has 417 flagged entries and your macro handles one at a time. Run the macro in register 'a' exactly 417 times with a single command. What do you type?",
                "lesson": (
                    "N@{register} — run a macro N times.\n\n"
                    "  417@a  → run the macro in register 'a' exactly 417 times\n\n"
                    "This is the core power of macros: record once, run thousands of times.\n\n"
                    "What happens on failure:\n"
                    "  If the macro fails on any iteration (e.g., a search finds no match),\n"
                    "  execution stops at that point. This is intentional — it means\n"
                    "  your macro will naturally stop when it's processed all valid lines.\n\n"
                    "A well-written macro should:\n"
                    "  1. Perform the transformation on the current line/position\n"
                    "  2. End by moving to the next position (e.g., j to go down)\n"
                    "  3. So that replaying it from the new position does the next item"
                ),
                "answer": "417@a",
                "hints": ["The count goes before the @register.", "417 followed by @a.", "The answer is: 417@a"],
            },
        ],
    },
}

ZONE_ORDER = [
    "normal_vault",
    "insert_protocol",
    "command_line",
    "visual_mode",
    "search_engine",
    "motion_objects",
    "split_network",
    "macro_forge",
]
