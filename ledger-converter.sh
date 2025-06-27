
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

printUsage() {
    echo ""
    echo "Ledger Converter"
    echo ""
    echo "Usage: $0 [ARGS]"
    echo ""
    echo "Arguments:"
    echo "None        : Run Converter"
    echo "-t | --test : Run Tests"
    echo "-h | --help : Get Helper"
    echo ""
}

# Handle arguments
if [ -n "$1" ]; then
    case "$1" in
        "-t" | "--test")
            runTests
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

# Default program without arguments
runLedgerConverter