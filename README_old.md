# Bad Phase Analysis Tool

This tool analyzes FED phases from PixelFEDSupervisor log files, helping identify "Weak" and "Dead" fiber patterns based on RD patterns.

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

3. **Navigate to the working directory:**

   ```bash
   cd /nfshome0/pixelpro/opstools/masked
   ```

4. **Execute the analysis script:**

   ```bash
   python3 bad_phase_analysis.py /nfspixelraid/nfspixelraid/log0/Log_DDMonthYYYY_HH-MM-SS_GMT
   ```

   > Replace `Log_DDMonthYYYY_HH-MM-SS_GMT` with the actual log folder you want to analyze.

---

## Important Notes

- First, inspect the available log folders under:

  ```bash
  /nfspixelraid/nfspixelraid/log0
  ```

- Copy the full path of the log folder you wish to analyze.

---

## Available Flags

- `-run`  
  Group and display the analysis output by **Run Number**.

- `-save`  
  Save the output summary as a **text file** under:

  ```
  /nfshome0/atahmad/bad_phase/
  ```

### Example Usage

- **Basic run (console output only):**

  ```bash
  python3 bad_phase_analysis.py /nfspixelraid/nfspixelraid/log0/Log_27Apr2025_13-45-22_GMT
  ```

- **Group output by Run Number (console only):**

  ```bash
  python3 bad_phase_analysis.py /nfspixelraid/nfspixelraid/log0/Log_27Apr2025_13-45-22_GMT -run
  ```

- **Save output to file without grouping:**

  ```bash
  python3 bad_phase_analysis.py /nfspixelraid/nfspixelraid/log0/Log_27Apr2025_13-45-22_GMT -save
  ```

- **Group by Run Number and save to file:**

  ```bash
  python3 bad_phase_analysis.py /nfspixelraid/nfspixelraid/log0/Log_27Apr2025_13-45-22_GMT -run -save
  ```

---

## Output

- If `-save` is used, the summary will currently be saved to:

  ```
  /nfshome0/atahmad/bad_phase/FED_phases_<log_folder_name>.txt
  ```

- If `-save` is **not** used, the summary will only be printed in the console.

---
