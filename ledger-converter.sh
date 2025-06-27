# ======================================
# Load Configurations
# ======================================
CONFIG_FILE=./config.sh
if [[ ! -f $CONFIG_FILE ]]; then
    echo "Configuration file not found; Using example file"
    CONFIG_FILE="${CONFIG_FILE}.example"
fi
source $CONFIG_FILE
echo ""

# ======================================
# Functions
# ======================================

runLedgerConverter() {
    # Activate environment to run code
    source venv/bin/activate

    # Run code
    python3 ledger-converter.py

    # Deactivate environment
    deactivate
}

runTests() {
    # Activate environment to run code
    source venv/bin/activate

    # Run code
    python3 -m unittest --verbose

    # Deactivate environment
    deactivate
}

runLedgerAccounts() {
    DEFAULT_LEDGER_FILE="./tests/ledger_test.ledger"
    OUTPUT_ACCOUNT_FILE="./input/config/accounts.txt"

    if [[ $LEDGER_FILE == $DEFAULT_LEDGER_FILE ]]; then
        OUTPUT_ACCOUNT_FILE="${OUTPUT_ACCOUNT_FILE}.example"
    fi

    ledger -f $LEDGER_FILE accounts > $OUTPUT_ACCOUNT_FILE
}

printUsage() {
    echo ""
    echo "Ledger Converter"
    echo ""
    echo "Usage: $0 [ARGS]"
    echo ""
    echo "Arguments:"
    echo "None             : Run Converter"
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

runLedgerConverter