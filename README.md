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

## available parser

parser name|arg name|description
:--|:--|:--
dir|name|
dir|path|
acdcli|id|
acdcli|path|

