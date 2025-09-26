import os
import re
import argparse
import sys
import textwrap

if os.path.exists("/nfshome0/pixelpro/opstools/"):
    OPSTOOLS_PATH = "/nfshome0/pixelpro/opstools/"
elif os.path.exists("/home/bpix/opstools/"):
    OPSTOOLS_PATH = "/home/bpix/opstools/"
elif os.path.exists("/home/local14chstack/opstools/"):
    OPSTOOLS_PATH = "/home/local14chstack/opstools/"
else:
    print("\nERROR: Cannot find a path to opstools\n")
    exit(1)

sys.path.append(OPSTOOLS_PATH + "config/")
import ConfigTools as confTools


def analyze_pattern(pattern):
    zero_count = pattern.count("0")
    if set(pattern) == {"0"} or set(pattern) == {"1"} or zero_count == 0:
        return "Dead", 0
    if zero_count < 10:
        return "Weak", zero_count
    return None, None


def process_log_file(filepath, run_outputs, group_by_run, trans_dat):
    with open(filepath, "r") as file:
        lines = file.readlines()
    fed_number = None
    current_phase_block = []
    current_run = None
    i = 0
    while i < len(lines):
        line = lines[i]
        if group_by_run:
            run_match = re.search(
                r"PixelFEDSupervisor::startActionImpl\s+--\s+Run Number\s+:\s+(\d{6})", line
            )
            if run_match:
                new_run = run_match.group(1)
                if current_run:
                    if current_run not in run_outputs:
                        run_outputs[current_run] = []
                    run_outputs[current_run].extend(current_phase_block)
                    current_phase_block = []
                current_run = new_run
        fed_match = re.search(r"-+begin output-FED#(\d+)-+", line)
        if fed_match:
            fed_number = fed_match.group(1)
        if re.search(r"Fiber\s+RDY\s+SET\s+RD\s+pattern:", line):
            i += 1
            while i < len(lines):
                table_line = lines[i].strip()
                if not re.match(r"^\d+\s+\d+", table_line):
                    break
                parts = re.split(r"\s+", table_line)
                if len(parts) < 6 and i + 1 < len(lines):
                    next_line = lines[i + 1].strip()
                    parts.extend(re.split(r"\s+", next_line))
                    i += 1
                if len(parts) >= 6:
                    fiber_number = parts[0]
                    pattern = parts[4]
                    state, good_phases = analyze_pattern(pattern)
                    if state in ("Weak", "Dead"):
                        rocs = []
                        detector = ""
                        if fed_number and fiber_number.isdigit():
                            ch = (int(fiber_number) * 2) - 1
                            try:
                                roc1 = trans_dat.roc_name_from_fed_ch(int(fed_number), ch)
                                roc2 = trans_dat.roc_name_from_fed_ch(int(fed_number), ch + 1)
                                rocs = [roc1, roc2]
                                if roc1.startswith("BPix"):
                                    detector = "BPIX"
                                elif roc1.startswith("FPix"):
                                    detector = "FPIX"
                            except Exception:
                                rocs = []
                                detector = "UNKNOWN"
                        entry = f"{state}\t{fed_number}\t{fiber_number}\t{good_phases if state == 'Weak' else '0'}\t{detector}\t{','.join(rocs)}"
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


def format_row(parts, roc_width=82):
    state, fed, fiber, phases, detector, rocs = parts
    wrapped_rocs = textwrap.wrap(rocs, width=roc_width, subsequent_indent="")
    lines = []
    for idx, roc_line in enumerate(wrapped_rocs):
        if idx == 0:
            lines.append(
                "| {:<6} | {:<4} | {:<5} | {:<11} | {:<8} | {:<{}s} |".format(
                    state, fed, fiber, phases, detector, roc_line, roc_width
                )
            )
        else:
            lines.append(
                "| {:<6} | {:<4} | {:<5} | {:<11} | {:<8} | {:<{}s} |".format(
                    "", "", "", "", "", roc_line, roc_width
                )
            )
    return lines


def main(directory, show_run, save_output):
    run_outputs = {} if show_run else []
    pixconf = os.environ.get("PIXELCONFIGURATIONBASE")
    if not pixconf:
        raise RuntimeError("PIXELCONFIGURATIONBASE environment variable not set.")
    trans_dat = confTools.translation_dat(
        os.path.join(pixconf, "nametranslation/0/translation.dat")
    )
    output_folder = "/nfshome0/atahmad/bad_phase"
    os.makedirs(output_folder, exist_ok=True)
    dir_name = os.path.basename(os.path.normpath(directory))
    custom_name = dir_name.replace("Log_", "") if dir_name.startswith("Log_") else "summary"
    output_filename = os.path.join(output_folder, f"FED_phases_{custom_name}.txt")
    for root, _, files in os.walk(directory):
        for file in files:
            if "PixelFEDSupervisor" in file and file.endswith(".log"):
                filepath = os.path.join(root, file)
                print(f"Processing file: {filepath}")
                process_log_file(filepath, run_outputs, show_run, trans_dat)
    roc_width = 82
    header = "| {:<6} | {:<4} | {:<5} | {:<11} | {:<8} | {:<{}s} |".format(
        "State", "FED", "Fiber", "Good Phases", "Detector", "ROCs", roc_width
    )
    table_width = len(header)
    separator = "+" + "-" * (table_width - 2) + "+"
    underline = "_" * table_width
    if save_output:
        out_file = open(output_filename, "w")
    else:
        out_file = None

    def write_and_print(line):
        print(line)
        if out_file:
            out_file.write(line + "\n")

    if show_run:
        for run_number in sorted(
            run_outputs.keys(), key=lambda x: (x != "No Run Number Found", x)
        ):
            run_lines = run_outputs[run_number]
            run_lines.sort(key=lambda x: int(x.split("\t")[1]))
            title = f"{'Run Number: ' + run_number if run_number != 'No Run Number Found' else 'No Run Number Found'}"
            write_and_print(f"\n{title}")
            write_and_print(separator)
            write_and_print(header)
            write_and_print(separator)
            for line in run_lines:
                parts = line.split("\t")
                for row in format_row(parts, roc_width):
                    write_and_print(row)
                write_and_print(underline)
    else:
        run_outputs.sort(key=lambda x: int(x.split("\t")[1]))
        write_and_print(separator)
        write_and_print(header)
        write_and_print(separator)
        for line in run_outputs:
            parts = line.split("\t")
            for row in format_row(parts, roc_width):
                write_and_print(row)
            write_and_print(underline)
    if out_file:
        out_file.close()
        print(f"\nOutput written to: {output_filename}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Analyze bad FED phases in PixelFEDSupervisor log files."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-last", action="store_true", help="Use last log folder in /nfspixelraid/nfspixelraid/log0")
    group.add_argument("-log0", metavar="LOGDIR", help="Use /nfspixelraid/nfspixelraid/log0/LOGNAME")
    group.add_argument("-other", metavar="PATH", help="Use a custom log folder path")
    parser.add_argument("-run", action="store_true", help="Group and display data by run number.")
    parser.add_argument("-save", action="store_true", help="Save the output to a text file.")
    args = parser.parse_args()

    if args.last:
        base_dir = "/nfspixelraid/nfspixelraid/log0"
        subdirs = [os.path.join(base_dir, d) for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]
        if not subdirs:
            raise RuntimeError("No log folders found in /nfspixelraid/nfspixelraid/log0")
        directory = max(subdirs, key=os.path.getmtime)
    elif args.log0:
        directory = os.path.join("/nfspixelraid/nfspixelraid/log0", args.log0)
    elif args.other:
        directory = args.other
    else:
        raise RuntimeError("You must specify one of -last, -log0, or -other")

    main(directory, args.run, args.save)
