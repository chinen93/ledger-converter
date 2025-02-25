# ledger-converter
Convert input files to a list of entries in the ledger format.

## Example

Input
```text
Date,Description,Amount,Running Bal.
02/13/2025,"ABCDEFGH","1,200.00","5,678.90"
```

Output
```text
2025-02-13       ABCDEFGH
    Expenses:Don't know                            $1,200.00
    Bank:CreditCard
```

## What is Ledger

[Ledger](https://ledger-cli.org) is a command-line tool for tracking your finances using double-entry accounting. It helps you stay on top of your money, see where it’s going, and plan for the future. With Ledger, you can track expenses, set budgets, and get a clear picture of your financial health—all in plain text files.

- **Know where your money goes** – Track every expense and income source with precision.
- **Plan ahead** – Set budgets based on past spending and avoid surprises.
- **Stay in control** – No locked-in databases, no hidden fees. Just a simple plain text file to manage your finances.

However, Ledger requires all transactions to be entered in a specific format, which is not how financial institutions typically provide transaction data. They give you CSV files, PDFs, or other formats instead. That means you have to manually convert your statements, which can be a huge pain.

## Why this project exists?

I built this tool to make that process easier. Instead of spending time reformatting transactions by hand, this project automatically converts CSV files into Ledger’s format.

I also had a couple of personal reasons:

- **I wanted to relearn Python** – This was a good way to dive back into coding and solve a real problem at the same time.
- **I needed it myself** – I use Ledger for my own finances, and manual conversion was annoying. So, I built something to fix that.

There are other tools out there that do similar things. But I wanted to make my own, keep it simple, and learn something along the way. Hope it helps you too!

# Installation
## Clone the Repository

```sh
git clone https://github.com/chinen93/ledger-converter.git
cd ledger-converter
```
## Create an Virtual Environment

This step is optional

```sh
python3 -m venv venv
source venv/bin/activate
```

## Install Dependencies

To make sure everything will work as expected.

```sh
pip3 install -r requirements.txt
```

# Usage
Follow these steps to convert your files into Ledger's format:

1. Prepare Your CSV Files
    - Move files to be converted into `input` directory  inside the project folder.

2. Prepare Accounts and Aliases File
    - Copy `accounts.txt.example` to `accounts.txt`
    - Copy `accounts_aliases.txt` to `accounts_aliases.txt`
    - Populate with known accounts and aliases to be used as placeholders in the conversion
    - HINT: One way to populate is to use `ledger accounts >> accounts.txt`

3. Run the Conversion Script
    - ```sh
        python3 ledger-converter.py
        ```
4. Review the Output File
    - The converted entries will be saved in the `output.txt` file
    - Open the file and check for any missing entries

5. Edit and Finalize the Output
    - Some fields may contain placeholder values. Update them to ensure accuracy.
    - Make sure all transaction details match your financial records.

6. Integrate with Your Ledger System
    - Copy and paste the finalized transactions into your Ledger journal file.
    - Run Ledger CLI to verify that the new entries are correctly formatted.

By following these steps, you’ll have a smooth conversion process and an accurate Ledger file.