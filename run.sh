#!/bin/bash

set -e

TARGET_HOME=$(eval echo ~$(logname))
MODE="\$1"

# Bold/Bright colors
RED="\e[1;31m"
GREEN="\e[1;32m"
BLUE="\e[1;34m"
MAGENTA="\e[1;35m"
YELLOW="\e[1;33m"

# Reset
RESET="\e[0m"


echo -e "${YELLOW}SmrtiLog - A Keystroke Logger Simulation by SudoHopeX${RESET}"

# install mission dependencies n call
function install_missing() {
    local pkg="$1"

	echo -e "${BLUE}[>_] Checking ${pkg} Installation...${RESET}"

	if ! dpkg -s $pkg >/dev/null 2>&1; then
	   	echo -e "${RED}[!] ${pkg} Installation not found. Installating it...${RESET}"
	   	sudo apt-get install $pkg -y
	   	echo -e "${GREEN}[✔] ${pkg} Installation successfully Done..${RESET}"
	else
		echo -e "${BLUE}[✔] ${pkg} Installation Found.${RESET}"
	fi
}

function update_sys(){
  echo -e "${MAGENTA}[>_] Updating system...${RESET}"
  sudo apt-get update >/dev/null 2>&1
  echo -e "${GREEN}[✔] System Updated...${RESET}"
}

# start SmrtiLog Venv
function start_venv(){
  # creating a venv named SmrtiLog
  python3 -m venv "$TARGET_HOME"/SmrtiLog

  # starting venv
  source "$TARGET_HOME"/SmrtiLog/bin/activate
}


# setup SmrtiLog - Keystroke Logger
function setup_smrti_log_keystroke_logger(){

  # perform system update
  update_sys

  # checking for dependencies installation & installing if not found
  install_missing python3
  install_missing python3-venv

  start_venv # start SmrtiLog venv

  # Installing SmrtiLog required libraries or packages
  echo -e "${MAGENTA}[>_] Installing required SmrtiLog dependencies & pkgs....${RESET}"
  pip3 install requests pynput cryptography

  echo -e "${GREEN}[✔] SmrtiLog Setup Successfully Done...${RESET}"
}


case "\$MODE" in

  --help|-h)

      echo -e "${GREEN}SmrtiLog - A Keystroke logger Simulation by SudoHopeX

${MAGENTA}Uses:
    ${BLUE}./run.sh [MODE]   ${RESET}or   ${BLUE}bash run.sh [MODE]

${MAGENTA}MODE:
    ${YELLOW}--help ( -h )             ${BLUE}show usages
    ${YELLOW}--setup ( -s )            ${BLUE}setup Keystroke logger
    ${YELLOW}--run ( -r ) [Default]    ${BLUE}run Keystroke logger
    ${YELLOW}--setupRun ( -sr )        ${BLUE}setup & then execute Keystroke logger

${MAGENTA}NOTE:
      ${RED}To stop SmrtiLog keystroke logger press 'ESC'
      Must Use 'sudo' privilege when performing setup ${BLUE}e.g. sudo bash run.sh --setup

${MAGENTA}CONTACT:
    ${GREEN}For any query or reporting contact SudoHopeX
      ${YELLOW}GitHub     =>  ${BLUE}@SudoHopeX
      ${YELLOW}LinkedIn   =>  ${BLUE}in/dkrishna0124
${RESET}"
      ;;

  --setup|-s)

      update_sys                         # call update system
      setup_smrti_log_keystroke_logger   # call setup fucntion
      deactivate                         # deactivate SmrtiLog Venv
      ;;

  --setupRun|--SetupRun|--setuprun|-sr)

      update_sys                         # call update system
      setup_smrti_log_keystroke_logger   # call setup fucntion
      python3 main.py                    # execute main.py
      deactivate                         # deactivate venv after successful execution
      ;;

  --run|-r|*)

      start_venv      # start SmrtiLog Venv
      python3 main.py # execute main.py
      deactivate      # deactivate venv after successful execution
      ;;

esac

echo -e " ${YELLOW} Thanku for playing with SmrtiLog - SudoHopeX"
