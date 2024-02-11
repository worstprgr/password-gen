# Password Generator
Generates a password and copies the result to clipboard.  

> [!Warning]
> This tool uses all alphanumeric ASCII characters and this set of special characters: `!#$%&()*+-=?@_`
>   
> The reason for the limiting is, that some services having still trouble to escape certain characters \*sigh\*  
> But you can change it to your needs: `class PassGen` -> Var: `self.other`  


```commandline
usage: pass.py [-h] [-n] length

positional arguments:
  length      How long the password should be

options:
  -h, --help  show a help message and exit
  -n, --nocp  If provided, this program would not store the output in the OS clipboard.
```
