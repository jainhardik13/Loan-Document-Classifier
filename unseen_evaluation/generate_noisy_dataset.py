from pathlib import Path
import random
from typing import Callable

import pandas as pd

OUTPUT_PATH = Path(__file__).resolve().parent / "noisy_loan_documents.csv"
TOTAL_PER_CLASS = 60  # 60 x 5 classes = 300 rows


def add_ocr_noise(text: str, rng: random.Random) -> str:
    """Inject OCR-like noise: typos, symbols, casing, and spacing issues."""
    replacements = {
        "salary": "salry",
        "statement": "statemnt",
        "income": "incom3",
        "property": "proprty",
        "aadhaar": "aadhr",
        "passport": "passprt",
        "deduction": "deducton",
        "balance": "balnce",
        "return": "retum",
        "licence": "licnce",
    }

    words = text.split()
    noisy_words = []
    for word in words:
        cleaned = word.strip(",.-")
        mutated = replacements.get(cleaned.lower(), word)

        if rng.random() < 0.08:
            mutated = mutated.upper()
        if rng.random() < 0.08:
            mutated = mutated + rng.choice(["#", "@", "/", ":", "."])
        if rng.random() < 0.06 and len(mutated) > 4:
            # Character drop to mimic OCR misses
            idx = rng.randint(1, len(mutated) - 2)
            mutated = mutated[:idx] + mutated[idx + 1 :]

        noisy_words.append(mutated)

    # Sometimes remove spaces between neighboring words
    merged_words = []
    i = 0
    while i < len(noisy_words):
        if i < len(noisy_words) - 1 and rng.random() < 0.08:
            merged_words.append(noisy_words[i] + noisy_words[i + 1])
            i += 2
        else:
            merged_words.append(noisy_words[i])
            i += 1

    return " ".join(merged_words)


def salary_slip_text(rng: random.Random) -> str:
    templates = [
        "payroll salary slip gross salary {gross} net pay {net} pf deduction {pf} hra tds amount {tds}",
        "monthly employee payslip basic {basic} allowances {allowance} professional tax {tax} net credited {net}",
        "salary sheet for month {month} gross earning {gross} total deducton {tax} take home {net}",
    ]
    month = rng.choice(["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug"])
    text = rng.choice(templates).format(
        gross=rng.randint(30000, 180000),
        net=rng.randint(23000, 140000),
        pf=rng.randint(1000, 7000),
        tds=rng.randint(700, 6500),
        basic=rng.randint(18000, 90000),
        allowance=rng.randint(4000, 35000),
        tax=rng.randint(500, 6000),
        month=month,
    )
    return add_ocr_noise(text, rng)


def bank_statement_text(rng: random.Random) -> str:
    templates = [
        "bank account statement opening balance {open_bal} credits {credit} debits {debit} closing balance {close}",
        "passbook entry neft imps upi transfer cheque withdrawal ending balance {close}",
        "savings statemnt salary credit {credit} atm cash debit {debit} current balnce {close}",
    ]
    text = rng.choice(templates).format(
        open_bal=rng.randint(10000, 500000),
        credit=rng.randint(5000, 250000),
        debit=rng.randint(2000, 200000),
        close=rng.randint(5000, 450000),
    )
    return add_ocr_noise(text, rng)


def it_return_text(rng: random.Random) -> str:
    templates = [
        "itr acknowledgement assessment year {ay} total income {income} deduction 80c {ded} tax payable {tax}",
        "income tax retum form 16 tds {tds} taxable income {income} refund {refund}",
        "e filing return verification pan details gross incom3 {income} liability {tax}",
    ]
    text = rng.choice(templates).format(
        ay=rng.choice(["2022-23", "2023-24", "2024-25"]),
        income=rng.randint(250000, 2800000),
        ded=rng.randint(10000, 200000),
        tax=rng.randint(1000, 250000),
        tds=rng.randint(2000, 180000),
        refund=rng.randint(0, 100000),
    )
    return add_ocr_noise(text, rng)


def property_paper_text(rng: random.Random) -> str:
    templates = [
        "sale deed proprty survey number {survey} plot area {area} stamp duty {duty} registrar office",
        "encumbrance certificate property address ward {ward} owner details no active mortgage",
        "title deed land document khata extract parcel id {survey} agreement value {value}",
    ]
    text = rng.choice(templates).format(
        survey=rng.randint(10000, 99999),
        area=rng.randint(450, 5000),
        duty=rng.randint(20000, 350000),
        ward=rng.randint(1, 99),
        value=rng.randint(1500000, 25000000),
    )
    return add_ocr_noise(text, rng)


def id_proof_text(rng: random.Random) -> str:
    templates = [
        "aadhaar card uid {uid} date of birth {dob} identity verified",
        "pan card permanent account number {pan} applicant signature dob {dob}",
        "passprt number {passport} nationality indian expiry date {exp}",
        "voter id epic {epic} constituency and polling station details",
        "driving licnce number {dl} validity {exp} transport authority",
    ]
    text = rng.choice(templates).format(
        uid=rng.randint(100000000000, 999999999999),
        dob=rng.choice(["12-04-1994", "21-09-1989", "05-01-1998", "17-07-1992"]),
        pan=f"{rng.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{rng.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{rng.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{rng.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{rng.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{rng.randint(0, 9)}{rng.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}",
        passport=f"P{rng.randint(1000000, 9999999)}",
        exp=rng.choice(["2029-02-15", "2030-11-12", "2032-05-19", "2035-08-01"]),
        epic=f"EPIC{rng.randint(100000, 999999)}",
        dl=f"DL-{rng.randint(10, 99)}-{rng.randint(1000000, 9999999)}",
    )
    return add_ocr_noise(text, rng)


def main() -> None:
    rng = random.Random(2026)
    rows = []

    generators: list[tuple[str, Callable[[random.Random], str]]] = [
        ("Salary_Slip", salary_slip_text),
        ("Bank_Statement", bank_statement_text),
        ("IT_Return", it_return_text),
        ("Property_Paper", property_paper_text),
        ("ID_Proof", id_proof_text),
    ]

    for category, generator in generators:
        for _ in range(TOTAL_PER_CLASS):
            rows.append({"Document_Text": generator(rng), "Category": category})

    rng.shuffle(rows)
    df = pd.DataFrame(rows)
    df.to_csv(OUTPUT_PATH, index=False)

    print(f"Saved noisy dataset at: {OUTPUT_PATH}")
    print(f"Total rows: {len(df)}")
    print(df["Category"].value_counts().to_string())


if __name__ == "__main__":
    main()
