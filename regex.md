
# Regular expressions

Goal: To learn how to manipulate text easily. 

## Sample text

The purpose of our lives is to be happy. — Dalai Lama
Life is what happens when you’re busy making other plans. — John Lennon
Your time is limited, so don't waste it living someone else's life. – Steve Jobs

- [Normal replacements] (`s/word/some_other_word/g`)
- [Delete all the capitals] (`s/[A-Z]//g`) 
- [De-capitalise] (`s/\([A-Z]\/\l\1/g`) 
- [Try to recapitalize] (`s/\. \([a-z]\/\. \u\1/g`)
- [Another step.] (`s/^\([a-z]\/\u\1/g`) 

## Common elements {{{

- Groups: [A-Z], [p-q], [0-9], [^.]
- Special characters for group extension: 
    * . = anything
    * `$` = end of the line
    * `\` = for escaping anything
    * `/` = separator 
    * `*` = arbitrary repeats of preceding group
    * `\+` = at least 1 or more
- Capturing groups: (group) or `\(group\)` (depends on software)

}}}

## Exercises {{{

In one regex substitution, make
- `A B   C   D  E    F    G`    to `ABCDEFGH`
- `AA BB   CCC  DDD  EEE   FFFFF  GGGGG` to `ABCDEFGH`

One practical exercise if there's time.
`https://parade.com/937586/parade/life-quotes/`

}}}

### Answers {{{

1. `s/\s*\([A-Z]\)\s*/\1/g`
2. `s/\s*\([A-G]\)[A-G]*\s*/\1/g`

}}}
