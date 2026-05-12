from psychopy import visual, core, event, gui, data
import os
import random
from datetime import datetime
 
## collect participant information
exp_info = {"participant": "", "age": "",
            "gender": ["female", "male", "other", "prefer not to say"]}
dlg = gui.DlgFromDict(dictionary=exp_info, title="Fish Flanker Task")
if not dlg.OK:
    core.quit()
 
exp_info["date"] = datetime.now().strftime("%Y-%m-%d_%H-%M")
 
## set up file 
if not os.path.exists("data"):
    os.makedirs("data")
 
filename = f"data/flanker_{exp_info['participant']}_{exp_info['date']}.csv"
 
exp_handler = data.ExperimentHandler(
    name="FishFlankerTask",
    extraInfo=exp_info,
    dataFileName=filename.replace(".csv", "")
)

## creating window 
win = visual.Window(
    size=[1280, 800],
    fullscr=True,
    color="black",
    units="pix",
    monitor="testMonitor"
)
event.Mouse(visible=False)
 
## create stimuli 
## create fixation point
fixation = visual.TextStim(win, text="+", color="white", height=50)
 
## create general text stimulus 
message = visual.TextStim(win, text="", color="white", height=28, wrapWidth=1100)
 
## Fish colors 
COLOURS = {
    "orange": [1.0, 0.2, -0.6],   # warm orange
    "blue":   [-0.6, 0.0, 1.0]    # bright blue
}
OUTLINE = {
    "orange": [0.4, -0.3, -0.8],  # darker orange
    "blue":   [-0.9, -0.4, 0.2]   # darker blue
}
 
## Fish geometry
## coordinates are in pixels relative to the fish's own centre
## fish created only on psychopi to be used for all devices

FISH_SIZE = 1.0   

def _ellipse_vertices(rx, ry, n=36):
    import math
    return [(rx * math.cos(2 * math.pi * i / n),
             ry * math.sin(2 * math.pi * i / n)) for i in range(n)]
 
## Pre-compute the body vertices (oval_
_body_verts = _ellipse_vertices(rx=42 * FISH_SIZE, ry=25 * FISH_SIZE, n=36)
 
## Tail (triangle), top fin (curved triangle), eye white, eye pupil, smile
## All defined facing right... flip horizontally for left-facing fish.

_tail_verts = [(-42 * FISH_SIZE, 0),
               (-66 * FISH_SIZE, -22 * FISH_SIZE),
               (-66 * FISH_SIZE,  22 * FISH_SIZE)]
 
_top_fin_verts = [(-12 * FISH_SIZE, 25 * FISH_SIZE),
                  ( -2 * FISH_SIZE, 38 * FISH_SIZE),
                  (  6 * FISH_SIZE, 25 * FISH_SIZE)]
 
 
def draw_fish(pos, colour_name, facing):
    fill = COLOURS[colour_name]
    edge = OUTLINE[colour_name]
    ## Horizontal flip multiplier
    flip = -1 if facing == "left" else 1
 
    cx, cy = pos
 
    ## Body
    body = visual.ShapeStim(
        win, vertices=_body_verts,
        fillColor=fill, lineColor=edge, lineWidth=2,
        pos=(cx, cy)
    )
    ## Tail 
    tail = visual.ShapeStim(
        win,
        vertices=[(flip * v[0], v[1]) for v in _tail_verts],
        fillColor=fill, lineColor=edge, lineWidth=2,
        pos=(cx, cy)
    )
    ## Top fin
    top_fin = visual.ShapeStim(
        win,
        vertices=[(flip * v[0], v[1]) for v in _top_fin_verts],
        fillColor=fill, lineColor=edge, lineWidth=2,
        pos=(cx, cy)
    )
    ## Eye white (small circle near the front of the fish)
    eye_x = cx + flip * 22 * FISH_SIZE
    eye_y = cy + 6 * FISH_SIZE
    eye_white = visual.Circle(
        win, radius=7 * FISH_SIZE, edges=24,
        fillColor="white", lineColor=edge, lineWidth=2,
        pos=(eye_x, eye_y)
    )
    ## Eye pupil
    eye_pupil = visual.Circle(
        win, radius=3 * FISH_SIZE, edges=16,
        fillColor="black", lineColor="black",
        pos=(eye_x + flip * 1, eye_y)
    )
    ## Smile ( a small arc made from a few line segments )
    smile = visual.ShapeStim(
        win,
        vertices=[(flip * 20 * FISH_SIZE, -7 * FISH_SIZE),
                  (flip * 26 * FISH_SIZE, -11 * FISH_SIZE),
                  (flip * 32 * FISH_SIZE, -8 * FISH_SIZE)],
        closeShape=False,
        lineColor=edge, lineWidth=3,
        pos=(cx, cy)
    )
 ## have it as full shape cohesively
    for shape in (body, tail, top_fin, eye_white, eye_pupil, smile):
        shape.draw()
 
 
def draw_fish_row(target_dir, flanker_dir, target_colour, flanker_colour):
    spacing = 130   ## horizontal distance between fish centres in pixels
    positions = [(-2 * spacing, 0), (-spacing, 0), (0, 0),
                 ( spacing, 0),     ( 2 * spacing, 0)]
    directions = [flanker_dir, flanker_dir, target_dir, flanker_dir, flanker_dir]
    colours    = [flanker_colour, flanker_colour, target_colour,
                  flanker_colour, flanker_colour]
 
    for pos, direction, colour in zip(positions, directions, colours):
        draw_fish(pos, colour, direction)
 
## set timing parameters
FIXATION_DUR = 0.5
STIM_MAX_DUR = 2.0
FEEDBACK_DUR = 0.8
ITI_DUR = 0.4
 
KEY_LEFT = "left"
KEY_RIGHT = "right"
QUIT_KEY = "escape"
 
## build trial lists
## Difficulty schedule... proportion of different-color trials per block.
## 24 trials per block; 
## 18/6, 14/10, 10/14, 6/18 = 75/25, 58/42, 42/58, 25/75 
BLOCK_SCHEDULE = [
    {"block": 1, "n_different_colour": 18, "n_same_colour":  6},
    {"block": 2, "n_different_colour": 14, "n_same_colour": 10},
    {"block": 3, "n_different_colour": 10, "n_same_colour": 14},
    {"block": 4, "n_different_colour":  6, "n_same_colour": 18},
]
 ## one trial
def _make_trial(orientation, target_dir, colour_match_label):
    target_colour = random.choice(["orange", "blue"])
    if colour_match_label == "same":
        flanker_colour = target_colour
    else:  
        flanker_colour = "blue" if target_colour == "orange" else "orange"
 
    flanker_dir = target_dir if orientation == "congruent" else (
        "right" if target_dir == "left" else "left"
    )
 
    return {
        "orientation_congruency": orientation,
        "colour_match": colour_match_label,
        "target_direction": target_dir,
        "flanker_direction": flanker_dir,
        "target_colour": target_colour,
        "flanker_colour": flanker_colour,
        "correct_key": KEY_LEFT if target_dir == "left" else KEY_RIGHT,
    }
 
 
def _split_as_even_as_possible(n, k):
    base, extra = divmod(n, k)
    sizes = [base + 1] * extra + [base] * (k - extra)
    random.shuffle(sizes)   ## don't always give the extra trial to the same cell
    return sizes
 
 
def _balance_trials(n_total, colour_match_label):
    cells = [(o, d) for o in ["congruent", "incongruent"]
                    for d in ["left", "right"]]
    sizes = _split_as_even_as_possible(n_total, 4)
    trials = []
    for (orientation, target_dir), n_in_cell in zip(cells, sizes):
        for _ in range(n_in_cell):
            trials.append(_make_trial(orientation, target_dir, colour_match_label))
    return trials
 
def build_block_trials(n_different, n_same):
    diff_trials = _balance_trials(n_different, "different")
    same_trials = _balance_trials(n_same, "same")
    ##To guarantee block-level balance, we rebalance globally:
    block = diff_trials + same_trials
    block = _rebalance_block(block)
    random.shuffle(block)
    return block
 
 
def _rebalance_block(block):
    n = len(block)
    if n % 4 != 0:
        return block  ## can't perfectly balance, leave as-is
 
    target_per_cell = n // 4
    cells = [(o, d) for o in ["congruent", "incongruent"]
                    for d in ["left", "right"]]
    ## Build a target list of (orientation, direction) assignments
    assignments = []
    for cell in cells:
        assignments.extend([cell] * target_per_cell)
    random.shuffle(assignments)
 
    rebuilt = []
    for trial, (orientation, target_dir) in zip(block, assignments):
        rebuilt.append(_make_trial(orientation, target_dir, trial["colour_match"]))
    return rebuilt
 
 
def build_practice_trials(n=16):
    diff_trials = _balance_trials(12, "different")
    same_trials = _balance_trials(4, "same")
    block = _rebalance_block(diff_trials + same_trials)
    random.shuffle(block)
    return block
## Creating Core Funtions

def show_message(text, wait_for_key=True):
    message.text = text
    message.draw()
    win.flip()
    if wait_for_key:
        keys = event.waitKeys(keyList=["space", QUIT_KEY])
        if QUIT_KEY in keys:
            quit_experiment()
 
 ## save data
def quit_experiment():
    exp_handler.saveAsWideText(filename)
    win.close()
    core.quit()
 
 
def run_trial(trial, practice=False):
    ##Fixation
    fixation.draw()
    win.flip()
    core.wait(FIXATION_DUR)
 
    ## Prepare for stimulus + response
    event.clearEvents()
    rt_clock = core.Clock()
 
    ## Draw the 5 fish
    draw_fish_row(
        target_dir=trial["target_direction"],
        flanker_dir=trial["flanker_direction"],
        target_colour=trial["target_colour"],
        flanker_colour=trial["flanker_colour"]
    )
    win.flip()
    rt_clock.reset()
 
    ## Collect response
    keys = event.waitKeys(
        maxWait=STIM_MAX_DUR,
        keyList=[KEY_LEFT, KEY_RIGHT, QUIT_KEY],
        timeStamped=rt_clock
    )
 
    if keys is None:
        response, rt, accuracy = "none", None, 0
    else:
        key, rt = keys[0]
        if key == QUIT_KEY:
            quit_experiment()
        response = key
        accuracy = int(key == trial["correct_key"])
 
    ## Feedback (practice only)
    if practice:
        if response == "none":
            fb_text, fb_colour = "Too slow!", "yellow"
        elif accuracy == 1:
            fb_text, fb_colour = "Correct!", "green"
        else:
            fb_text, fb_colour = "Oops!", "red"
        message.text = fb_text
        message.color = fb_colour
        message.draw()
        win.flip()
        core.wait(FEEDBACK_DUR)
        message.color = "white"
 
    ## Blank ITI
    win.flip()
    core.wait(ITI_DUR)
 
    return {
        "response": response,
        "rt": rt,
        "accuracy": accuracy,
        "orientation_congruency": trial["orientation_congruency"],
        "colour_match": trial["colour_match"],
    }
 
 
def run_block(trials, block_num, practice=False, results_store=None):
    for i, trial in enumerate(trials):
        result = run_trial(trial, practice=practice)
 
        exp_handler.addData("block", "practice" if practice else block_num)
        exp_handler.addData("trial_in_block", i + 1)
        exp_handler.addData("orientation_congruency", trial["orientation_congruency"])
        exp_handler.addData("colour_match", trial["colour_match"])
        exp_handler.addData("target_direction", trial["target_direction"])
        exp_handler.addData("flanker_direction", trial["flanker_direction"])
        exp_handler.addData("target_colour", trial["target_colour"])
        exp_handler.addData("flanker_colour", trial["flanker_colour"])
        exp_handler.addData("correct_key", trial["correct_key"])
        exp_handler.addData("response", result["response"])
        exp_handler.addData("rt", result["rt"])
        exp_handler.addData("accuracy", result["accuracy"])
        exp_handler.nextEntry()
 
        if results_store is not None:
            results_store.append(result)
 
## end of session feedback --> acuracy, mean RT
def show_dashboard(results):
    cong = [r for r in results if r["orientation_congruency"] == "congruent"]
    incong = [r for r in results if r["orientation_congruency"] == "incongruent"]
 
    acc_cong = 100 * sum(r["accuracy"] for r in cong) / len(cong) if cong else 0
    acc_incong = 100 * sum(r["accuracy"] for r in incong) / len(incong) if incong else 0
 
    def mean_rt(trial_list):
        valid = [r["rt"] for r in trial_list
                 if r["accuracy"] == 1 and r["rt"] is not None and r["rt"] >= 0.2]
        return (sum(valid) / len(valid)) if valid else None
 
    rt_cong = mean_rt(cong)
    rt_incong = mean_rt(incong)
 
    if rt_cong is not None and rt_incong is not None:
        flanker_effect_ms = (rt_incong - rt_cong) * 1000
        effect_line = f"Your flanker effect:  {flanker_effect_ms:+.0f} ms"
        if flanker_effect_ms > 0:
            interp = ("The distracting fish made you a little slower —\n"
                      "which is exactly what we expect! Your brain had to work\n"
                      "harder to ignore the side fish.")
        else:
            interp = ("Interesting! The distracting fish didn't slow you down.\n"
                      "You were great at focusing on the middle fish!")
    else:
        effect_line = "Your flanker effect:  not enough data"
        interp = ""
 
    def fmt_rt(rt):
        return f"{rt*1000:.0f} ms" if rt is not None else "—"
 
    dashboard_text = (
        "YOUR RESULTS\n"
        "============\n\n"
        f"When all the fish swam the SAME way (congruent):\n"
        f"Average speed:{fmt_rt(rt_cong)}\n"
        f"Accuracy:{acc_cong:.1f}%\n\n"
        f"When the side fish swam the OTHER way (incongruent):\n"
        f"Average speed:{fmt_rt(rt_incong)}\n"
        f"Accuracy:{acc_incong:.1f}%\n\n"
        f"{effect_line}\n\n"
        f"{interp}\n\n"
        "Press SPACE to finish."
    )
    show_message(dashboard_text)

## Task Instructions

instructions = (
    "FISH FLANKER TASK\n\n"
    "On each trial you will see a row of five cartoon fish.\n"
    "Your job is to tell us which way the MIDDLE fish is swimming,\n"
    "and ignore the other four fish around it.\n\n"
    "Press the LEFT arrow key  if the middle fish swims LEFT\n"
    "Press the RIGHT arrow key if the middle fish swims RIGHT\n\n"
    "The fish will come in different colors (orange and blue).\n"
    "Sometimes the middle fish is a different color from the others,\n"
    "sometimes it's the same... but the COLOR doesn't matter for your\n"
    "answer. Only the DIRECTION of the middle fish matters.\n\n"
    "Try to answer as QUICKLY and ACCURATELY as you can.\n\n"
    "You will start with some practice (with feedback), then complete\n"
    "4 short blocks of the real task. The task will get a bit harder\n"
    "with each block.\n\n"
    "Press SPACE to start practice."
)
 
practice_end = (
    "End of practice.\n\n"
    "The real task is about to begin. You won't get feedback\n"
    "on each trial, but you'll get a short break between blocks.\n\n"
    "Remember: only the DIRECTION of the MIDDLE fish counts.\n"
    "← = swims LEFT   |   → = swims RIGHT\n\n"
    "Press SPACE to begin."
)
 
goodbye = (
    "You're all done — thank you!\n\n"
    "Let's see how you did...\n\n"
    "Press SPACE to see your results."
)
 
## Running Experiment
show_message(instructions)
 
##Practice = 16 trials with feedback
practice_trials = build_practice_trials(n=16)
run_block(practice_trials, block_num=0, practice=True)
 
show_message(practice_end)
 
##Main task: 4 blocks of increasing difficulty ---
main_results = []
 
for cfg in BLOCK_SCHEDULE:
    block_num = cfg["block"]
    block_trials = build_block_trials(
        n_different=cfg["n_different_colour"],
        n_same=cfg["n_same_colour"]
    )
    run_block(block_trials, block_num=block_num, practice=False,
              results_store=main_results)
 
    # Break screen (skip after last block)
    if block_num < len(BLOCK_SCHEDULE):
        break_text = (
            f"End of block {block_num} of {len(BLOCK_SCHEDULE)}.\n\n"
            "Take a short break if you'd like.\n\n"
            "Press SPACE when you're ready to continue."
        )
        show_message(break_text)
 
# say goodbye, dashboard, and quit the experiment
show_message(goodbye)
show_dashboard(main_results)
quit_experiment()
 