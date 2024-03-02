# Autoclicker Usage

The autoclicker is triggered with the `enableBallTexture()` function

## Default behavior

When `enableBallTexture()` is called without any arguments, the default behaviour is:

### On the 1st run:
  - Each image in the `autoclickerImages` dictionary will be searched for on the screen... and clicked if found
    - The screen coordinates for each clicked image will be stored for future use (fast mode)

### On subsequent runs:
  - If `enableFastMode` is set to `True` in your script, "fast mode" will kick in. The first image (Disable Safe Mode) will be searched for, and the rest will be clicked using the previously saved coordinates (if they exist)
    - This is slightly faster (and more CPU efficient) than searching the screen for the same images on every run

    - At the end of each "fast mode" run, success (or failure) is determined by searching the screen for the 1st and last images, to make sure they're not present
    
    - Warning: "fast mode" will fail if you move/resize the AlphaConsole menu between runs (because the screen coordinates for the images/buttons will change)
  
  - If `enableFastMode` is set to `False` in your script, the behavior will be the same as the 1st run. Images will be searched for, and clicked if found
    - Previously clicked button coordinates will be used to fine-tune the image search regions, to make image searching faster
  
    - This method is generally more reliable than "fast mode", but uses more CPU due to all the image searching, which could potentially cause lag on less capable PCs

### If "fast mode" fails:

- A "clean up" attempt will be made to click any remaining buttons/images on the screen using the default image search method. Then the previous (invalid) screen coordinates for each image will be cleared
  
- The next run will be done in the default mode (same as the 1st run... searching for images and saving their coordinates) in order to get valid/updated coordinates

## Optional arguments

To give the autoclicker a custom behavior, you can change the value of any of these keyword arguments and put them inside `enableBallTexture(...)`

|keyword argument | default value | description|
|---|:---:|---|
`clickDuration=` | `0` | Amount of time the mouse button is held down on each click (seconds)
`delayAfterDSM=` | `0.3` | Amount of time to wait after "Disable Safe Mode" is clicked (seconds). Allows time for AlphaConsole plugin & menu UI to load
`delayBetweenClicks=` | `0` | Amount of time to wait between clicks (seconds)
`enableCleanup=` | `True` | Attempt a "clean up" (click remaining buttons on the screen using default image search method) if "fast mode" fails
`fastModeStartDelay=` | `0.4` | Amount of time to wait before starting a "fast mode" run (seconds). Gives bakkesmod time to reload the AlphaConsole plugin
`onlyUseCoordsForFastMode=` | `False` | Only use saved coordinates during "fast mode" runs (as opposed to searching for the "Disable Safe Mode" button which uses more CPU)
`startDelay=` | `0.4` | Amount of time to wait before starting a regular run (seconds). Gives bakkesmod time to reload the AlphaConsole plugin
`startFromImage=` | `1` | The 1st image to start from during an autoclicker run (out of the list of 5 images). Useful if you want to skip certain image(s)

### Example:

Say you want to manually click the "Disable Safe Mode" button, then have the autoclicker click the rest of the buttons

You can use something like 

```python
enableBallTexture(fastModeStartDelay=3, startFromImage=2)
```

This will make the autoclicker wait for 3 seconds (so you have time to manually click the "Disable Safe Mode" button). Then it will begin autoclicking, starting with the "cosmetics" tab (the 2nd image)