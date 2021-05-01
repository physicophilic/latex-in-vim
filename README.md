

## LaTeX in Vim

A course on how to utilize most powerful editor for scientific writing.
See a video of the promised features [here](https://www.youtube.com/watch?v=hpQBHVaFE1I). 

<details>

<summary>Click here for summary</summary>

- Magic LaTeX conceal for preview within editor 
- [Shortcuts](https://github.com/SirVer/ultisnips) for writing LaTeX with `\infty` power, including:
    * Invoking Mathematica/python/etc within vim for anything
    * Regex conversion: `< 0 |` ---auto magic-----> `\langle 0 |` 
    * Context aware shortcuts: `$$ ;a $$` ----> `$$ \alpha $$`, but `;a` without surrounding `$$` doesn't change. 
- When magic conceal isn't enough: a **live** LaTeX preview using [this tool](https://github.com/iamcco/markdown-preview.nvim)
- Vanilla LaTeX using the famous [VimTeX](https://github.com/lervag/vimtex) plugin

</details>

### How it works

I add commented code (new features' settings) and each Saturday discuss them while
uncommenting during the class. Think of it as providing lecture notes
during the class and discussing thereafter.  


### What has been covered?

#### Lecture 4 (Planned)

- Conceal in vim
- Regular expression exercises

#### Lecture 3

- Using `git pull`, etc to fetch code from online repository
- Folding in vim
- Tiny intro to VimTeX: only covering `\ll, \le, \lv, \lc` commands

Now your `vim` should be compiling LaTeX. 

#### Lecture 2

- Concept of mappings, e.g. `nmap`. 
- Use of `vim-plug`, installing UltiSnips
- 2 snippet examples using UltiSnips (very important)

Find example snippets for yourself by taking inspiration from Gilles Castel
[here](https://github.com/gillescastel/latex-snippets)

#### Lecture 1

- Basic introduction to vim
- set options like `linewidth`, `number`, `spell`, and `colorscheme`.

Homework: doing `vimtutor`

### How to get started?

Even if you've not attended the lectures so far, if you do the following
steps, you'll be at least operationally prepared for the next lecture.


1. Backup pre-existing vim files if have used vim before:

```
# Linux/MacOS
mv ~/.vimrc ~/.myvimrc
mv ~/.vim ~/.myvim
```

On windows use file browser to backup `vimfiles` and `.vimrc` from the `$HOME` folder


2. Clone this repository

```
# Linux/MacOS
git clone https://github.com/physicophilic/vim-course ~/.vim
```
On windows you can use the web interface.  See HTG article [here for more on cloning](https://www.howtogeek.com/451360/how-to-clone-a-github-repository/).

3. Open vim, and run `:PlugInstall` 

To get fully prepared, you can read about stuff we've covered so far
above.

### How will you get the new commented code?

As each week we'll add new features, I will add new comments to the settings file. Therefore, before each class, all attendants should `git pull` - i.e. fetch the latest changes from this online repository into their `.vim` folder.

Before each class, run 
```
    git stash   #safely stashes any changes you may have made into the repo - don't do it though.
    git pull    # pulls the latest files from this repo.
```
followed by `:PlugInstall` to stay in sync with this setup.


### How to add your own changes?

Make a file `~/.myvimrc` and add your custom settings there. 
This file is being sourced in `vimrc` file at the end.

For sake of simplicity, this will be the name of custom `vimrc` throughout the course.

### How to learn vim ?

Many suggestions:

1. Attend the lectures.
2. Do `vimtutor`
3. Use `:help` command in vim for what you don't understand.
4. Google
5. Stack Overflow

### Like the course?

Leave a feedback on my email.

