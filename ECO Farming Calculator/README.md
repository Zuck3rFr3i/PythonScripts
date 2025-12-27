# Dependencies
- Pyside6
- Nuitka (For Compiling)


# Usage
- The UI will explain itself. Essentially it will Calculate everything you need to know about Planting your Crop
- It takes following into consideration:
    - Nutrition Values (Currently on your plots)
    - Target Nutrition Saturation
    - Crop aswell as the BIOME
    - Temperature and Moisture.

- It will show you the needed Fertilizer.
- It will show you a 5x5 Plot planting plan.
- It will show you the best Followup Crops depending on the Nutritions

# Compiling
- i will not Precompile this since there is alot of "not good people" out there abusing this to provide People with Malware.
- You can either run this just in Visual Studio Code or Compile it yourself if a .exe is needed.

# Compiling Command:
- python -m nuitka --onefile --standalone --windows-console-mode=disable --enable-plugin=pyside6 --include-data-files=crops_config.json=crops_config.json --output-filename=EcoFarming_Final_2025 ecocalc.py

# Config
- In the Config i added all Crops thaat i was able to find in my research.
- if you have modded Crfops just add them into the File with the same Syntax.
- "YOURCROPNAME": {"N": 0.6, "P": 0.2, "K": 0.2, "Biome": "Grassland", "Temp": "Mid", "Moist": "Mid"}, < Never forget that the second last line always needs a , the last line should not have one since its the last entry!