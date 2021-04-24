
A vim course for LaTeX

## Promised features

- Magic LaTeX conceal for preview within editor 
- [Shortcuts](https://github.com/SirVer/ultisnips) for writing LaTeX with `\infty` power, including:
    * Invoking Mathematica/python/etc within vim for anything
    * Regex conversion: `< 0 |` ---auto magic-----> `\langle 0 |` 
    * Context aware shortcuts: `$$ ;a $$` ----> `$$ \alpha $$`, but `;a` without surrounding `$$` doesn't change. 
- When magic conceal isn't enough: a **live** LaTeX preview using [this tool](https://github.com/iamcco/markdown-preview.nvim)
- Vanilla LaTeX using the famous [VimTeX](https://github.com/lervag/vimtex) plugin


## Install

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

**That's it.**

## Usage

Open vim and find a simple setup ready for you.

1. Many suggestions to learn: 

    1. Attend the lectures.
    2. Do `vimtutor`
        a. Know the `vimrc` file very well.
    3. Use `:help` command in vim for what you don't understand.
    4. Google
    5. Stack Overflow


1. Before each class, run 
```
    git stash   #safely stashes any changes you may have made into the repo - don't do it though.
    git pull    # pulls the latest files from this repo.
```
followed by `:PlugInstall` to stay in sync with this setup.



## Adding your own changes

Make a file `~/.myvimrc` and add your custom settings there. 
This file is being sourced in `vimrc` file at the end.

For sake of simplicity, this will be the name of custom `vimrc` throughout the course.



## Like the course?

Leave a feedback on my email.

