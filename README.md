# A short course on vim

Notice the file table above? You can access all the important files from there.
But before you begin copying, let me explain some concepts.

## Files for vim

Vim requires many files to do nifty things. The most important of them all, is called
`.vimrc`, (vim run commands) which is the **settings** file for vim. It is like the bloodstream
of vim if you prefer a metaphor.

Then, all the baggage vim needs to expand snippets, store plugins, custom syntax, etc, all is placed
in a folder called `.vim`. A plugin is simply some code written in vim language/some other language.
For example, a colorscheme file is a plugin using which you can change appearance of vim. 
This is stored in `.vim/colors`. You can see an example colorscheme in the `colors` folder above.

Note: on windows, `.vim` must be replaced by `vimfiles`. 

## .vim, .vimrc location

The `.vim` and `.vimrc` files must go inside your home folder.

- On linux and macOS, there's a designated folder called home, accessed using `~/` in the terminal.
- On windows, the home folder is `C:Drive/Users/YOUR_USERNAME/`. 

From here onwards, I will use `~/` to denote home folder exclusively.

**Alternative location on linux/macOS** 

`~/.vimrc` can be moved to `~/.vim/vimrc`.

Note that at the new location `.` gets removed. This is what we'll follow.

For windows, analogously `~/.vim` -> `~/vimfiles/vimrc` should work, but I haven't tested it.

## Covering up for Lecture 1

### Check your installation

- Check `vim --version`, and ensure `+python3` and `+termguicolors` are present in the table.
    - If there's a `-` sign instead, especially for python, i.e. `-python3`, you'll not be able to benefit from whatever I discuss.
- If these are absent, do
    - `brew install vim` #on mac; I've tested it and it works.
    - `sudo apt install vim`  #on a recent debian/mint/ubuntu; I use it myself
    - Windows download from vim.org does have these things enabled.

Also, if you're good at using windows, I recommend you install chocolatey, the new windows terminal, 
and then you can do `choco install vim` from your Powershell to install vim with all the features. 
This has an added benefit that running vim would be easier.

### Copy pasting

After you have identified your home folder, do the following:

- save the `.vimrc` file from the file table above into your home directory.
- create a new folder called `.vim` or `vimfiles` in this directory depending on your OS.
- create a colors folder within, and paste the example colorscheme from the table there. 

After this you'll have to do `vimtutor` to get started - it will give you a good introduction.

To open `vimtutor` open your terminal and type vimtutor, and it should open.




