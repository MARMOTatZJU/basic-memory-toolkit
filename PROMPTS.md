# Utility Prompts

Search for `SPECIFY_HERE` and specify your task context.


## Database Creation/Synchronization

```markdown
Based on the usage tutorial of Basic-Memory `user-tutorial-skill-version`, 

- if the a TARGET DATABASE exists, then perform an one-way sync from the SOURCE to the TARGET DATABASE 
  - NOTE: one-way sync forces the destination to exactly match the source.
- if not, then summarize the SOURCE and create a TARGET DATABASE upon the SOURCE.

- `user-tutorial-skill-version`: [user-tutorial-skill-version](./basic-memory-code/code-report/19-user-tutorial-skill-version.md)
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
