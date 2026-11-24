A database for the installation of Basic Memory installation is located at `./basic-memory-toolkit/basic-memory-installation/`:

- it corresponds to a complete installation of Basic Memory
- e.g. entry point: `./basic-memory-toolkit/basic-memory-installation/ENTRY-POINTS.md`
- e.g. quick start: `./basic-memory-toolkit/basic-memory-installation/QUICK-START.md`
- e.g. typical installation plan: `./basic-memory-toolkit/basic-memory-installation/installation-plan.md`
- etc.


A code report of [Basic Memory](https://github.com/basicmachines-co/basic-memory) is located at `./basic-memory-toolkit/basic-memory-code/code-report/`.

- it contains comprehensive scan and analysis of Basic Memory's implementation.
  - including an inventory of the BM's functionalities and their entry points.
- RUNTIME MODE:
  - INSTALLTAION MODE:
    - run the complete installation within docker containers by following the [user-tutorial](./basic-memory-code/code-report/17-user-tutorial.md)
      - try to launch docker containers if they are not started.
        - you are authorized to use Docker
        - if the sandbox blocks Docker access, request the permissions needed for these actions.
      - stop and remove the created docker containers after stoping the work.
    - maximally leverage the functionalities supported by Basic Memory in mind to boost the efficiency and quality of the work.
      - utilize the Basic Memory-supported GPU-accelerated semantic search to boost the scan/retrieval
    - always keep maximizing the inference performance and maximally utilize the local computing resources
      - continuously measure the inference performance
      - keep increasing parallelism UNTIL REACHING THE INFERENCE PERFORMANCE PEAK OR RESOURCE LIMIT
        - priotize GPU resources over CPU resources if the former is available.
          - maximize the usage of GPU by increasing the batch size
        - in case of using docker container as runtime environment of Basic Memory, instantiate more docker containers
        - otherwise, use multi-processing library and spawn more processes
  - SKILL MODE:
    - run the skill version by following `user-tutorial-skill-version`: [user-tutorial-skill-version](./basic-memory-code/code-report/19-user-tutorial-skill-version.md)
    - spawn subagents to accelerate if considered necessary in terms of efficiency
- RUNTIME MODE Switching Strategy:
  - try RUNTIME MODEs in the priority list
    - always start with the first item in the priority list.
    - if the trial of the current RUNTIME MODE fails, then fall back to the next one that has lower priority
  - priority list (from high to low):
    - INSTALLATION MODE
    - SKILL MODE

  - if complete installation of basic memory is available, then switch to INSTALLATION MODE
  - if not, then fall back to SKILL MODE


the workspace location: `./basic-memory-databases/basic-memory-database-workspace/`

- you can use this workspace to operate such as:
  - clone GitHub repositories like Basic-Memory
  - store your drafts
  - create skills that help the creation and operation of the database.
  - etc.


the workspace essential assets location: `./basic-memory-toolkit/basic-memory-database-workspace-essential-assets/`

- consider saving newly created utility elements to facilitate furture works.
  - e.g. assets/elements/tools/scripts/etc.
  - transform them into a more generic version before adding them.
- elements to be excluded:
  - temporary configurations/assets/etc. that have low probability to be reused
  - sensitive information
    - e.g. absolute path on the host machine.
    - e.g. usernames, user-related names, etc.
    - e.g. user data/notes, etc.
