

---

title: Getting closer to Gilles' setup
author: Manish RC

---


# Last time

- Did a demo
- Some action in vim
- Uncommented settings file [which everyone should have now]
- **HW** : doing vimtutor 

# This time

- Intro to git
- .vim via git
- Installing plugins
- Starting snippets

---

# Prerequisites:

- Install git
- Install python3 

PDF Viewers
- Install zathura for linux (sudo apt install zathura)
- Install skim for macOS (brew install skim)
- Get 32-bit portable SumatraPDF for windows from its website, and save executable at a location you know.

------


# .vim from github

- substituting earlier .vim 
    * Rename the first .vim, and .vimrc
    * Clone
        + git clone https://github.com/physicophilic/vim-course ~/.vim # for unix/linux 
        + windows users download from web. 
    * Explain .vimrc or .vim/vimrc
    * Warning: don't add custom changes here. If you want that, keep this folder only as a reference and continue with your earlier folder.

-----

# Concept of mapping

- Idea
    * mode: nmap/imap/..
    * LHS
    * RHS
- Illustrate

--------

# Installing plugins

- Get [vim-plug](https://github.com/junegunn/vim-plug)
- Install UltiSnips


# Intro to UltiSnips

- UltiSnips settings
- One example - writing comments in vimrc. 
- Show Gilles' [snippets](https://github.com/gillescastel/latex-snippets/blob/master/tex.snippets) for reference


# Next time

- VimTeX setup
