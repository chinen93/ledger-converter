# ======================================
# Functions
# ======================================

runLedgerConverter() {
    echo "Running Ledger Converter"

    # Activate environment to run code
    source venv/bin/activate

    # Run code
    python3 ledger-tool.py --convert

    # Deactivate environment
    deactivate
}

runTests() {
    echo "Running Ledger Converter Tests"

    # Activate environment to run code
    source venv/bin/activate

    # Run code
    python3 -m unittest --verbose

    # Deactivate environment
    deactivate
}

runLedgerAccounts() {
    echo "Running Ledger Account Export"

    echo "Loading environment variables"
    source .env

    ledger -f $LEDGER_FILE accounts > $ACCOUNTS_FILE
}

printUsage() {
    echo ""
    echo "Ledger Converter"
    echo ""
    echo "Usage: $0 [ARGS]"
    echo ""
    echo "Arguments:"
    echo "None             : Get Helper"
    echo "-c | --convert   : Run Conveter"
    echo "-r | --report    : Run Reports"
    echo "-t | --test      : Run Tests"
    echo "-a | --accounts" : Extract Accounts from Ledger file
    echo "-h | --help      : Get Helper"
    echo ""
}

# ======================================
# Handle arguments
# ======================================

if [ -n "$1" ]; then
    case "$1" in
        "-c" | "--convert")
            runLedgerConverter
            ;;
        "-r" | "--report")
            echo "Reports"
            ;;
        "-t" | "--test")
            runTests
            ;;
        "-a" | "--accounts")
            runLedgerAccounts
            ;;
        "-h" | "--help")
            printUsage
            ;;
        *)
            echo "$0: illegal option $1"
            printUsage
            ;;
    esac
    exit
fi


# ======================================
# Default program without arguments
# ======================================
printUsage