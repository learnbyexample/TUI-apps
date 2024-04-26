# Regexp field processing

As seen earlier, `awk` automatically splits input into fields (based on space/tab/newline characters) which are accessible using `$N` where `N` is the field number you need. You can use the `-F` option or assign the `FS` variable to set a regexp based input field separator.

```bash
$ echo 'goal:amazing:whistle:kwality' | awk -F: '{print $1}'
goal

# one or more alphabets will be considered as the input field separator
# the first field will be empty since there's nothing before 'Sample'
$ echo 'Sample123string42with777numbers' | awk -F'[a-zA-Z]+' '{print $2}'
123
```

Use the `OFS` variable to set the output field separator. This value is used when you pass multiple arguments to the `print` statement as well as when you print the `$0` variable (if it has been modified).

```bash
# default OFS is a single space character
$ echo 'goal:amazing:whistle:kwality' | awk -F: '{print $2, $NF}'
amazing kwality

$ echo 'goal:amazing:whistle:kwality' | awk -F: -v OFS=%% '{print $2, $NF}'
amazing%%kwality
```

Here are some examples of printing the contents of the `$0` variable after manipulating field contents.

```bash
# updating a field will force $0 to be updated as well
$ echo 'Sample123string777numbers' | awk -F'[0-9]+' -v OFS=, '{$1=$1} 1'
Sample,string,numbers

# changing the value of NF will also rebuild $0
$ echo 'goal:amazing:whistle:kwality' | awk 'BEGIN{FS=OFS=":"} {NF=2} 1'
goal:amazing

$ echo 'goal:amazing:whistle:kwality' | awk -F: -v OFS=, '{$(NF+1)="sea"} 1'
goal,amazing,whistle,kwality,sea
```

The `FS` variable allows you to define the input field *separator*. In contrast, `FPAT` (field pattern) allows you to define what should the fields be made up of.

```bash
# lowercase whole words starting with 'b'
$ awk -v FPAT='\\<b[a-z]*\\>' -v OFS=, '{$1=$1} 1' table.txt
brown,bread
blue
banana

# fields enclosed within double quotes or made up of non-comma characters
$ echo 'eagle,"fox,42",bee,frog' | awk -v FPAT='"[^"]*"|[^,]*' '{print $2}'
"fox,42"
```
