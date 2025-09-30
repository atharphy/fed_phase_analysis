# Bad Phase Analysis Tool

This tool analyzes FED phases from **PixelFEDSupervisor** log files, identifying **Weak** and **Dead** fibers based on RD patterns, and mapping them to detectors (**BPIX / FPIX**) and corresponding ROC names.

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
   python3 /nfshome0/pixelpro/opstools/scripts/fed_phases.py [OPTIONS]
   ```

---

## Input Options

You must provide one of the following:

- **`-last`**  
  Use the **latest** log folder under:
  ```
  /nfspixelraid/nfspixelraid/log0
  ```
  Example:
  ```bash
  python3 fed_phases.py -last
  ```

- **`-log0 LOGDIR`**  
  Use a specific log folder name inside `/nfspixelraid/nfspixelraid/log0/`.  
  Example:
  ```bash
  python3 fed_phases.py -log0 Log_27Apr2025_13-45-22_GMT
  ```

- **`-other PATH`**  
  Provide a full custom path to a log directory.  
  Example:
  ```bash
  python3 fed_phases.py -other /path/to/custom/logs
  ```

- **`-latest`**  
  Automatically gather the most recent logs from **all FED supervisors** via SSH and analyze them.  
  Example:
  ```bash
  python3 fed_phases.py -latest
  ```

---

## Additional Flags

- **`-run`**  
  Group and display results by **Run Number**.  
  ```bash
  python3 fed_phases.py -last -run
  ```

- **`-save`**  
  Save the summary to:  
  ```
  /nfshome0/atahmad/bad_phase/FED_phases_<log_folder_name>.txt
  ```
  Example:
  ```bash
  python3 fed_phases.py -last -save
  ```

- **`-dead` / `-weak`**  
  Filter to show **only Dead fibers** or **only Weak fibers**.  
  Examples:
  ```bash
  python3 fed_phases.py -latest -dead
  python3 fed_phases.py -log0 Log_27Apr2025_13-45-22_GMT -weak
  ```

- **Combine flags**  
  Example: group by run number, save to file, and show only Dead fibers:  
  ```bash
  python3 fed_phases.py -last -run -save -dead
  ```

---

## Output

- **Default**: Results are printed to the console as a formatted table.  
- **With `-save`**: Output is also written to a file under `/nfshome0/atahmad/bad_phase/`.  

The table includes the following columns:

| Column          | Description                                   |
|-----------------|-----------------------------------------------|
| **State**       | Weak / Dead                                   |
| **FED**         | FED ID number                                 |
| **Fiber**       | Fiber number                                  |
| **Good Phases** | Number of good phases (only for Weak)         |
| **Detector**    | BPIX / FPIX                                   |
| **ROCs**        | Expanded ROC names corresponding to the fiber |

