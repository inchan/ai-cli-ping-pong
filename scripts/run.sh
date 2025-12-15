#!/bin/bash

set -e

# Setup basic paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_ROOT"

# Basic VENV check
if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment not found."
    echo "Please run scripts/run-mcp-inspector.sh once to set it up, or manually create it."
    read -p "Do you want to run setup now via inspector script? (y/n) " setup_choice
    if [[ "$setup_choice" == "y" ]]; then
        ./scripts/run-mcp-inspector.sh
        exit 0
    else
        echo "Exiting."
        exit 1
    fi
fi

# Function to run pytest with optional args
run_pytest() {
    echo ""
    echo "🚀 Running pytest: $@"
    echo "--------------------------------------------------------"
    ./venv/bin/pytest $@ -v
}

# Function for Interactive Menu using Arrow Keys
# Arguments: "Title" "Option1" "Option2" ...
menu() {
    local title="$1"
    shift
    local options=("$@")
    local cur=0
    local count=${#options[@]}
    
    # Enable non-blocking input and hide cursor
    stty -echo
    tput civis
    
    trap "tput cnorm; stty echo; exit" INT TERM
    
    while true; do
        # Clear screen/menu area (simple approach: clear whole screen for stability)
        clear
        
        echo "========================================================"
        echo "   $title"
        echo "==========================================================================================" # Adjust width as needed
        
        for ((i=0; i<count; i++)); do
            if [ $i -eq $cur ]; then
                printf "\033[7m👉 %s \033[0m\n" "${options[$i]}" # Highlight and add arrow
            else
                printf "   %s \n" "${options[$i]}" # Regular, with spaces for alignment
            fi
        done
        echo "==========================================================================================" # Adjust width as needed
        echo "Use ↑/↓ to move, Enter to select, 'b' to go back, 'q' to quit"
        
        # Read input (1 byte)
        read -rsn1 key
        
        # Check for escape sequence (arrow keys)
        if [[ "$key" == $'\x1b' ]]; then
            read -rsn2 key # Read remaining 2 bytes of escape sequence
            if [[ "$key" == "[A" ]]; then # Up arrow
                ((cur--))
                if [ $cur -lt 0 ]; then cur=$((count-1)); fi
            elif [[ "$key" == "[B" ]]; then # Down arrow
                ((cur++))
                if [ $cur -ge $count ]; then cur=0; fi
            fi
        elif [[ "$key" == "" ]]; then # Enter key
            break
        elif [[ "$key" == "q" ]]; then # q for quit (optional shortcut)
             cur=-1 # Indicator for quit if needed, or handle specifically
             break
        elif [[ "$key" == "b" ]]; then # b for back (optional shortcut)
             cur=-2 # Indicator for back
             break
        fi
    done
    
    # Restore settings
    tput cnorm
    stty echo
    MENU_RESULT=$cur
    return 0
}

# Function for Individual Test Selection
select_individual_test() {
    echo "🔍 Scanning test files..."
    
    # Create a temporary file to store the sorted list
    tmp_list=$(mktemp)
    
    # Find all test files, count lines, and sort by line count (descending)
    find tests -name "test_*.py" -print0 | xargs -0 wc -l | sort -nr > "$tmp_list"
    
    declare -a menu_options
    declare -a file_paths
    
    while IFS= read -r line; do
        count=$(echo "$line" | awk '{print $1}')
        file=$(echo "$line" | awk '{print $2}')
        
        # Skip "total" line or empty lines
        if [[ "$file" == "total" || -z "$file" ]]; then continue; fi
        
        rel_path=${file#./}
        # Format: "Cost: 123 | tests/path/to/test.py"
        menu_options+=("Cost: ${count} | ${rel_path}")
        file_paths+=("$file")
        
    done < "$tmp_list"
    rm "$tmp_list"
    
    menu_options+=("🔙 Back")
    
    menu "Select Individual Test" "${menu_options[@]}"
    choice=$MENU_RESULT
    
    # Handle Back or Quit
    if [[ $choice -lt 0 || $choice -eq $((${#menu_options[@]} - 1)) ]]; then
        return
    fi
    
    selected_file="${file_paths[$choice]}"
    clear
    run_pytest "$selected_file"
    read -p "Press Enter to continue..."
}

# Main Logic
while true; do
    options=(
        "🕵️  Run MCP Inspector (Interactive Debugging)"
        "🧪 Run Tests (Categorized)"
        "🚪 Exit"
    )
    
    menu "Gemini CLI - Main Menu" "${options[@]}"
    main_choice=$MENU_RESULT
    
    case $main_choice in
        0) # Inspector
            clear
            ./scripts/run-mcp-inspector.sh
            read -p "Press Enter to return..."
            ;;
        1) # Tests
            while true; do
                test_options=(
"📦 All Tests         (Run entire suite)"
"🧱 Unit Tests        (tests/test_*.py)"
"🔄 Integration Tests (tests/scenarios/)"
"🌐 E2E & Validation  (tests/mcp-validation/)"
"📄 Individual Test   (Select from list)"
"🔙 Back"
)
                
                menu "Test Categories" "${test_options[@]}"
                test_choice=$MENU_RESULT
                
                # Check for Back (b) or selected Back option
                if [[ $test_choice -eq -2 ]] || [[ $test_choice -eq 5 ]]; then
                    break 
                fi
                
                clear
                case $test_choice in
                    0) 
                        echo "🚀 Running Unit Tests..."
                        ./venv/bin/pytest tests/test_*.py -v
                        echo ""
                        echo "🚀 Running Integration Tests..."
                        ./venv/bin/pytest tests/scenarios/ -v
                        echo ""
                        echo "🚀 Running E2E & Validation Tests..."
                        ./venv/bin/pytest tests/mcp-validation/ -v
                        ;;
                    1) run_pytest tests/test_*.py ;;
                    2) run_pytest tests/scenarios/ ;;
                    3) run_pytest tests/mcp-validation/ ;;
                    4) select_individual_test; continue ;; # select_individual handles its own pause
                esac
                
                # Pause unless we just came from individual selection (which handles it)
                if [[ $test_choice -ne 4 ]]; then
                     read -p "Press Enter to continue..."
                fi
            done
            ;;
        2) # Exit
            clear
            echo "Bye! 👋"
            exit 0
            ;;
        -1) # q pressed
             clear
             echo "Bye! 👋"
             exit 0
             ;;
    esac
done
