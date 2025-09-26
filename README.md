# Bad Phase Analysis Tool

This tool analyzes **FED phases** from **PixelFEDSupervisor** log files, identifying **"Weak"** and **"Dead"** fiber patterns based on RD patterns.  
It also provides detector context (**BPIX / FPIX**) and lists the corresponding **ROCs** for easier diagnosis.  

---

## Setup and Execution

### 1. Connect to the main server
```bash
ssh username@cmsusr
```

### 2. Connect to the specific machine
```bash
ssh srv-s2b18-37-01
```

### 3. Set up the TriDAS environment
```bash
cd /nfshome0/pixelpro/TriDAS/
source setenv.sh
```

### 4. Run the analysis script
```bash
python3 /nfshome0/pixelpro/opstools/scripts/fed_phase_analysis.py [OPTIONS]
```

---

## Choosing Log Folder

You must provide **one of the following flags** to specify the log folder:

- **`-last`**  
  Use the **last created log folder** in:
  ```
  /nfspixelraid/nfspixelraid/log0
  ```

- **`-log0 LOGNAME`**  
  Use a specific folder inside `log0`. Example:
  ```bash
  python3 fed_phase_analysis.py -log0 Log_27Apr2025_13-45-22_GMT
  ```

- **`-other PATH`**  
  Use a **custom folder path**. Example:
  ```bash
  python3 fed_phase_analysis.py -other /tmp/custom_logs
  ```

---

## Additional Flags

- **`-run`**  
  Group and display the output by **Run Number**.

- **`-save`**  
  Save the output summary into:
  ```
  /nfshome0/atahmad/bad_phase/
  ```

---

## Example Usage

- **Use last log folder (console output only):**
  ```bash
  python3 /nfshome0/pixelpro/opstools/scripts/fed_phase_analysis.py -last
  ```

- **Analyze a specific folder in log0:**
  ```bash
  python3 /nfshome0/pixelpro/opstools/scripts/fed_phase_analysis.py -log0 Log_27Apr2025_13-45-22_GMT
  ```

- **Use a custom folder path:**
  ```bash
  python3 /nfshome0/pixelpro/opstools/scripts/fed_phase_analysis.py -other /tmp/custom_logs
  ```

- **Group results by Run Number and save output:**
  ```bash
  python3 /nfshome0/pixelpro/opstools/scripts/fed_phase_analysis.py -last -run -save
  ```

---

## Output

- With `-save`, the summary is written to:
  ```
  /nfshome0/atahmad/bad_phase/FED_phases_<log_folder_name>.txt
  ```

- Without `-save`, the summary is only displayed in the terminal.

The output table includes:

| Column       | Description                                |
|--------------|--------------------------------------------|
| **State**    | Phase status: `Weak` or `Dead`            |
| **FED**      | FED number                                |
| **Fiber**    | Fiber number                              |
| **Good Phases** | Number of good phases detected          |
| **Detector** | Detector system: `BPIX` or `FPIX`         |
| **ROCs**     | List of affected ROC(s), auto-wrapped     |

---

## Quick Reference

Most common commands:

- Run on **last log folder**:
  ```bash
  python3 fed_phase_analysis.py -last
  ```

- Run on a **specific log0 folder**:
  ```bash
  python3 fed_phase_analysis.py -log0 Log_27Apr2025_13-45-22_GMT
  ```

- Run on a **custom path**:
  ```bash
  python3 fed_phase_analysis.py -other /path/to/logs
  ```

- Run on last log, **group by run and save**:
  ```bash
  python3 fed_phase_analysis.py -last -run -save
  ```
