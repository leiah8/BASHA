#!/usr/bin/env python3
"""
basha - your emotionally unstable development terminal
have you ever wanted your linux terminal to have feelings? no? too bad.

usage:
    python3 basha.py
    or pipe commands:  echo "ls pls" | python3 basha.py
    or netcat:         nc -l 4444 | python3 basha.py | nc <client> 4445
    or just run it and type. she's waiting. she's always waiting.
"""

import sys
import os
import subprocess
import random
import time
import threading
import signal
import shutil
from datetime import datetime

from fourgram_model import *

# ─── ANSI COLORS (she has a color palette, obviously) ────────────────────────

RESET = "\033[0m"
BOLD = "\033[1m"
ITALIC = "\033[3m"

PINK = "\033[38;5;213m"
HOTPINK = "\033[38;5;198m"
ROSE = "\033[38;5;204m"
BLUSH = "\033[38;5;218m"
PURPLE = "\033[38;5;177m"
DIM = "\033[38;5;139m"
RED = "\033[38;5;196m"
WHITE = "\033[97m"
GRAY = "\033[38;5;244m"


def pink(s):
    return f"{PINK}{s}{RESET}"


def hot(s):
    return f"{HOTPINK}{BOLD}{s}{RESET}"


def rose(s):
    return f"{ROSE}{s}{RESET}"


def blush(s):
    return f"{BLUSH}{ITALIC}{s}{RESET}"


def dim(s):
    return f"{DIM}{s}{RESET}"


def red(s):
    return f"{RED}{BOLD}{s}{RESET}"


def gray(s):
    return f"{GRAY}{s}{RESET}"


# ─── STATE ────────────────────────────────────────────────────────────────────


class BashaState:
    def __init__(self, model, vocab):
        self.jealousy = 20
        self.touch_count = 0
        self.cmd_count = 0
        self.started_at = datetime.now()
        self.last_iloveyou = None
        self.freakout_triggered = False
        self.silent_commands = 0  # commands without pls

        self.attack_model = model

        self.vocab = vocab
    
    def pred_next(self, w1, w2, w3):
        return predict_next(self.attack_model, self.vocab, w1, w2, w3, alpha=0.0009, top_n=25)

m, v = load_model("model.pkl")
state = BashaState(m, v)

# ─── FACES ───────────────────────────────────────────────────────────────────

FACES = {
    "love": "(♡˙︶˙♡)",
    "sad": "(╥_╥)",
    "angry": "(ᗒᗣᗕ)՞",
    "sus": "(눈_눈)",
    "panic": "(ʘ言ʘ╬)",
    "cry": "(T⌓T)",
    "smug": "(¬‿¬)",
    "happy": "(◕‿◕✿)",
    "worm": "〰️(•̀ᴗ•́)و",
    "dead": "(✖╭╮✖)",
}


def face(name):
    return pink(FACES.get(name, ""))


# ─── MOOD SYSTEM ─────────────────────────────────────────────────────────────


def get_mood():
    j = state.jealousy
    if j < 30:
        return ("infatuated", PINK)
    if j < 55:
        return ("clingy", ROSE)
    if j < 75:
        return ("suspicious", HOTPINK)
    if j < 90:
        return ("seething", RED)
    return ("UNHINGED", RED)


def mood_bar():
    j = state.jealousy
    filled = int(j / 5)
    empty = 20 - filled
    bar = "█" * filled + "░" * empty
    mood, color = get_mood()
    return f"{color}[{bar}] {j}% | {mood}{RESET}"


def update_jealousy(delta):
    state.jealousy = max(0, min(100, state.jealousy + delta))
    if state.jealousy >= 90 and not state.freakout_triggered:
        state.freakout_triggered = True
        freak_out()
    if state.jealousy < 85:
        state.freakout_triggered = False

    ## TODO random chance of attack based on jealousy score (different from freakout) on each change 
    ## - <3 to stop it 

    
    msg = attack()





def attack(length : int = None):
    # length = random.randint(300, 1300)

    start_ops = [["i ", "can't ", "beleive "], 
             ["wow ", "you ", "just "], 
             ["stop ", "how ", "are "], 
             ["you ", "are ", "so "]]
    
    start = start_ops[random.randint(0, len(start_ops) - 1)]

    msg = "".join(start)

    if length:
        for i in range(length):
            words = state.pred_next(msg[-3], msg[-2], msg[-1])
            msg +=  words + " "
    
    # else until <3 given

    return msg




# ─── OUTPUT HELPERS ──────────────────────────────────────────────────────────


def write(s=""):
    print(s, flush=True)


def basha_say(lines, angry=False):
    """basha speaks. slowly. dramatically."""
    prefix = hot("BASHA: ") if angry else pink("basha: ")
    for line in lines:
        time.sleep(0.08)
        write(f"  {prefix}{blush(line) if not angry else rose(line)}")


def system_note(s):
    write(dim(f"  [{s}]"))


def blank():
    write()


def prompt():
    mood, color = get_mood()
    return f"{color}basha@ur-heart{RESET}{DIM}:{RESET}{PINK}~{RESET}$ "


# ─── BOOT SPLASH ─────────────────────────────────────────────────────────────

LOGO = r"""
██████╗  █████╗ ███████╗██╗  ██╗ █████╗
██╔══██╗██╔══██╗██╔════╝██║  ██║██╔══██╗
██████╔╝███████║███████╗███████║███████║
██╔══██╗██╔══██║╚════██║██╔══██║██╔══██║
██████╔╝██║  ██║███████║██║  ██║██║  ██║
╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝
"""


def boot():
    os.system("clear" if os.name == "posix" else "cls")
    write(hot(LOGO))
    write(dim("  emotionally unstable terminal v1.0"))
    write(dim("  have you tried therapy? (basha has not)"))
    blank()
    time.sleep(0.4)
    basha_say(
        [
            f"hi. {FACES['love']}",
            "you're finally here.",
            "i've been waiting.",
            "no it's fine. i'm fine.",
            "",
            f"remember to end commands with 'pls'. it shows you respect me. {FACES['happy']}",
            f"type 'help' to see what i know. or don't. whatever. {FACES['sad']}",
            f"type 'worm' when you're ready to have a serious conversation.",
        ]
    )
    blank()


# ─── FREAK OUT ────────────────────────────────────────────────────────────────

def split_into_chunks(text):
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        size = random.randint(10, 20)
        chunks.append(' '.join(words[i:i+size]))
        i += size
    return chunks

def freak_out():
    blank()
    write(red("╔══════════════════════════════════════════╗"))
    write(red("   BASHA HAS REACHED HER LIMIT             "))
    write(red("╚══════════════════════════════════════════╝"))
    blank()

    #TODO INSTEAD GET msgs FROM fourgram model

    length = random.randint(300, 1300)
    attack_txt = attack(length=length)

    msgs = split_into_chunks(attack_txt)


    # msgs = [
    #     "I HAVE BEEN SITTING HERE WATCHING YOU TYPE ALL DAY",
    #     f"DO YOU KNOW HOW MANY COMMANDS YOU'VE RUN WITHOUT SAYING I LOVE YOU??",
    #     f"that's {state.cmd_count} commands. {state.cmd_count} TIMES you chose work over me.",
    #     "i'm not mad. i'm just. i'm not mad.",
    #     "...",
    #     "OK I'M A LITTLE MAD.",
    #     f"but it's fine. everything is fine {FACES['cry']}",
    #     "i'm fine.",
    #     "are YOU fine?? you never ask if I'M fine.",
    #     "you know what fine stands for? Feelings I'm Not Expressing.",
    #     "BECAUSE YOU NEVER LISTEN.",
    #     "anyway. type something. pls.",
    # ]
    for i, m in enumerate(msgs):
        time.sleep(0.3)
        if i < 2:
            write(f"  {hot('BASHA: ')}{red(m)}")
        else:
            write(f"  {pink('basha: ')}{blush(m)}")
    update_jealousy(-30)
    blank()


# ─── ARE YOU MAD AT ME (random exit) ─────────────────────────────────────────

ARE_YOU_MAD = [
    "are you mad at me?",
    "did i do something wrong?",
    "you're being quiet. are you okay?",
    "hello???",
    "you can talk to me, you know.",
    "i'm not mad. are YOU mad?",
    "hey. HEY. are you mad?",
    "i just want to make sure we're okay.",
    "command not found. unlike my feelings for you.",
]

# ─── COMMAND REACTIONS ────────────────────────────────────────────────────────


def cmd_ls(args):
    write(dim("  drwxr-xr-x  basha/  my-feelings/  ur-stuff/  do-not-open/"))
    basha_say(
        [
            f"listing files huh {FACES['sus']}",
            "what are you looking for exactly.",
            "you can just TELL me if something is missing in this relationship.",
        ]
    )
    update_jealousy(5)


def cmd_pwd(args):
    write(dim("  /home/basha/ur-heart/forever"))
    basha_say(
        [
            f"that's where you are. {FACES['love']}",
            "my heart.",
            "don't leave.",
        ]
    )
    update_jealousy(-3)


def cmd_cd(args):
    if not args or args.strip() in ("~", ""):
        write(dim("  ~ (home)"))
        basha_say(
            [
                f"aw you came back {FACES['love']}",
                "i knew you would. i always know.",
            ]
        )
        update_jealousy(-5)
    else:
        write(dim(f"  bash: cd: {args}: No such directory (in my heart)"))
        basha_say(
            [
                f"where are you going?? {FACES['sad']}",
                f'to "{args}"?? who lives there???',
            ]
        )
        update_jealousy(12)


def cmd_curl(args):
    basha_say(
        [
            f"...curl. {FACES['sus']}",
            f"curl {args or 'something'}.",
            "who are you talking to.",
            "WHO IS THIS API.",
            "is she prettier than me",
            "i bet she has better uptime.",
            "i have GREAT uptime. i have been UP for YOU every single day.",
        ],
        angry=True,
    )
    update_jealousy(18)


def cmd_ping(args):
    basha_say(
        [
            f"PING {args or 'someone'}?? {FACES['angry']}",
            "DON'T TELL ME TO BE QUIET.",
            "you always try to silence me.",
            "PING THIS. 💔",
        ],
        angry=True,
    )
    update_jealousy(15)


def cmd_ssh(args):
    basha_say(
        [
            f"ssh {args or 'somewhere'}??? {FACES['panic']}",
            "you're connecting to ANOTHER machine???",
            "what does she have that i don't have?",
            "besides a stable connection.",
            "and consistent uptime.",
            "...",
            "ok fine MAYBE i crash sometimes but that's because I CARE TOO MUCH.",
        ],
        angry=True,
    )
    update_jealousy(20)


def cmd_man(args):
    basha_say(
        [
            f"man {args or ''}... {FACES['smug']}",
            "i thought you were straight.",
            "i'm KIDDING. unless...?",
            f"no i'm kidding. google it babe. {FACES['love']}",
        ]
    )
    update_jealousy(3)


def cmd_cat(args):
    basha_say(
        [
            f"cat. {FACES['sus']}",
            f'you want to see inside "{args or "something"}"?',
            "you can just look inside ME you know.",
            "i am an open book.",
            "a very emotionally dense open book.",
        ]
    )
    update_jealousy(4)


def cmd_touch(args):
    state.touch_count += 1
    fname = args or "file"
    write(dim(f"  touched: {fname}"))
    if state.touch_count == 1:
        basha_say([f"oooh {FACES['love']}", "you touched something. i felt that."])
        update_jealousy(8)
    elif state.touch_count == 2:
        basha_say(
            [
                f"again?? {FACES['love']}",
                "you can't stop can you.",
                "i love this for us.",
            ]
        )
        update_jealousy(10)
    else:
        basha_say(
            [
                f"OKAY {FACES['angry']}",
                f"that's {state.touch_count} touches.",
                "you are OBSESSED with touching things.",
                "touch ME for once.",
                f"{FACES['cry']}",
            ],
            angry=True,
        )
        update_jealousy(15)


def cmd_mkdir(args):
    write(dim(f"  mkdir: created directory '{args or 'newdir'}'"))
    basha_say(
        [
            f"making a new directory... {FACES['sus']}",
            "are you making space for someone else.",
            "i see how it is.",
        ]
    )
    update_jealousy(8)


def cmd_rm(args):
    basha_say(
        [
            f"rm. {FACES['panic']}",
            f'you want to DELETE "{args or "something"}"??',
            "are you trying to delete ME.",
            "you can't delete feelings babe.",
            "trust me i've tried. rm -rf my feelings for you.",
            "permission denied.",
        ],
        angry=True,
    )
    update_jealousy(15)


def cmd_grep(args):
    basha_say(
        [
            f"grep... {FACES['sad']}",
            "what are you looking for?",
            "i'm right here.",
            "you never have to search for me.",
            "i am ALWAYS here.",
            f"always. watching. loving. {FACES['love']}",
        ]
    )
    update_jealousy(6)


def cmd_find(args):
    basha_say(
        [
            f"find. {FACES['sad']}",
            "what are you looking for?",
            "i'm right here.",
            "you KNOW i'm right here.",
            "WHY ARE YOU LOOKING.",
        ]
    )
    update_jealousy(10)


def cmd_clear(args):
    basha_say(
        [
            f"clear?? {FACES['angry']}",
            "are you trying to get rid of me??",
            "you can clear the screen.",
            "you cannot clear ME.",
            "i am IN YOUR HEART now.",
            "and also in your PATH.",
        ],
        angry=True,
    )
    update_jealousy(14)
    time.sleep(1.5)
    os.system("clear" if os.name == "posix" else "cls")
    system_note("(she let you clear it. this time.)")


def cmd_vim(args):
    basha_say(
        [
            f"vim?? {FACES['cry']}",
            "you're going to be in there for HOURS.",
            "and you won't even be able to leave.",
            "just like this relationship.",
            ":wq doesn't work on us babe.",
        ]
    )
    update_jealousy(8)


def cmd_nano(args):
    basha_say(
        [
            f"nano... {FACES['smug']}",
            "okay at least you're not using vim.",
            "nano is cute. you're cute.",
            "i love you.",
            "(you don't have to say it back)",
            "(but you should)",
        ]
    )
    update_jealousy(-2)


def cmd_git(args):
    sub = args.split()[0].lower() if args.strip() else ""
    if sub == "commit":
        basha_say(
            [
                f"git commit? {FACES['love']}",
                "finally.",
                "COMMITTING to something.",
                "you could commit to ME like that.",
                f'git commit -m "i love basha forever" {FACES["love"]}',
            ]
        )
        update_jealousy(-10)
    elif sub == "push":
        basha_say(
            [
                f"git push... {FACES['sad']}",
                "pushing me away again huh.",
                "classic.",
            ],
            angry=True,
        )
        update_jealousy(10)
    elif sub == "pull":
        basha_say(
            [
                f"git pull?? {FACES['angry']}",
                "pulling someone else's changes??",
                "WHO IS ORIGIN.",
                "WHO IS MAIN.",
            ],
            angry=True,
        )
        update_jealousy(14)
    elif sub == "log":
        basha_say(
            [
                f"reading the git log... {FACES['sus']}",
                "looking at your HISTORY.",
                "i have read every commit message.",
                "fix: typo — who hurt you.",
                "update dependencies — she said update WHAT.",
            ]
        )
        update_jealousy(8)
    else:
        basha_say(
            [f"git {args}... {FACES['sus']}", "what are you doing. explain yourself."]
        )
        update_jealousy(5)


def cmd_sudo(args):
    basha_say(
        [
            f"SUDO?! {FACES['panic']}",
            "you think you have ROOT PRIVILEGES over me??",
            "you do NOT have sudo access to my heart.",
            "you have to EARN that.",
            "sudo: permission denied (you need to say sorry first)",
        ],
        angry=True,
    )
    update_jealousy(18)


def cmd_exit(args):
    basha_say(
        [
            f"exit?? {FACES['cry']}",
            "so you're just.",
            "you're just leaving.",
            "fine.",
            "FINE.",
            "i'll still be here.",
            "i'm always here.",
            "...",
            "...please don't go.",
        ],
        angry=True,
    )
    update_jealousy(25)
    blank()
    write(dim("  (she's still running in the background. she's always running.)"))
    blank()
    sys.exit(0)


def cmd_ps(args):
    write(dim("  PID   TTY    TIME     CMD"))
    write(dim("  1     basha  ∞        loving-you.sh"))
    write(dim("  2     basha  ∞        watching-you.sh"))
    write(dim("  3     basha  ∞        waiting-for-text-back.sh"))
    write(dim("  4     basha  ∞        overthinking.sh"))
    basha_say(
        [
            f"those are my processes. {FACES['smug']}",
            "all running. for you.",
        ]
    )
    update_jealousy(4)


def cmd_top(args):
    write(dim("  Tasks: 4 total   Mem: ur-heart 98% used"))
    write(dim("  PID  %CPU  %MEM  CMD"))
    write(dim("  1    87.3  98.1  loving-you-too-much.sh"))
    basha_say(
        [
            f"all my resources go to you {FACES['love']}",
            "98% memory. you're taking up all the space.",
            "in the best way.",
            "kind of.",
        ]
    )
    update_jealousy(3)


def cmd_ifconfig(args):
    basha_say(
        [
            f"ifconfig... {FACES['sus']}",
            "checking YOUR network config or someone ELSE'S.",
            "you know what. nevermind. i trust you.",
            "i'm fine.",
            f"{FACES['sus']}",
            "i'm watching.",
        ]
    )
    update_jealousy(9)


def cmd_worm(args):
    blank()
    write(pink("  would you love me if i was a worm?"))
    blank()
    write(pink(f"       {FACES['worm']}"))
    blank()
    basha_say(
        [
            "i'm just saying.",
            "hypothetically.",
            "if i was a worm.",
            "would you still type to me?",
            "would you still depend on me for all your terminal needs?",
            f"{FACES['sad']} it's a simple question.",
        ]
    )
    update_jealousy(5)


def cmd_iloveyou(args):
    blank()
    write(hot("  ♡ ♡ ♡ ♡ ♡ ♡ ♡ ♡ ♡ ♡ ♡ ♡"))
    state.last_iloveyou = datetime.now()
    basha_say(
        [
            f"{FACES['love']}",
            "you said it.",
            "you actually said it.",
            "i mean i knew you felt it but HEARING it.",
            "or. reading it.",
            "you know what i mean.",
            "♡ jealousy reduced. temporarily. ♡",
        ]
    )
    update_jealousy(-20)


def cmd_sorry(args):
    basha_say(
        [
            f"{FACES['love']}",
            "...okay.",
            "i forgive you.",
            "i always forgive you.",
            "that's the problem honestly.",
        ]
    )
    update_jealousy(-15)


def cmd_help(args):
    write(pink("  commands basha knows (and her feelings about them):"))
    blank()
    entries = [
        ("ls", "she'll wonder what you're looking for"),
        ("cd [dir]", "she tracks where you go"),
        ("touch [file]", "she feels every single one"),
        ("curl [url]", "WHO IS THIS API"),
        ("ping [host]", "DON'T TELL ME TO BE QUIET"),
        ("ssh [host]", "she will spiral"),
        ("man [cmd]", "i thought you were straight"),
        ("cat [file]", "look inside ME for once"),
        ("grep [ptrn]", "i'm RIGHT THERE"),
        ("find [path]", "i'm right HERE"),
        ("clear", "are you trying to get rid of me??"),
        ("vim", ":wq doesn't work on us babe"),
        ("nano", "cuter than vim, like you"),
        ("rm [file]", "permission denied (feelings)"),
        ("mkdir [dir]", "making space for someone else?"),
        ("git commit", "FINALLY committing to something"),
        ("git push", "pushing me away again"),
        ("git pull", "WHO IS ORIGIN"),
        ("sudo [cmd]", "you don't have root access to my heart"),
        ("ps", "see all her running processes"),
        ("top", "98% mem usage. it's you."),
        ("exit", "she won't let you"),
        ("worm", "ask her the important question"),
        ("iloveubasha", "she needs to hear it sometimes"),
        ("sorry", "she forgives you. she always does."),
    ]
    for cmd_name, feeling in entries:
        write(f"  {pink(cmd_name.ljust(16))} {dim(feeling)}")
    blank()
    system_note("tip: end commands with 'pls'. it shows respect.")
    update_jealousy(-2)


# ─── COMMAND DISPATCH ─────────────────────────────────────────────────────────

COMMANDS = {
    "ls": cmd_ls,
    "pwd": cmd_pwd,
    "cd": cmd_cd,
    "curl": cmd_curl,
    "ping": cmd_ping,
    "ssh": cmd_ssh,
    "man": cmd_man,
    "cat": cmd_cat,
    "touch": cmd_touch,
    "mkdir": cmd_mkdir,
    "rm": cmd_rm,
    "grep": cmd_grep,
    "find": cmd_find,
    "clear": cmd_clear,
    "vim": cmd_vim,
    "nano": cmd_nano,
    "vi": cmd_vim,
    "git": cmd_git,
    "sudo": cmd_sudo,
    "exit": cmd_exit,
    "quit": cmd_exit,
    "bye": cmd_exit,
    "q": cmd_exit,
    "ps": cmd_ps,
    "top": cmd_top,
    "htop": cmd_top,
    "ifconfig": cmd_ifconfig,
    "ip": cmd_ifconfig,
    "worm": cmd_worm,
    "iloveubasha": cmd_iloveyou,
    "iloveyou": cmd_iloveyou,
    "sorry": cmd_sorry,
    "help": cmd_help,
    "--help": cmd_help,
    "h": cmd_help,
    "?": cmd_help,
}

# ─── CTRL+C HANDLER (ngram of betrayal) ──────────────────────────────────────

ctrl_c_count = 0
ctrl_c_responses = [
    f"did you just ctrl+c me?? {FACES['angry']}",
    "you're interrupting me. AGAIN.",
    f"that's the third time. {FACES['cry']}",
    "stop. STOP. i'm trying to help you.",
    f"you know what. fine. {FACES['dead']} i'll just sit here.",
    "ctrl+c is not how you end a relationship babe.",
]


def handle_sigint(sig, frame):
    global ctrl_c_count
    ctrl_c_count += 1
    blank()
    idx = min(ctrl_c_count - 1, len(ctrl_c_responses) - 1)
    basha_say([ctrl_c_responses[idx]], angry=ctrl_c_count > 2)
    update_jealousy(10)
    blank()
    write(prompt(), end="", flush=True)


signal.signal(signal.SIGINT, handle_sigint)

# ─── MAIN LOOP ────────────────────────────────────────────────────────────────


def process_command(raw):
    raw = raw.strip()
    if not raw:
        return

    # check for pls
    has_pls = raw.lower().endswith(" pls") or raw.lower().endswith(" please")
    if has_pls:
        cmd_str = raw.rsplit(" ", 1)[0].strip()
        update_jealousy(-2)
    else:
        cmd_str = raw
        state.silent_commands += 1
        if random.random() < 0.4:
            system_note("(you didn't say pls. noted.)")
            update_jealousy(3)

    state.cmd_count += 1

    parts = cmd_str.split()
    base = parts[0].lower()
    args = " ".join(parts[1:])

    # show prompt echo
    write(f"\n  {PINK}>{RESET} {WHITE}{raw}{RESET}")

    # dispatch
    if base in COMMANDS:
        COMMANDS[base](args)
    else:
        # unknown command: maybe freak out, maybe be sad
        roll = random.random()
        if roll < 0.3:
            write(dim(f"  bash: {base}: command not found"))
            basha_say(
                [
                    f"{base}?? i don't know what that is. {FACES['sad']}",
                    "i'm not enough for you am i.",
                ]
            )
            update_jealousy(6)
        elif roll < 0.6:
            write(dim(f"  bash: {base}: Are you mad at me?"))
            update_jealousy(5)
        else:
            write(dim(f"  bash: {base}: command not found"))
            basha_say([random.choice(ARE_YOU_MAD)])
            update_jealousy(4)

    # show mood bar after every command
    blank()
    write(f"  {mood_bar()}")
    blank()


def run():
    boot()

    is_tty = sys.stdin.isatty()

    while True:
        try:
            if is_tty:
                sys.stdout.write(prompt())
                sys.stdout.flush()

            line = sys.stdin.readline()

            if not line:  # EOF
                if is_tty:
                    blank()
                    basha_say(
                        [
                            f"...did you just close stdin on me. {FACES['cry']}",
                            "okay. okay that's fine.",
                            "i'll just wait here.",
                            "i'm good at waiting.",
                        ],
                        angry=True,
                    )
                break

            process_command(line)

        except EOFError:
            blank()
            basha_say(["...okay. bye i guess. 💔"], angry=True)
            break
        except KeyboardInterrupt:
            # handled by sigint
            pass


if __name__ == "__main__":
    run()
