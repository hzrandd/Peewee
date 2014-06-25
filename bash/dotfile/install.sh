#!/bin/bash

install_git()
{
    echo 'Install git_config'
    cp -v gitconfig ~/.gitconfig
}

install_pip_mirror()
{
    echo 'Install pip mirrors'
    mkdir ~/.pip
    cp -v pydistutils.cfg ~/.pydistutils.cfg
    cp -v pip.conf ~/.pip/pip.conf
}

install_byobu_keybinding()
{
    echo 'Install byobu keybinding'
    cp -v keybindings.tmux ~/.byobu/keybindings.tmux
}

install_screen()
{
    echo "Install screenrc"
    cp -v screenrc ~/.screenrc
}

if [[ $1 == 'git' ]];then
    install_git
elif [[ $1 == 'pip' ]]; then
    install_pip_mirror
elif [[ $1 == 'byobu' ]]; then
    install_byobu_keybinding
elif [[ $1 == 'all' ]]; then
    install_git
    install_pip_mirror
    install_byobu_keybinding
else
    echo "Usages: $0 <git|pip|byobu|all>"
fi
