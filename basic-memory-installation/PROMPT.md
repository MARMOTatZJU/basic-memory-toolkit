```markdown
$asd-ste100-writing-context 

Prepare for a complete installation of runtime environment of [Basic Memory](https://github.com/basicmachines-co/basic-memory).

You have an existing [code report](../basic-memory-code/code-report/) to refer to.

The customized requirements of the complete installation are:

- within WSL2
- uv-managed
- docker container-based
  - write .dockerfile for building the docker image
  - write scripts to perform docker runtime installation
  - set up environment directly within docker container (no need to isolate)
    - in form of .dockerfile
  - test dockerfile
- gpu support (local 5090 laptop)
  - NV software stack (NVIDIA driver for WSL2, CUDA/CuDNN installation in WSL2, etc.)
  - inference framework(ollama, onnx, etc.)

Plan for the installation and present to me a structural and concise list of the dependencies in the order of the installation. Show me the name and the version of every item in your list.
```