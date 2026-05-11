# Flanker-Test
The following repository is a complete experimental task examining selective attention and cognitive control using a child-friendly version of the Eriksen flanker task.
## The Flanker Task
The Eriksen flanker task is a classic paradigm in cognitive psychology used to measure selective attention and the ability to suppress responses to irrelevant information (Eriksen & Eriksen, 1974). On each trial, participants are shown a row of stimuli and must respond to the direction of the central target while ignoring the surrounding "flanker" stimuli.
There are two trial types: 
  1. **Congruent trials**: the flankers match the target (e.g., all arrows point in the same direction). These are easy because the flankers reinforce the correct response.
  2. **Incongruent trials**: the flankers conflict with the target (e.g., flankers point opposite to the target). These are harder, because the flankers activate a competing response that must be suppressed.

The difference in reaction time and accuracy between incongruent and congruent trials is called the flanker effect, and it serves as a behavioral measure of attentional control. Larger flanker effects suggest weaker selective attention; smaller flanker effects suggest stronger top-down control. The flanker task has been used widely in cognitive neuroscience, developmental psychology, and clinical research on conditions involving attention difficulties such as ADHD.

## Attention and Cognitive Control
The flanker task is widely used to assess two related constructs (1)  selective attention and (2) cognitive control. Selective attention refers to the ability to focus on task-relevant information while filtering out distractors. Cognitive control (also called executive control or inhibitory control) refers to the ability to override automatic or competing responses in favour of goal-directed behaviour. Together, these processes allow flexible, deliberate action in environments where irrelevant information competes for attention.

The flanker effect (the reaction-time cost imposed by incongruent flankers) provides a behavioral index of how efficiently a person can resolve this kind of perceptual and response conflict. Neuroimaging and electrophysiological studies have linked the resolution of flanker conflict to a network of frontal brain regions, particularly the anterior cingulate cortex, which is associated with conflict monitoring (Botvinick et al., 2001).

These attentional processes are clinically relevant. Atypical performance on flanker and related tasks has been reported in attention-deficit/hyperactivity disorder (ADHD), where deficits in selective attention and inhibitory control are core diagnostic features. The flanker task has also been used in developmental research to track the maturation of attention networks across childhood (Rueda et al., 2004), in ageing research to examine cognitive decline, and in clinical populations including anxiety and schizophrenia.

## Project Overview
The classic Eriksen flanker task uses letters or arrows, which are abstract and unappealing for younger participants. Rueda et al. (2004) addressed this by developing a child-friendly "fish flanker" version as part of the Attention Network Test, in which colorful cartoon fish replaced arrows. Their version has since become standard in developmental attention research and is included in the NIH Toolbox.

This project is a PsychoPy implementation of a child-friendly fish flanker, with three additions on top of the basic design:
 1. Cartoon fish are drawn procedurally in PsychoPy from geometric primitives (no external image files are needed).
 2. A color distractor manipulation is built into the design. On each trial the target and flanker fish are independently colored orange or blue. Sometimes the target matches the flankers' color, sometimes it does not. The proportion of "different-color" trials shifts across blocks, so the color cue becomes a less reliable aid as the task progresses.
 3. An end-of-session feedback dashboard computes the participant's personal flanker effect and presents their results in plain language.

## Experimental Design
### Variables
### Independent variables:
 1. Orientation congruency (congruent vs. incongruent) —> the standard flanker manipulation
 2. Color match (target colour same as vs. different from flankers) —>  a within-trial distractor that varies in proportion across blocks
 3. Blocks (1 to 4) —> represents progressively decreasing reliability of the color cue

### Dependent variables:
  1. Reaction time
  2. Accuracy (proportion correct)
  3. Flanker effect (mean RT on incongruent trials minus mean RT on congruent trials)

### Block Structure
 - 16 practice trials with trial-by-trial feedback (mostly different-color trials, to introduce the task gently)
 - 4 main blocks of 24 trials each (96 trials total)
 - Self-paced breaks between blocks

Within each main block, trials are  balanced on the main manipulations: 12 congruent / 12 incongruent, and 12 left-target / 12 right-target. What varies across blocks is the proportion of trials where the target color differs from the flanker color:

In block 1, there is 18 (75%) different-color trials and 6 (25%) same-color trials. This is the easiest as color usually helps locate the target. 

In block 2, there is 14 (48%) different-color trials and 10 (42%) same-color trials. Here, the color cue will be less reliable. 

In block 3, there is 10 (42%) different-color trials and 14 (58%) same-color trials. Here, the color cue rarely helps. 

In block 4, there is 6 (25%) different-color trials and 18 (75%) same-color trials. This is the most difficult condition. 

When the target and flankers share a color, the participant must rely entirely on orientation to identify the target, which we expect will produce a larger flanker effect. When colors differ, the target visually "pops out" and the flanker effect should shrink. Treating these block-level proportions as a fixed manipulation allows the task to be analyzed at the level of individual trial conditions or at the level of block.

### Parameters
The experiment was designed so that any of these parameters can be easily changed at the top of the script.

FIXATION_DUR = 0.5

STIM_MAX_DUR = 2.0

FEEDBACK_DUR = 0.8

ITI_DUR = 0.4

FISH_SIZE = 1.0

BLOCK_SCHEDULE = (refer back to block 1-4 descriptions)

## Parameter costumization (if changes wanted)
### Fixation Duration
The fixation cross is shown for 500 ms before each trial, controlled by the FIXATION_DUR parameter. This duration allows the participant to refocus on the centre of the screen. It can be lengthened if needed. 

### Stimulus Maximum Duration
The fish remain on screen for up to 2000 ms or until the participant responds, whichever comes first. This is controlled by STIM_MAX_DUR. Two seconds is a generous response window appropriate for younger or slower participants, but can be reduced (e.g., 1500 ms) for faster-paced testing or extended (e.g., 3000 ms) for participants with motor difficulties.

### Inter-trial Interval
A blank screen of 400 ms is shown between trials (ITI_DUR). This gives the visual system time to clear and prevents responses to one trial from carrying into the next. Lengthening this would slow the task; shortening it would speed it up but risks response carry-over.

### Fish Size
The FISH_SIZE parameter scales the cartoon fish proportionally. The default of 1.0 yields fish roughly 84 pixels wide on a 1280 × 800 display. This can be increased for visibility on larger displays, or for participants with visual difficulties.

### Block Schedule
The BLOCK_SCHEDULE list at the top of the script defines the proportion of different- vs. same-color trials in each block. Each block currently contains 24 trials. The number of blocks, the trial counts, and the color-match proportions can all be adjusted by editing this list. Note that to keep orientation × direction perfectly balanced, the total trial count per block should remain divisible by four.

### Fish Colors
The two fish colors are defined in the COLOURS dictionary as RGB values in PsychoPy's default color space. The defaults are a warm orange and a saturated blue, chosen to be visually distinct. They can be replaced with any other pair, although high contrast between the two colors is important for the color manipulation to function as intended.

## Running the Experiment
1. Navigate to the project directory in your terminal.
2. Run the experiment:
     python flanker_task.py
3. Enter participant information (ID, age, gender) in the dialog box that appears.
4. Follow the on-screen instructions.

## Dependencies
This code is written for PsychoPy.

## During the Experiment
Left arrow key: respond when the middle fish swims LEFT
Right arrow key: respond when the middle fish swims RIGHT
Escape: quit the experiment at any time (data collected up to that point is saved)

## Output
The experiment saves one CSV file per participant to the data/ folder, named:
flanker_<participant>_<date>.csv.

Each row of the CSV represents one trial and contains:

 - block —> block number (1-4 for main, "practice" for practice trials)
 - trial_in_block —> trial index within the block
 - orientation_congruency —> congruent or incongruent
 - colour_match —> same or different
 - target_direction, flanker_direction —> left or right
 - target_colour, flanker_colour —> orange or blue
 - correct_key —> the expected response
 - response —> the key the participant pressed
 - rt —> reaction time in seconds
 - accuracy —> 1 (correct) or 0 (incorrect or no response)

## Analysis 

The end-of-session dashboard automatically computes and displays the participant's mean reaction time and accuracy in each orientation condition, along with their personal flanker effect. Reaction times shorter than 200 ms are excluded from the mean RT calculation, as these are typically anticipatory responses rather than real decisions (Ratcliff, 1993; Whelan, 2008). Mean RT is calculated on correct trials only; accuracy is calculated on all trials.

For more detailed analysis, the CSV output supports:
  - Flanker effect by block —> does the cost of incongruent flankers grow as the color cue becomes less reliable across blocks?
  - Color-match effect —> within each block, do same-color trials show a larger flanker effect than different-color trials?
  - Interaction effects —> does the color manipulation modulate the size of the flanker effect, and does this interaction shift across blocks?
  - Post-error slowing —> do participants slow down on the trial after an error?

## Enjoy the experiment! 

## References
Botvinick, M. M., Braver, T. S., Barch, D. M., Carter, C. S., & Cohen, J. D. (2001). Conflict monitoring and cognitive control. Psychological Review, 108(3), 624–652.

Eriksen, B. A., & Eriksen, C. W. (1974). Effects of noise letters upon the identification of a target letter in a nonsearch task. Perception & Psychophysics, 16(1), 143–149.

Ratcliff, R. (1993). Methods for dealing with reaction time outliers. Psychological Bulletin, 114(3), 510–532.

Rueda, M. R., Fan, J., McCandliss, B. D., Halparin, J. D., Gruber, D. B., Lercari, L. P., & Posner, M. I. (2004). Development of attentional networks in childhood. Neuropsychologia, 42(8), 1029–1040.

Whelan, R. (2008). Effective analysis of reaction time data. The Psychological Record, 58(3), 475–482.
