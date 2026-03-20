#!/usr/bin/env bash

# ==========================================
# Ransomware Load Generator (Reset per Burst)
# Simulates how ransomware targets different file types
# ==========================================

TARGET_DIR="monitor_folder"

GREEN="\033[0;32m"
YELLOW="\033[1;33m"
CYAN="\033[0;36m"
RESET="\033[0m"

mkdir -p "$TARGET_DIR"
cd "$TARGET_DIR" || exit 1

clear
echo -e "${CYAN}============================================================${RESET}"
echo -e "${CYAN}   RANSOMWARE LOAD GENERATOR  (Reset per Burst)            ${RESET}"
echo -e "${CYAN}============================================================${RESET}"
echo
echo -e "${YELLOW}📁  Target directory : ${RESET}$(pwd)"
echo -e "${YELLOW}⚙️   Behaviour       : Per round you choose count + data type.${RESET}"
echo -e "${YELLOW}♻️   Note            : Old files are wiped before each round.${RESET}"
echo -e "${YELLOW}⏹  Exit             : Type 'q' + ENTER anytime.${RESET}"
echo

round=1

while true; do
    echo
    echo -e "${CYAN}────────────  ROUND ${round}  ────────────${RESET}"

    # -------- files count --------
    echo -ne "${YELLOW}[#] Files to simulate this round (0 = skip, 'q' = quit): ${RESET}"
    read -r BATCH

    if [[ "$BATCH" == "q" || "$BATCH" == "Q" ]]; then
        echo -e "${GREEN}[✓] Stopping load generator on user request.${RESET}"
        break
    fi

    if ! [[ "$BATCH" =~ ^[0-9]+$ ]]; then
        BATCH=0
    fi

    if [[ "$BATCH" -eq 0 ]]; then
        echo -e "${YELLOW}[-] 0 selected → no files generated this round.${RESET}"
        round=$(( round + 1 ))
        continue
    fi

    echo -e "${YELLOW}[*] Files this round : ${RESET}${BATCH}"

    # -------- file type pattern --------
    echo
    echo -e "${YELLOW}🎯  Choose target data type (simulated ransomware focus):${RESET}"
    echo "    1) Text notes        (.txt)"
    echo "    2) Office documents  (.docx, .pdf, .xlsx)"
    echo "    3) Personal images   (.jpg, .png)"
    echo "    4) Realistic mix     (txt + docs + images)"
    echo "    5) Full sweep        (all above types, sequential)"
    echo -ne "${YELLOW}[?] Choice [1-5, default 4]: ${RESET}"
    read -r CHOICE

    case "$CHOICE" in
        1)
            EXTENSIONS=("txt")
            PATTERN_DESC="plain text notes"
            ;;
        2)
            EXTENSIONS=("docx" "pdf" "xlsx")
            PATTERN_DESC="office documents"
            ;;
        3)
            EXTENSIONS=("jpg" "png")
            PATTERN_DESC="personal images"
            ;;
        5)
            EXTENSIONS=("txt" "docx" "pdf" "xlsx" "jpg" "png")
            PATTERN_DESC="full sweep across all data types"
            ;;
        *)
            EXTENSIONS=("txt" "docx" "pdf" "jpg" "png" "xlsx")
            PATTERN_DESC="mixed documents and images"
            ;;
    esac

    echo -e "${YELLOW}[*] Target profile   : ${RESET}${PATTERN_DESC}"

    # -------- wipe old files --------
    echo -e "${YELLOW}[*] Resetting lab    : clearing old files in ${TARGET_DIR} ...${RESET}"
    rm -f -- file* 2>/dev/null

    # numbering fresh each round
    current_index=1
    batch_end=$BATCH

    echo -e "${YELLOW}[*] Simulating ${BATCH} encrypted files (file1.* .. file${batch_end}.*)...${RESET}"

    total=$BATCH
    i=1
    ext_count=${#EXTENSIONS[@]}

    for n in $(seq "$current_index" "$batch_end"); do
        idx=$(( (n - 1) % ext_count ))
        ext="${EXTENSIONS[$idx]}"

        echo "test${n}" > "file${n}.${ext}"

        percent=$(( i * 100 / total ))
        bar_width=28
        filled=$(( percent * bar_width / 100 ))
        empty=$(( bar_width - filled ))

        bar_filled="$(printf '%*s' "$filled" '' | tr ' ' '#')"
        bar_empty="$(printf '%*s' "$empty" '' | tr ' ' '.')"
        bar="${bar_filled}${bar_empty}"

        echo -ne " [${bar}] ${percent}%  -> ${GREEN}file${n}.${ext}${RESET}\r"
        i=$(( i + 1 ))
        sleep 0.05
    done

    echo
    echo -e "${GREEN}[✓] Burst complete → simulated ransomware touched ${BATCH} ${PATTERN_DESC}.${RESET}"
    echo -e "${GREEN}[→] Check Detection Engine window for behaviour alerts.${RESET}"

    round=$(( round + 1 ))
done

echo
echo -e "${GREEN}[✓] Load generator finished.${RESET}"
