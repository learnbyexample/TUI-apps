# Removing duplicates

`awk '!a[$0]++'` is one of the most famous `awk` one-liners. It eliminates line based duplicates while retaining the input order. The following example shows it in action along with an illustration of how the logic works.

```bash
$ cat purchases.txt
coffee
tea
washing powder
coffee
toothpaste
tea
soap
tea

$ awk '{print +a[$0] "\t" $0; a[$0]++}' purchases.txt
0       coffee
0       tea
0       washing powder
1       coffee
0       toothpaste
1       tea
0       soap
2       tea

# only those entries with zero in the first column will be retained
$ awk '!a[$0]++' purchases.txt
coffee
tea
washing powder
toothpaste
soap
```

Here are examples of dealing with duplicates based on specific fields instead of the whole line:

```bash
$ cat items.csv
brown,toy,bread,42
dark red,ruby,rose,111
blue,ruby,water,333
dark red,sky,rose,555
yellow,toy,flower,333
white,sky,bread,111
light red,purse,rose,333
dark red,soap,rose,314

# remove duplicates based on the last field
$ awk -F, '!seen[$NF]++' items.csv
brown,toy,bread,42
dark red,ruby,rose,111
blue,ruby,water,333
dark red,sky,rose,555
dark red,soap,rose,314

# list all duplicates based on the first and third fields
# recall that $1,$3 will add SUBSEP between the column values
$ awk -F, 'NR==FNR{a[$1,$3]++; next} a[$1,$3]>1' items.csv items.csv
dark red,ruby,rose,111
dark red,sky,rose,555
dark red,soap,rose,314
```
