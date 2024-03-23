- Dockerfile - testing sandbox dockerfile
- testing pipeline .(py) - pipeline implementation

Architecture of the pipeline: <br>

1) Simply compile all the sources ('compile' function)
2) Start n iterations:
 - generate testcase ('generate_tests' function)
 - feed it to both solutions ('run_solution' function)
 - compare results
 - Do this until a divergent test is found

In all the mentioned functions we had burden of 'if' statements,
a statement per each language supported (in every function !). 
To add a new language, you will need to go through all these 
functions and add your new "if" handling your specific language 
with some new extension.

It was decided to write a separate class for each supported language
using the "chain of responsibility" design pattern. So, the chain
will find a class that should handle a specific code file, not
a bunch of 'if' statements in every function.

With this approach you would need to:

- Add a new enum value, handling the extension, e.g. rs = auto(),
into FileType enum.
- Add a class, inheriting ISrcCodeWorker
- Implement all the functions: compile, generate_tests, run
- Add it to the chain: the chain should always end with 
SrcUnsupportedWorker, so put reference to this class instead in the
pre last class in the chain and make SrcUnsupportedWorker the last 
(right after your class)


e.g the chain: <br>
SrcChainStarter -> SrcPythonWorker -> SrcCppWorker ->
SrcUnsupportedWorker

you make it <br>
SrcChainStarter -> SrcPythonWorker -> SrcCppWorker -> SrcRustWorker ->
SrcUnsupportedWorker

Thus adding SrcRustWorker.

---
I hope this is not over-engineering, but something that really
improves maintainability...


