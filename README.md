# AI-search

______________________________________________________________________

## File Structure

**AI-search**\
├── [Budget-HC.py](Budget-HC.py)\
├── [Budget-ID.py](Budget-ID.py)\
└── [input.txt](input.txt)

______________________________________________________________________

## How to Run

***By default the program reads the [*input.txt*](input.txt), but if you want to test out different inputs, just manually edit the file or replace the file with your own input***

### Budget-ID (Interative Deepening Search)

- **Open terminal and cd to this dir**
- `python Budget-ID.py {target_value} {budget} {flag_for_display_trace}`
  - replace *`target_value: int`, `budget: int`, `flag_for_display_trace: 'V' for Verbose, 'C' for Compact`* accordingly

### Budget-HC (Hill Climbing with Random Restarts)

- **Open terminal and cd to this dir**
- `python Budget-HC.py {target_value} {budget} {flag_for_display_trace} {restart_num}`
  - replace *`target_value: int`, `budget: int`, `flag_for_display_trace: 'V' for Verbose, 'C' for Compact`, `restart_num: int`* accordingly
