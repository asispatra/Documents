<img src="https://lubuntu.net/wp-content/uploads/2017/12/Lubuntu_logo.svg" width="25%" height="25%">

### Natural Scrolling in Lubuntu 18.04
You can try this. Notice 6 and 7 are swapped.<br>
NaturalScrolling:
```
echo "pointer = 1 2 3 5 4 7 6 8 9 10 11 12" > ~/.Xmodmap && xmodmap ~/.Xmodmap
```
Reference: https://askubuntu.com/questions/908484/natural-scrolling-in-lubuntu-17-04

### How to restore the default Lubuntu panel?
```
cp /usr/share/lxpanel/profile/Lubuntu/panels/panel ~/.config/lxpanel/Lubuntu/panels
lxpanelctl restart
```
`Actually I tried it before and the 1st and 2nd codes didn't seem to work. However, I tried the 3rd one now and did work! `<br>
Reference: https://askubuntu.com/questions/64631/how-to-restore-the-default-lubuntu-panel
