import re
import sys

energy_pattern = re.compile(r"^ENERGY:\s+(\d+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)")

output_file = str(sys.argv[1])

step_offset = 0

header = "ETITLE: TS BOND ANGLE DIHED IMPRP ELECT VDW BOUNDARY MISC KINETIC TOTAL TEMP POTENTIAL TOTAL3 TEMPAVG PRESSURE GPRESSURE VOLUME PRESSAVG GPRESSAVG\n"

with open(output_file, "w") as out:
    out.write(header)

    for i in range(1, 11):
        log_file = f"step5_{i}.out"
        with open(log_file, "r") as f:
            for line in f:
                match = energy_pattern.match(line)
                if match:
                    step = int(match.group(1)) + step_offset
                    bond = match.group(2)
                    angle = match.group(3)
                    dihed = match.group(4)
                    imprp = match.group(5)
                    elect = match.group(6)
                    vdw = match.group(7)
                    boundary = match.group(8)
                    misc = match.group(9)
                    kinetic = match.group(10)
                    total = match.group(11)
                    temp = match.group(12)
                    potential = match.group(13)
                    total3 = match.group(14)
                    tempavg = match.group(15)
                    pressure = match.group(16)
                    gpressure = match.group(17)
                    volume = match.group(18)
                    pressavg = match.group(19)
                    gpressavg = match.group(20)

                    out.write(f"ENERGY: {step} {bond} {angle} {dihed} {imprp} {elect} {vdw} {boundary} {misc} {kinetic} {total} {temp} {potential} {total3} {tempavg} {pressure} {gpressure} {volume} {pressavg} {gpressavg}\n")

        step_offset += int(sys.argv[2])


print("Log files merged successfully!")

