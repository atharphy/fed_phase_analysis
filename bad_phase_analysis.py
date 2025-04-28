import os
import re
import argparse

def analyze_pattern(pattern):
    zero_count = pattern.count('0')
    if set(pattern) == {'0'} or set(pattern) == {'1'} or zero_count == 0:
        return 'Dead', 0
    if zero_count < 10:
        return 'Weak', zero_count
    return None, None

def process_log_file(filepath, run_outputs, group_by_run):
    with open(filepath, 'r') as file:
        lines = file.readlines()

    fed_number = None
    current_phase_block = []
    current_run = None
    i = 0

    while i < len(lines):
        line = lines[i]

        if group_by_run:
            run_match = re.search(r'PixelFEDSupervisor::startActionImpl\s+--\s+Run Number\s+:\s+(\d{6})', line)
            if run_match:
                new_run = run_match.group(1)

                if current_run:
                    if current_run not in run_outputs:
                        run_outputs[current_run] = []
                    run_outputs[current_run].extend(current_phase_block)
                    current_phase_block = []

                current_run = new_run

        fed_match = re.search(r'-+begin output-FED#(\d+)-+', line)
        if fed_match:
            fed_number = fed_match.group(1)

        if re.search(r'Fiber\s+RDY\s+SET\s+RD\s+pattern:', line):
            i += 1
            while i < len(lines):
                table_line = lines[i].strip()
                if not re.match(r'^\d+\s+\d+', table_line):
                    break
                parts = re.split(r'\s+', table_line)

                if len(parts) < 6 and i + 1 < len(lines):
                    next_line = lines[i + 1].strip()
                    parts.extend(re.split(r'\s+', next_line))
                    i += 1

                if len(parts) >= 6:
                    fiber_number = parts[0]
                    pattern = parts[4]
                    state, good_phases = analyze_pattern(pattern)
                    if state in ('Weak', 'Dead'):
                        entry = f"{state}\t{fed_number}\t{fiber_number}\t{good_phases if state == 'Weak' else '0'}"
                        if group_by_run:
                            current_phase_block.append(entry)
                        else:
                            run_outputs.append(entry)
                i += 1
        else:
            i += 1

    if group_by_run and current_phase_block:
        key = current_run if current_run else "No Run Number Found"
        if key not in run_outputs:
            run_outputs[key] = []
        run_outputs[key].extend(current_phase_block)

def main(directory, show_run, save_output):
    run_outputs = {} if show_run else []

    output_folder = "/nfshome0/atahmad/bad_phase"
    os.makedirs(output_folder, exist_ok=True)

    dir_name = os.path.basename(os.path.normpath(directory))
    custom_name = dir_name.replace("Log_", "") if dir_name.startswith("Log_") else "summary"
    output_filename = os.path.join(output_folder, f"FED_phases_{custom_name}.txt")

    for root, _, files in os.walk(directory):
        for file in files:
            if 'PixelFEDSupervisor' in file and file.endswith('.log'):
                filepath = os.path.join(root, file)
                print(f"Processing file: {filepath}")
                process_log_file(filepath, run_outputs, show_run)

    header = "| {:<8} | {:<11} | {:<13} | {:<12} |".format("State", "FED Number", "Fiber Number", "Good Phases")
    separator = "+" + "-"*10 + "+" + "-"*13 + "+" + "-"*15 + "+" + "-"*14 + "+"

    if save_output:
        out_file = open(output_filename, "w")
    else:
        out_file = None

    def write_and_print(line):
        print(line)
        if out_file:
            out_file.write(line + "\n")

    if show_run:
        for run_number in sorted(run_outputs.keys(), key=lambda x: (x != "No Run Number Found", x)):
            run_lines = run_outputs[run_number]
            run_lines.sort(key=lambda x: int(x.split("\t")[1]))

            title = f"{'Run Number: ' + run_number if run_number != 'No Run Number Found' else 'No Run Number Found'}"
            write_and_print(f"\n{title}")
            write_and_print(separator)
            write_and_print(header)
            write_and_print(separator)

            for line in run_lines:
                parts = line.split("\t")
                formatted_line = "| {:<8} | {:<11} | {:<13} | {:<12} |".format(*parts)
                write_and_print(formatted_line)

            write_and_print(separator)
    else:
        run_outputs.sort(key=lambda x: int(x.split("\t")[1]))
        write_and_print(separator)
        write_and_print(header)
        write_and_print(separator)
        for line in run_outputs:
            parts = line.split("\t")
            formatted_line = "| {:<8} | {:<11} | {:<13} | {:<12} |".format(*parts)
            write_and_print(formatted_line)
        write_and_print(separator)

    if out_file:
        out_file.close()
        print(f"\nOutput written to: {output_filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze bad FED phases in PixelFEDSupervisor log files.")
    parser.add_argument("directory", help="Path to the directory containing log files.")
    parser.add_argument("-run", action="store_true", help="Group and display data by run number.")
    parser.add_argument("-save", action="store_true", help="Save the output to a text file.")
    args = parser.parse_args()
    main(args.directory, args.run, args.save)
