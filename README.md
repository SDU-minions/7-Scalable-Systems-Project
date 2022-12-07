# 7-Project

Spark
----------------------------

After running the docker application, Spark needs to be set up.

Execute into the Spark master container
```sh
docker exec -it spark-master bin/sh
```

Create Spark environment
```sh
bash scripts/create_environment.sh
```

Submit the applications to Spark (Run in two seperate terminals)
```sh
bash scripts/start_commit_consumer.sh
bash scripts/start_language_consumer.sh
```

Format of the commit messages
----------------------------
```
<type>: <subject>
<BLANK LINE>
<body>
<BLANK LINE>
<footer>
```

Any line of the commit message cannot be longer 100 characters! This allows the message to be easier to read on github as well as in various git tools.

### Subject line        
Subject line contains succinct description of the change.

#### Allowed `<type>`
* feat (feature)
* fix (bug fix)
* docs (documentation)
* style (formatting, missing semi colons, …)
* refactor
* test (when adding missing tests)
* chore (maintain)

#### `<subject>` text
* use imperative, present tense: “change” not “changed” nor “changes”
* don't capitalize first letter
* no dot (.) at the end

### Message body
* just as in <subject> use imperative, present tense: “change” not “changed” nor “changes”
* includes motivation for the change and contrasts with previous behavior

http://365git.tumblr.com/post/3308646748/writing-git-commit-messages
http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html

### Message footer

#### Breaking changes

All breaking changes have to be mentioned in footer with the description of the change, justification and migration notes

```
BREAKING CHANGE: isolate scope bindings definition has changed and
    the inject option for the directive controller injection was removed.
    
    To migrate the code follow the example below:
    
    Before:
    
    scope: {
      myAttr: 'attribute',
      myBind: 'bind',
      myExpression: 'expression',
      myEval: 'evaluate',
      myAccessor: 'accessor'
    }
    
    After:
    
    scope: {
      myAttr: '@',
      myBind: '@',
      myExpression: '&',
      // myEval - usually not useful, but in cases where the expression is assignable, you can use '='
      myAccessor: '=' // in directive's template change myAccessor() to myAccessor
    }
    
    The removed `inject` wasn't generaly useful for directives so there should be no code using it.
```

#### Referencing issues

Closed bugs should be listed on a separate line in the footer prefixed with "Closes" keyword like this:
```
Closes #234
```

or in case of multiple issues:
```
Closes #123, #245, #992
```

Examples
--------
```
feat: onUrlChange event (popstate/hashchange/polling)
```

```
fix: couple of unit tests for IE9

Older IEs serialize html uppercased, but IE9 does not...
Would be better to expect case insensitive, unfortunately jasmine does
not allow to user regexps for throw expectations.

Closes #392
Breaks foo.bar api, foo.baz should be used instead
```

```
feat: ng:disabled, ng:checked, ng:multiple, ng:readonly, ng:selected



Closes #351
```

```
style: add couple of missing semi colons
```

```
docs: updated fixed docs from Google Docs

Couple of typos fixed:
- indentation
- batchLogbatchLog -> batchLog
- start periodic checking
- missing brace
```

```
feat: simplify isolate scope bindings

Changed the isolate scope binding options to:
  - @attr - attribute binding (including interpolation)
  - =model - by-directional model binding
  - &expr - expression execution binding

BREAKING CHANGE: isolate scope bindings definition has changed and
the inject option for the directive controller injection was removed.
```

[source](https://gist.github.com/stephenparish/9941e89d80e2bc58a153#file-commit-md)
