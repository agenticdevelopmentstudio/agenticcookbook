
- `must-show-determinate-progress-when-total-known`: an async wait whose total work is known, shown with a progress bar and percentage or with none
- `must-show-indeterminate-progress-when-total-unknown`: an async wait whose total work is not known, shown with a spinner, skeleton or shimmer or with nothing
- `must-not-appear-frozen`: an async wait during which the UI shows no progress and looks frozen or unresponsive
- `must-show-determinate-progress-when-total-known`, `must-show-indeterminate-progress-when-total-unknown`: Implement determinate progress bars (with percentage) and indeterminate spinners/skeletons/shimmer in the DOM;
- `must-not-appear-frozen`: prevent UI freeze during async operations
- `should-update-progress-bar-as-work-completes`: a determinate progress bar that does not advance as work completes
