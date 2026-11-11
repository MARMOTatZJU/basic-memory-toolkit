# Utility Prompts

Search for `SPECIFY_HERE` and specify your task context.


## Database Creation/Synchronization

```markdown
Based on the usage tutorial of Basic-Memory `user-tutorial-skill-version`, 

- if the a TARGET DATABASE exists, then perform a synchronization from the SOURCE to the TARGET DATABASE
  - Desired synchronization type: SPECIFY_HERE
  - Descriptions of synchronization types:
    - ONE-WAY SYNC: force the DESTINATION DATABASE to exactly match the SOURCE; perform sync incrementally and ignore unchanged items.
      - Typical scenarios: database creation, force sync of outdated database, etc.
    - APPEND-ONLY SYNC: insert new records from the SOURCE to the DESTINATION DATABASE; ignores deletes; try to find updated items in the DESTINATION DATABASE and make corresponding updates.
      - Typical scenarios: conversation memory record, etc.
- if not, then summarize the SOURCE and create a TARGET DATABASE upon the SOURCE.

- `user-tutorial-skill-version`: [user-tutorial-skill-version](./basic-memory-toolkit/basic-memory-code/code-report/19-user-tutorial-skill-version.md)
- the SOURCE location:
  - SPECIFY_HERE
- the TARGET DATABASE location:
  - SPECIFY_HERE
- the workspace location: SPECIFY_HERE
  - you can use this workspace to operate such as:
    - clone GitHub repositories like Basic-Memory
    - store your drafts
    - create skills that help the creation and operation of the database.
    - etc.
- the workspace essential assets location: SPECIFY_HERE
  - consider saving newly created utility elements to facilitate furture works.
    - e.g. assets/elements/tools/scripts/etc.

Keep all the texts in their original languages.

After all works are finished, give me a report describing what you do and what you test.
```


## Rephrasing Texts

```markdown
$asd-ste100-writing-context Use the core ideas of ASD-STE100 writing style and rephrase all texts in the database. Keep all the texts in their original languages.

And make three rounds of reorganization/structural optimization to make the database:

- more compact
- more structural
- less complicated

In the end, report your works of each round.
```

## Cleaning up

### Scan

```markdown
Refer to:
- ./basic-memory-toolkit/UTILITY-ASSETS.md for paths to utility assets.
Currently, the utility assets are too redundant. Based on practical uses, make a full scan of these assets and spot points from which the redundancy can be reduced.

Focus on:
- List temporary files that can be safely deleted, such as
  - logs
  - cache
- List outdated files that are no longer needed, such as
  - outdated scripts
- etc.

$asd-ste100-writing-context Make a temporary report under the root directory of the repository.

- Applying the core ideas of ASD-STE100 writing style to this report.
- At the beginning of the report, write a "oneline" style (like `git log --graph --oneline`) hierarchical summary of the items spotted below.


Pause before taking actions to clean up.
```

### Per-Part Clean-up

```
Help to clean up SPECIFY_HERE and pay attention to following points:
- remove out dated elements and cleanup references to them if exists.
- for duplicated elements, decide the sides to preserve and remove the other sides with their references
```

### Report

```markdown
Make a "--oneline style" summary of operation items and write to `commit-message.txt` under the root path of the repo.
```
