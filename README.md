# Bad Phase Analysis Tool

This tool analyzes FED phases from **PixelFEDSupervisor** log files, identifying **Weak** and **Dead** fiber patterns based on RD patterns, and maps them to detectors (**BPIX/ FPIX**) and corresponding ROC names.

---

## How to Run

1. **Connect to the main server:**
   ```bash
   ssh username@cmsusr
   ```

2. **Connect to the specific machine:**
   ```bash
   ssh srv-s2b18-37-01
   ```

3. **Load the TriDAS environment:**
   ```bash
   cd /nfshome0/pixelpro/TriDAS/
   source setenv.sh
   ```

4. **Run the script:**
   ```bash
   python3 /nfshome0/pixelpro/opstools/scripts/fed_phase_analysis.py [OPTIONS]
   ```

---

## Input Options

You must provide one of the following to specify which log folder to analyze:

- `--last`  
  Use the **latest** log folder from:
  ```
  /nfspixelraid/nfspixelraid/log0
  ```
  Example:
  ```bash
  python3 /nfshome0/pixelpro/opstools/scripts/fed_phase_analysis.py --last
  ```

- `--log0 LOGDIR`  
  Use a specific log folder under `/nfspixelraid/nfspixelraid/log0`.  
  Example:
  ```bash
  python3 /nfshome0/pixelpro/opstools/scripts/fed_phase_analysis.py --log0 Log_27Apr2025_13-45-22_GMT
  ```

- `--other PATH`  
  Provide a full custom path to a log directory.  
  Example:
  ```bash
  python3 /nfshome0/pixelpro/opstools/scripts/fed_phase_analysis.py --other /path/to/custom/logs
  ```

---

## Additional Flags

- `-run`  
  Group and display results by **Run Number**.  
  Example:
  ```bash
  python3 /nfshome0/pixelpro/opstools/scripts/fed_phase_analysis.py --last -run
  ```

- `-save`  
  Save output summary as a text file under:
  ```
  /nfshome0/atahmad/bad_phase/
  ```
  Example:
  ```bash
  python3 /nfshome0/pixelpro/opstools/scripts/fed_phase_analysis.py --last -save
  ```

- Combine flags:  
  Example (group by run number **and** save to file):
  ```bash
  python3 /nfshome0/pixelpro/opstools/scripts/fed_phase_analysis.py --last -run -save
  ```

---

## Output

- If `-save` is used, the summary will be written to:
  ```
  /nfshome0/atahmad/bad_phase/FED_phases_<log_folder_name>.txt
  ```
- If not, results are printed directly in the console.  

The output is formatted as a clean table with columns for **State, FED, Fiber, Good Phases, Detector, and ROCs**.
