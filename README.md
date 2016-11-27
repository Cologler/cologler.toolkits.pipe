# pipe.toolkits.cologler

## how to use

simple. just a example:

``` cmd
dir | pipe dir start {path}
[1]        [2] [3]
```

read output of [1] `dir` and use parser [2] `dir` and execute command [3] `start {path}`.

all argument (`{???}`) will convert to actual value and send to command.

for each line, if any argument cannot parse, then ignore the line.

**Tip: you can try use `dir | pipe dir echo XXX` to see what command will be execute.**

* pipe  use `os.system`  to send command.
* pipes use `subprocess` to send command.
* pipes use `subprocess` to concurrent send command.

## available parser

name  | param | desc
:---  | :---- | :---
ALL   | line  | origin line for all parser
dir   | name  |
dir   | path  |
acdcli| id    |
acdcli| path  |

