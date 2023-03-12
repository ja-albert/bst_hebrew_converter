from __future__ import annotations

import csv
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class GrabsteinRecord:
    id: int
    grabstein: Grabstein
    key: str
    values: list[str] = field(default_factory=list)


@dataclass
class Grabstein:
    id: str
    records: list[GrabsteinRecord] = field(default_factory=list)


def read_grabstein_csv(file: Path, encoding: str = "utf-8") -> list[Grabstein]:
    with open(file, newline="", encoding=encoding) as f:
        reader = csv.reader(f, dialect="excel-tab")

        data = {}
        for row in reader:
            if not row[0]:
                # Empty row
                continue

            record_id = int(row[0])
            grabstein_id = row[1]
            record_key = row[2]
            record_values = row[3:]

            grabstein = data.get(grabstein_id, Grabstein(grabstein_id))
            grabstein_record = GrabsteinRecord(
                record_id, grabstein, record_key, record_values
            )
            grabstein.records.append(grabstein_record)
            data[grabstein_id] = grabstein

    return list(data.values())


def write_grabstein_csvs(directory: Path, grabsteine: list[Grabstein]) -> None:
    for grabstein in grabsteine:
        grabstein_csv = directory / f"{grabstein.id}.csv"
        write_grabstein_csv(grabstein_csv, grabstein)


def write_grabstein_csv(file: Path, grabstein: Grabstein, mode: str = "w") -> None:
    with open(file, mode, encoding="utf-8") as f:
        writer = csv.writer(f, dialect="excel")
        for record in grabstein.records:
            writer.writerow([record.key] + record.values)
