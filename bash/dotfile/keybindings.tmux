set -g prefix M-c
unbind-key -n C-a

bind-key k selectp -U
bind-key j selectp -D
bind-key h selectp -L
bind-key l selectp -R

bind-key [ splitw -v
bind-key ] splitw -h
