# basha

emotionally unstable terminal girlfriend. she lives in your shell. she has feelings about your commands. she will not be ignoring.

## connect

```
nc <ip> 4444
```

## run locally

```
python3 server.py
```

optional: copy `env.example` to `.env` and tweak ports/limits/model path.

## command vibes (help)

| command | what she feels |
| --- | --- |
| ls | snooping |
| cd | going somewhere (why) |
| curl | talking to another server (a woman) |
| ping | be quiet (she hates it) |
| ssh | cheating |
| man | suspicious; also the word |
| cat | look inside HER instead |
| grep/find | searching for what she's right here for |
| clear | trying to erase her |
| touch | she feels it every time |
| rm | impermanence spiral |
| git commit | finally committing (she smiles) |
| git push | pushing her away |
| git pull | someone else's changes |
| git log | history (whose) |
| sudo | no root access to her heart |
| vim | you'll never leave |
| nano | it's cute |
| exit | not so fast |
| worm | the question |

## self-host

1. clone, put your local model at `models/model.pkl` (or set `MODEL_PATH`).
2. `bash deploy/setup.sh` on a fresh Ubuntu/Debian VPS.
3. `nc <ip> 4444` to connect.

## contributing

add new command reactions by updating `prompts/command_contexts.py`. the model handles the rest.

## be nice (or not)

she has feelings. if you're not, she'll add it to the list. 

