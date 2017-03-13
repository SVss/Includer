## Extended includer script

```
Extended #include directive file processor.

Works both with relative and absolute paths:
	#include "test.txt"
	#include "../previous.ext"
	#include "X:/path/to/file.inc"

Common include directive syntax:

	#include "<file_path>" [{]

If "{" occures at the end of line, #include directive must be followed by
replace-dictionary declaration:

	#include "<file_path>" {
		'<some_key>': '<some_value>',
		...
	}
	...

Replace operation is performed after all #include-s processed, so
each <some_key> appearance in <file_path> and it's included files content
will be replaced in output with <some_value> text.

Usage format:

	python process.py  <input_file_name>  <output_file_name> [-?]

Use -? to see this help.
```
