# fix-umlauts

This little project consists of two small scripts. The first one `convert.py` is used to convert a dictionary, either a .dic file or an Open-/LibreOffice dictionary, to the needed file format.

```bash
$ python3 convert.py <dictionary> <output_file>
``` 

The second one is used to fix the umlauts in a file. It needs two arguments: the file we generated before and the file to fix. 

```bash
$ python3 fix.py <generated_file> <file_to_fix>
```