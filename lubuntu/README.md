<img src="https://lubuntu.net/wp-content/uploads/2017/12/Lubuntu_logo.svg" width="25%" height="25%">

### Natural Scrolling in Lubuntu 18.04
```
synclient VertScrollDelta=-120
```
Once you’ve got that done, create an entry in your autostart for it and voila!

    Go to Menu → Preferences → Preferences → Default applications for LXSession → Autostart → Manual autostarted applications
    Add your command
    Click add
    Click OK

Alternately, you could also drop a Desktop Entry in ~/.config/autostart.
<br><br>
OR
<br><br>
You can try this. Notice 6 and 7 are swapped.<br>
NaturalScrolling:
```
echo "pointer = 1 2 3 5 4 7 6 8 9 10 11 12" > ~/.Xmodmap && xmodmap ~/.Xmodmap
```
Note: this does not affect on Terminal.<br>
Reference: https://askubuntu.com/questions/908484/natural-scrolling-in-lubuntu-17-04

### How to restore the default Lubuntu panel?
```
cp /usr/share/lxpanel/profile/Lubuntu/panels/panel ~/.config/lxpanel/Lubuntu/panels
lxpanelctl restart
```
`Actually I tried it before and the 1st and 2nd codes didn't seem to work. However, I tried the 3rd one now and did work! `<br>
Reference: https://askubuntu.com/questions/64631/how-to-restore-the-default-lubuntu-panel
